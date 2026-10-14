<#
.SYNOPSIS
  Mod conflict checker for a Forge 1.20.1 Prism instance.
  Reads META-INF/mods.toml (plus jar-in-jar mods) from every jar in the mods folder and reports
  missing dependencies, version mismatches, incompatibilities, duplicate mod IDs and wrong-loader jars.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File check-mods.ps1
  powershell -ExecutionPolicy Bypass -File check-mods.ps1 -ShowOptional -OutFile report.txt
#>
param(
    [string]$InstanceDir = $PSScriptRoot,
    [switch]$ShowOptional,   # also list optional dependencies that are not installed
    [switch]$ListMods,       # print the full mod table
    [string]$OutFile
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

# ---------- environment ----------
$modsDir = Join-Path $InstanceDir 'minecraft\mods'
if (-not (Test-Path $modsDir)) { $modsDir = Join-Path $InstanceDir 'mods' }
if (-not (Test-Path $modsDir)) { throw "Mods folder not found under $InstanceDir" }

$mcVersion = '1.20.1'; $forgeVersion = '47.4.10'
$packFile = Join-Path $InstanceDir 'mmc-pack.json'
if (Test-Path $packFile) {
    $pack = Get-Content $packFile -Raw | ConvertFrom-Json
    foreach ($c in $pack.components) {
        if ($c.uid -eq 'net.minecraft') { $mcVersion = $c.version }
        if ($c.uid -eq 'net.minecraftforge') { $forgeVersion = $c.version }
    }
}

# ---------- version comparison (Maven-style, good enough for mod versions) ----------
function Split-Version([string]$v) {
    $v = ($v -replace '^[vV]', '').Trim()
    return , [string[]]@($v -split '[.\-+_]' | Where-Object { $_ -ne '' })
}

function Compare-Version([string]$a, [string]$b) {
    [string[]]$pa = Split-Version $a; [string[]]$pb = Split-Version $b
    $n = [Math]::Max($pa.Count, $pb.Count)
    for ($i = 0; $i -lt $n; $i++) {
        $x = if ($i -lt $pa.Count) { $pa[$i] } else { '0' }
        $y = if ($i -lt $pb.Count) { $pb[$i] } else { '0' }
        $xn = 0L; $yn = 0L
        $xi = [long]::TryParse($x, [ref]$xn); $yi = [long]::TryParse($y, [ref]$yn)
        if ($xi -and $yi) {
            if ($xn -ne $yn) { return [Math]::Sign($xn - $yn) }
        } elseif ($xi -ne $yi) {
            # numbers sort after qualifiers like "beta"
            if ($xi) { return 1 } else { return -1 }
        } else {
            $c = [string]::Compare($x, $y, $true)
            if ($c -ne 0) { return [Math]::Sign($c) }
        }
    }
    return 0
}

# Returns $true / $false, or $null if the version can't be checked
function Test-VersionInRange([string]$version, [string]$range) {
    if ([string]::IsNullOrWhiteSpace($range) -or $range.Trim() -eq '*') { return $true }
    if ([string]::IsNullOrWhiteSpace($version) -or $version -match '\$\{') { return $null }
    $range = $range.Trim()
    # bare version = Maven "recommended" version: Forge accepts anything
    if ($range -notmatch '^[\[\(]') { return $true }
    $groups = [regex]::Matches($range, '([\[\(])([^\]\)]*)([\]\)])')
    foreach ($g in $groups) {
        $open = $g.Groups[1].Value; $body = $g.Groups[2].Value; $close = $g.Groups[3].Value
        if ($body -notmatch ',') {
            if ((Compare-Version $version $body.Trim()) -eq 0) { return $true }
            continue
        }
        $parts = $body -split ',', 2
        $lo = $parts[0].Trim(); $hi = $parts[1].Trim()
        $ok = $true
        if ($lo) {
            $c = Compare-Version $version $lo
            if ($open -eq '[' -and $c -lt 0) { $ok = $false }
            if ($open -eq '(' -and $c -le 0) { $ok = $false }
        }
        if ($ok -and $hi) {
            $c = Compare-Version $version $hi
            if ($close -eq ']' -and $c -gt 0) { $ok = $false }
            if ($close -eq ')' -and $c -ge 0) { $ok = $false }
        }
        if ($ok) { return $true }
    }
    return $false
}

# ---------- minimal TOML reader (enough for mods.toml) ----------
function Parse-ModsToml([string]$text) {
    $result = @{ Top = @{}; Tables = New-Object System.Collections.ArrayList }
    $current = $result.Top
    $lines = $text -split "`r?`n"
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i].Trim()
        if ($line -eq '' -or $line.StartsWith('#')) { continue }
        if ($line -match '^\[\[\s*([^\]]+?)\s*\]\]') {
            $tbl = @{ Name = ($matches[1] -replace '"', ''); Values = @{} }
            [void]$result.Tables.Add($tbl); $current = $tbl.Values; continue
        }
        if ($line -match '^\[\s*([^\]]+?)\s*\]') {
            $current = @{}   # plain tables like [modproperties.x] are ignored
            continue
        }
        if ($line -notmatch '^([A-Za-z0-9_\-."]+)\s*=\s*(.*)$') { continue }
        $key = $matches[1] -replace '"', ''; $raw = $matches[2]
        $val = $null
        if ($raw.StartsWith('"""') -or $raw.StartsWith("'''")) {
            $delim = $raw.Substring(0, 3); $rest = $raw.Substring(3)
            $sb = New-Object System.Text.StringBuilder
            while ($rest.IndexOf($delim) -lt 0 -and $i + 1 -lt $lines.Count) {
                [void]$sb.AppendLine($rest); $i++; $rest = $lines[$i]
            }
            $idx = $rest.IndexOf($delim)
            if ($idx -ge 0) { [void]$sb.Append($rest.Substring(0, $idx)) } else { [void]$sb.Append($rest) }
            $val = $sb.ToString()
        } elseif ($raw -match '^"((?:[^"\\]|\\.)*)"') {
            $val = $matches[1] -replace '\\"', '"' -replace '\\\\', '\'
        } elseif ($raw -match "^'([^']*)'") {
            $val = $matches[1]
        } else {
            $val = ($raw -replace '#.*$', '').Trim()
        }
        $current[$key] = $val
    }
    return $result
}

function Read-EntryText($zip, [string]$name) {
    $e = $zip.GetEntry($name)
    if (-not $e) { return $null }
    $sr = New-Object System.IO.StreamReader($e.Open())
    try { return $sr.ReadToEnd() } finally { $sr.Dispose() }
}

function Get-ManifestVersion($zip) {
    $mf = Read-EntryText $zip 'META-INF/MANIFEST.MF'
    if ($mf -and $mf -match '(?m)^Implementation-Version:\s*(\S+)') { return $matches[1] }
    return $null
}

# ---------- scan jars ----------
$mods = New-Object System.Collections.ArrayList     # every mod entry (top-level and embedded)
$issues = New-Object System.Collections.ArrayList

function Add-Issue([string]$level, [string]$jar, [string]$msg) {
    [void]$issues.Add([pscustomobject]@{ Level = $level; Jar = $jar; Message = $msg })
}

function Read-Jar($zip, [string]$jarName, [string]$parentJar, [int]$depth) {
    $where = if ($parentJar) { "$parentJar > $jarName" } else { $jarName }
    $toml = Read-EntryText $zip 'META-INF/mods.toml'
    $neoToml = Read-EntryText $zip 'META-INF/neoforge.mods.toml'
    $hasFabric = [bool]$zip.GetEntry('fabric.mod.json')
    $hasQuilt = [bool]$zip.GetEntry('quilt.mod.json')

    if (-not $toml -and -not $parentJar) {
        $manifest = Read-EntryText $zip 'META-INF/MANIFEST.MF'
        $isService = [bool]$zip.GetEntry('META-INF/services/cpw.mods.modlauncher.api.ITransformationService')
        if ($isService -or ($manifest -and $manifest -match '(?m)^FMLModType:\s*(LIBRARY|GAMELIBRARY|LANGPROVIDER)')) {
            Add-Issue 'INFO' $where 'Loader-level jar (ModLauncher service / FML library, no mods.toml): dependencies cannot be checked.'
        }
        elseif ($neoToml) { Add-Issue 'ERROR' $where 'NeoForge-only jar (neoforge.mods.toml, no mods.toml): will not load on Forge.' }
        elseif ($hasFabric -or $hasQuilt) { Add-Issue 'ERROR' $where 'Fabric/Quilt-only jar: will not load on Forge (needs Sinytra Connector at best).' }
        else { Add-Issue 'WARN' $where 'No META-INF/mods.toml: not a Forge mod (library, resource pack or wrong file?).' }
    }

    if ($toml) {
        $t = Parse-ModsToml $toml
        $loader = $t.Top['modLoader']; $loaderVer = $t.Top['loaderVersion']
        $manifestVer = $null
        foreach ($tbl in $t.Tables) {
            if ($tbl.Name -ne 'mods') { continue }
            $v = $tbl.Values['version']
            if (-not $v -or $v -match '\$\{file\.jarVersion\}') {
                if (-not $manifestVer) { $manifestVer = Get-ManifestVersion $zip }
                $v = $manifestVer
            }
            $id = $tbl.Values['modId']
            $deps = @()
            foreach ($d in $t.Tables) {
                if ($d.Name -ne "dependencies.$id") { continue }
                $type = 'required'
                if ($d.Values.ContainsKey('type')) { $type = $d.Values['type'].ToLower() }
                elseif ($d.Values.ContainsKey('mandatory')) { $type = if ($d.Values['mandatory'] -eq 'true') { 'required' } else { 'optional' } }
                $deps += [pscustomobject]@{
                    ModId = $d.Values['modId']; Range = $d.Values['versionRange']
                    Type = $type; Side = $d.Values['side']
                }
            }
            [void]$mods.Add([pscustomobject]@{
                ModId = $id; Version = $v; Name = $tbl.Values['displayName']
                Jar = $where; TopJar = $(if ($parentJar) { $parentJar } else { $jarName })
                Embedded = [bool]$parentJar; Loader = $loader; LoaderVersion = $loaderVer; Deps = $deps
            })
        }
    }

    # jar-in-jar (Forge JarJar)
    if ($depth -lt 3) {
        foreach ($e in $zip.Entries) {
            if ($e.FullName -notlike 'META-INF/jarjar/*.jar') { continue }
            $ms = New-Object System.IO.MemoryStream
            $s = $e.Open(); try { $s.CopyTo($ms) } finally { $s.Dispose() }
            $ms.Position = 0
            $inner = New-Object System.IO.Compression.ZipArchive($ms, [System.IO.Compression.ZipArchiveMode]::Read)
            try { Read-Jar $inner $e.Name $(if ($parentJar) { $where } else { $jarName }) ($depth + 1) }
            finally { $inner.Dispose(); $ms.Dispose() }
        }
    }
}

$jars = Get-ChildItem $modsDir -File | Where-Object { $_.Extension -eq '.jar' }
$disabled = Get-ChildItem $modsDir -File | Where-Object { $_.Name -like '*.disabled' }
foreach ($j in $jars) {
    try {
        $zip = [System.IO.Compression.ZipFile]::OpenRead($j.FullName)
        try { Read-Jar $zip $j.Name $null 0 } finally { $zip.Dispose() }
    } catch {
        Add-Issue 'ERROR' $j.Name "Could not read jar: $($_.Exception.Message)"
    }
}

# ---------- build the "what is installed" index ----------
$builtin = @{ 'minecraft' = $mcVersion; 'forge' = $forgeVersion }
$byId = @{}
foreach ($m in $mods) {
    if (-not $m.ModId) { continue }
    if (-not $byId.ContainsKey($m.ModId)) { $byId[$m.ModId] = New-Object System.Collections.ArrayList }
    [void]$byId[$m.ModId].Add($m)
}

# JarJar resolves duplicates by picking the highest version; top-level jars win over embedded
function Get-Resolved([string]$id) {
    if ($builtin.ContainsKey($id)) { return [pscustomobject]@{ ModId = $id; Version = $builtin[$id]; Jar = '(built in)' } }
    if (-not $byId.ContainsKey($id)) { return $null }
    $list = $byId[$id]
    $top = @($list | Where-Object { -not $_.Embedded })
    if ($top.Count -gt 0) { return $top[0] }
    $best = $list[0]
    foreach ($m in $list) { if ((Compare-Version $m.Version $best.Version) -gt 0) { $best = $m } }
    return $best
}

# ---------- checks ----------
# duplicate top-level mod IDs
foreach ($id in $byId.Keys) {
    $top = @($byId[$id] | Where-Object { -not $_.Embedded })
    if ($top.Count -gt 1) {
        Add-Issue 'ERROR' ($top.Jar -join ', ') "Duplicate mod ID '$id' in $($top.Count) jars: Forge refuses to start."
    }
}

$knownLoaders = @('javafml', 'lowcodefml')
foreach ($m in $mods) {
    if ($m.Embedded) { continue }
    $label = if ($m.Name) { "$($m.Name) [$($m.ModId)]" } else { $m.ModId }

    if ($m.Loader -and $knownLoaders -notcontains $m.Loader) {
        if ($m.Loader -eq 'kotlinforforge' -and -not $byId.ContainsKey('kotlinforforge')) {
            Add-Issue 'ERROR' $m.Jar "$label needs Kotlin for Forge (modLoader=kotlinforforge), which is not installed."
        } elseif ($m.Loader -ne 'kotlinforforge') {
            Add-Issue 'WARN' $m.Jar "$label uses language loader '$($m.Loader)'; make sure its provider mod is installed."
        }
    } elseif ($m.LoaderVersion -and (Test-VersionInRange $forgeVersion $m.LoaderVersion) -eq $false) {
        Add-Issue 'ERROR' $m.Jar "$label needs loader $($m.Loader) $($m.LoaderVersion); instance has Forge $forgeVersion."
    }

    foreach ($d in $m.Deps) {
        if (-not $d.ModId) { continue }
        $depId = $d.ModId
        $have = Get-Resolved $depId
        $range = if ($d.Range) { $d.Range } else { '*' }
        switch -Regex ($d.Type) {
            '^(incompatible|discouraged)$' {
                if ($have -and (Test-VersionInRange $have.Version $range) -ne $false) {
                    $lvl = if ($d.Type -eq 'incompatible') { 'ERROR' } else { 'WARN' }
                    Add-Issue $lvl $m.Jar "$label is marked $($d.Type) with '$depId' $range (found $($have.Version) in $($have.Jar))."
                }
            }
            '^required$' {
                if (-not $have) {
                    if ($depId -eq 'neoforge') {
                        Add-Issue 'ERROR' $m.Jar "$label requires NeoForge $range; this instance runs Forge $forgeVersion."
                    } else {
                        Add-Issue 'ERROR' $m.Jar "$label requires '$depId' ${range}: NOT INSTALLED."
                    }
                } else {
                    $ok = Test-VersionInRange $have.Version $range
                    if ($ok -eq $false) {
                        Add-Issue 'ERROR' $m.Jar "$label requires '$depId' $range but $($have.Version) is installed ($($have.Jar))."
                    } elseif ($null -eq $ok) {
                        Add-Issue 'INFO' $m.Jar "$label requires '$depId' $range; installed version '$($have.Version)' could not be checked."
                    }
                }
            }
            default {
                if ($have) {
                    if ((Test-VersionInRange $have.Version $range) -eq $false) {
                        Add-Issue 'WARN' $m.Jar "$label optionally supports '$depId' $range but $($have.Version) is installed: Forge will refuse to start."
                    }
                } elseif ($ShowOptional) {
                    Add-Issue 'INFO' $m.Jar "$label has optional integration with '$depId' (not installed)."
                }
            }
        }
    }
}

# embedded copies that are older than what a dependency needs are covered above; flag shadowed top-level vs embedded mismatches
foreach ($id in $byId.Keys) {
    $top = @($byId[$id] | Where-Object { -not $_.Embedded })
    $emb = @($byId[$id] | Where-Object { $_.Embedded })
    if ($top.Count -eq 1 -and $emb.Count -gt 0) {
        foreach ($e in $emb) {
            if ((Compare-Version $e.Version $top[0].Version) -gt 0) {
                Add-Issue 'INFO' $top[0].Jar "'$id' $($top[0].Version) is installed, but $($e.TopJar) bundles a newer $($e.Version)."
            }
        }
    }
}

# ---------- report ----------
$out = New-Object System.Collections.ArrayList
function Say([string]$text, [string]$color = 'Gray') {
    [void]$out.Add($text)
    Write-Host $text -ForegroundColor $color
}

Say "Mod conflict check: $modsDir" 'Cyan'
Say "Minecraft $mcVersion | Forge $forgeVersion | $($jars.Count) jars | $(@($mods | Where-Object { $_.Embedded }).Count) embedded mods" 'Cyan'
if ($disabled) { Say "Disabled (ignored): $(($disabled.Name) -join ', ')" 'DarkGray' }
Say ''

if ($ListMods) {
    Say 'Installed mods:' 'Cyan'
    foreach ($m in ($mods | Sort-Object ModId)) {
        $tag = if ($m.Embedded) { "  (in $($m.TopJar))" } else { '' }
        Say ("  {0,-28} {1,-22} {2}{3}" -f $m.ModId, $m.Version, $m.Jar.Split('>')[-1].Trim(), $tag)
    }
    Say ''
}

$colors = @{ ERROR = 'Red'; WARN = 'Yellow'; INFO = 'DarkCyan' }
foreach ($lvl in 'ERROR', 'WARN', 'INFO') {
    $list = @($issues | Where-Object { $_.Level -eq $lvl } | Sort-Object Jar, Message -Unique)
    if ($list.Count -eq 0) { continue }
    Say "$lvl ($($list.Count))" $colors[$lvl]
    foreach ($i in $list) { Say "  [$($i.Jar)]  $($i.Message)" $colors[$lvl] }
    Say ''
}

$errs = @($issues | Where-Object { $_.Level -eq 'ERROR' }).Count
$warns = @($issues | Where-Object { $_.Level -eq 'WARN' }).Count
if ($errs -eq 0 -and $warns -eq 0) { Say 'No missing dependencies or version mismatches found.' 'Green' }
else { Say "$errs error(s), $warns warning(s)." $(if ($errs) { 'Red' } else { 'Yellow' }) }

if ($OutFile) {
    $path = if ([IO.Path]::IsPathRooted($OutFile)) { $OutFile } else { Join-Path $InstanceDir $OutFile }
    $out | Out-File -FilePath $path -Encoding utf8
    Write-Host "Report saved to $path" -ForegroundColor Cyan
}
exit [int]($errs -gt 0)
