# build.ps1 - regenera skills\ y zips\ desde la fuente canonica del workspace de Colek.
# Uso (lado Adrian, no editores):  powershell -ExecutionPolicy Bypass -File build.ps1
# Regla: este repo NO se edita a mano; toda correccion va a la fuente y se re-corre el build.

$ErrorActionPreference = "Stop"
$src  = "G:\Mi unidad\CLAUDE WORKSPACE\skills"
$repo = Split-Path -Parent $MyInvocation.MyCommand.Path

# skill => tiene edicion portable en <skill>\portable\SKILL.md; references viajan tal cual
$skills = @("media-prompting", "image-character-sheet")

foreach ($s in $skills) {
    $dst = Join-Path $repo "skills\$s"
    if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
    New-Item -ItemType Directory -Force (Join-Path $dst "references") | Out-Null

    Copy-Item (Join-Path $src "$s\portable\SKILL.md") (Join-Path $dst "SKILL.md")
    Copy-Item (Join-Path $src "$s\references\*.md") (Join-Path $dst "references\")
    # docs internos de mantenimiento no viajan a los editores
    Remove-Item (Join-Path $dst "references\metodo-ficha.md") -ErrorAction SilentlyContinue

    # ZIP para usuarios de claude.ai (carpeta de la skill en la raiz del zip).
    # tar de Windows (bsdtar) y no Compress-Archive: PS 5.1 mete backslashes en los
    # entry names y los extractores POSIX (claude.ai) extraen plano.
    $zipdir = Join-Path $repo "zips"
    New-Item -ItemType Directory -Force $zipdir | Out-Null
    $zip = Join-Path $zipdir "$s.zip"
    if (Test-Path $zip) { Remove-Item -Force $zip }
    tar -a -c -f $zip -C (Join-Path $repo "skills") $s
    if ($LASTEXITCODE -ne 0) { throw "tar fallo para $s" }
}

Write-Host "Build OK: $($skills.Count) skills regeneradas en skills\ y zips\"
Write-Host "Siguiente paso: git add -A; git commit; git push"
