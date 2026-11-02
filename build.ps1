# build.ps1 - regenera skills\ y zips\ desde la fuente canonica del workspace de Colek.
# Uso (lado Adrian, no editores):  powershell -ExecutionPolicy Bypass -File build.ps1
# Regla: este repo NO se edita a mano; toda correccion va a la fuente y se re-corre el build.
#
# Rutas (escision fase 3, H:\Mi unidad\EXIO\escision\DISENO-RUTAS.md): la fuente sale de
# la casa de Adrian, variable de usuario EXIO_CASA_ADRIAN (+ '\skills'). Sin ella, el build
# se detiene: nunca cae a una ruta escrita a mano.
#   -Src      fuente de las skills (por omision: <EXIO_CASA_ADRIAN>\skills)
#   -Destino  donde se escriben skills\ y zips\ (por omision: este repo). Las pruebas y las
#             corridas en seco lo apuntan a una carpeta temporal para no tocar lo versionado.
param(
    [string]$Src = "",
    [string]$Destino = ""
)

$ErrorActionPreference = "Stop"

# Lector de casas (DISENO-RUTAS.md 1.3). En el cuerpo y no en param(): con
# `powershell -File` (tarea agendada) las variables automaticas llegan vacias ahi.
function Get-Casa([string]$Cual) {
    $var = @{ adrian = 'EXIO_CASA_ADRIAN'; estudio = 'EXIO_CASA_ESTUDIO' }[$Cual]
    $v = [Environment]::GetEnvironmentVariable($var)
    if (-not $v -or -not (Test-Path -LiteralPath $v -PathType Container)) { throw "Falta $var o no existe (ver DISENO-RUTAS.md)" }
    $v
}

$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $Src) { $Src = Join-Path (Get-Casa adrian) 'skills' }
if (-not $Destino) { $Destino = $repo }
Write-Host "Fuente:  $src"
Write-Host "Destino: $Destino"

# skill => tiene edicion portable en <skill>\portable\SKILL.md; references viajan tal cual
$skills = @("media-prompting", "image-character-sheet")

foreach ($s in $skills) {
    $dst = Join-Path $Destino "skills\$s"
    if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
    New-Item -ItemType Directory -Force (Join-Path $dst "references") | Out-Null

    Copy-Item (Join-Path $src "$s\portable\SKILL.md") (Join-Path $dst "SKILL.md")
    Copy-Item (Join-Path $src "$s\references\*.md") (Join-Path $dst "references\")
    # docs internos de mantenimiento y tumbas de consolidacion no viajan a los editores
    Remove-Item (Join-Path $dst "references\metodo-ficha.md") -ErrorAction SilentlyContinue
    Remove-Item (Join-Path $dst "references\ficha-infinitalk.md") -ErrorAction SilentlyContinue

    # SANITIZADO (2026-09-05). El repo destino es PUBLICO en GitHub y hasta hoy las
    # fichas viajaban tal cual: cada medicion nueva se hizo sobre un proyecto real y
    # con ella entraron nombres de cliente, rutas del Drive y costos por clip. Cuatro
    # fichas ya publicadas nombraban clientes cuando se detecto.
    # `sanitizar.py` sustituye los nombres por su categoria y ABORTA si algo sobrevive:
    # es preferible un build detenido a un cliente publicado.
    Write-Host "  sanitizando $s ..."
    & python (Join-Path $repo "sanitizar.py") (Join-Path $dst "references")
    if ($LASTEXITCODE -ne 0) {
        throw "SANITIZADO FALLIDO en '$s': quedaron terminos internos. NO se publica nada."
    }
    # El SKILL.md portable pasa por el mismo filtro que sus fichas.
    $tmpSkill = Join-Path $dst "_skillmd"
    New-Item -ItemType Directory -Force $tmpSkill | Out-Null
    Copy-Item (Join-Path $dst "SKILL.md") (Join-Path $tmpSkill "SKILL.md")
    & python (Join-Path $repo "sanitizar.py") $tmpSkill
    if ($LASTEXITCODE -ne 0) { throw "SANITIZADO FALLIDO en el SKILL.md de '$s'." }
    Copy-Item (Join-Path $tmpSkill "SKILL.md") (Join-Path $dst "SKILL.md") -Force
    Remove-Item -Recurse -Force $tmpSkill

    # ZIP para usuarios de claude.ai (carpeta de la skill en la raiz del zip).
    # tar de Windows (bsdtar) y no Compress-Archive: PS 5.1 mete backslashes en los
    # entry names y los extractores POSIX (claude.ai) extraen plano.
    $zipdir = Join-Path $Destino "zips"
    New-Item -ItemType Directory -Force $zipdir | Out-Null
    $zip = Join-Path $zipdir "$s.zip"
    if (Test-Path $zip) { Remove-Item -Force $zip }
    tar -a -c -f $zip -C (Join-Path $Destino "skills") $s
    if ($LASTEXITCODE -ne 0) { throw "tar fallo para $s" }
}

Write-Host "Build OK: $($skills.Count) skills regeneradas en $Destino (skills\ y zips\)"
Write-Host "Siguiente paso: git add -A; git commit; git push"
