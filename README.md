# colek-skills — skills de Claude para el equipo de Colek Studios

Repositorio de **distribución** de las skills de prompting y visuales de Colek para editores y colaboradores. Aquí viven las **ediciones portables** (autocontenidas, sin dependencias del ecosistema interno de Colek).

> ⚠️ **Este repo no se edita a mano.** La fuente canónica vive en el workspace del estudio; `build.ps1` regenera `skills\` desde ahí. Mejoras y correcciones → avisar al director.

> 🔒 **Todo lo que se publica aquí pasa por `sanitizar.py`.** Este repo es público, y las fichas canónicas contienen mediciones hechas sobre proyectos reales: nombres de cliente, rutas del Drive interno y costos por clip. El sanitizado sustituye cada nombre propio por su categoría —"la plantilla sellada de OBO" pasa a "la plantilla sellada de una serie de sketches"—, borra rutas y costos por su forma, y después **verifica**: si algún término interno sobrevive, el build **se detiene** y no publica nada. Arnés: `python tests_sanitizar.py`.

## Skills incluidas

| Skill | Qué hace |
|---|---|
| `media-prompting` | Experto en prompting de contenido generativo (imagen + video): dado tu requerimiento, produce el prompt optimizado para la herramienta concreta (Higgsfield, Seedance, Kling, Veo, GPT Image, Nano Banana) con la gramática de ESA herramienta. |
| `image-character-sheet` | Character sheets de personaje multi-vista (front/side/back, close-up, swatches): produce prompts listos para ChatGPT (GPT Image) y Nano Banana (Gemini) desde una ficha canónica. |

## Instalación

### Si usas Claude Code (Windows)

1. Descarga este repo (botón **Code → Download ZIP**, o `git clone` si tienes git).
2. Doble clic a **`instalar-skills.bat`** — copia las skills a tu carpeta `%USERPROFILE%\.claude\skills\`.
3. Reinicia tu sesión de Claude. Listo: Claude las usa solo cuando pidas prompts o character sheets.

**Para actualizar:** vuelve a bajar el repo (o `git pull`) y corre otra vez `instalar-skills.bat`.

### Si usas claude.ai (web o app de escritorio)

1. Descarga el ZIP de la skill que quieras desde la carpeta `zips\` de este repo.
2. En claude.ai: **Settings → Features (Capabilities) → Custom Skills → Upload skill** y sube el ZIP. *(Requiere plan de pago con code execution activado.)*
3. Repite con cada actualización (claude.ai no se sincroniza solo).

### Configura tu Claude (recomendado)

Pega el contenido de **`CLAUDE-SNIPPET.md`** en tu archivo `CLAUDE.md` global (`%USERPROFILE%\.claude\CLAUDE.md`, créalo si no existe) — le dice a tu Claude que estas skills existen, cuándo usarlas y cómo mantenerlas al día.

## Versionado

Cada skill declara su versión de edición portable en su `SKILL.md` (línea "Edición portable vAAAA-MM-DD"). Si tu resultado difiere de lo que le sale a otro editor, primero comparen versiones.
