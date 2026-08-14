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

    # ZIP para usuarios de claude.ai (la carpeta de la skill en la raiz del zip)
    $zipdir = Join-Path $repo "zips"
    New-Item -ItemType Directory -Force $zipdir | Out-Null
    $zip = Join-Path $zipdir "$s.zip"
    if (Test-Path $zip) { Remove-Item -Force $zip }
    Compress-Archive -Path $dst -DestinationPath $zip
}

Write-Host "Build OK: $($skills.Count) skills regeneradas en skills\ y zips\"
Write-Host "Siguiente paso: git add -A; git commit; git push"
