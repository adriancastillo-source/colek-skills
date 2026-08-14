# Cómo instalar las skills de Colek en tu Claude

Vas a recibir uno o dos archivos ZIP (`media-prompting.zip` y `image-character-sheet.zip`). **No los descomprimas todavía** — sigue los pasos según cómo uses Claude.

---

## Opción A — Si usas claude.ai (página web o app de escritorio)

*Requisito: cuenta de pago (Pro o Team).*

1. Guarda los ZIP en tu computadora (por ejemplo en Descargas). Déjalos como ZIP, sin descomprimir.
2. Entra a claude.ai y abre **Settings** (Configuración) — está en el menú de tu perfil, abajo a la izquierda.
3. Ve a la sección **Features** (Funciones). Si ves un interruptor de **Code execution**, actívalo.
4. Busca **Skills** → **Upload skill** (Subir skill) y selecciona `media-prompting.zip`.
5. Repite el paso 4 con `image-character-sheet.zip`.
6. Abre un chat nuevo y prueba: escribe *"¿Tienes la skill media-prompting? Dame un prompt de prueba para Kling"*. Si Claude te empieza a preguntar detalles del video, quedó instalada.

**Cuando te manden una versión nueva:** en Settings → Skills borra la skill vieja y sube el ZIP nuevo. No se actualiza sola.

---

## Opción B — Si usas Claude Code (la terminal / app de escritorio con proyectos)

1. Abre el **Explorador de archivos**, pega esto en la barra de dirección y da Enter:
   `%USERPROFILE%\.claude\skills`
   *(Si te dice que la carpeta `skills` no existe, entra a `%USERPROFILE%\.claude` y créala tú con clic derecho → Nueva carpeta → `skills`.)*
2. Clic derecho a `media-prompting.zip` → **Extraer todo…** → en la ventana que se abre, **borra la ruta sugerida** y pega `%USERPROFILE%\.claude\skills` → Extraer.
3. Repite el paso 2 con `image-character-sheet.zip`.
4. Verifica que quedó así (importante — sin carpeta doble):
   `...\.claude\skills\media-prompting\SKILL.md` ✅
   `...\.claude\skills\media-prompting\media-prompting\SKILL.md` ❌ (si te quedó así, mueve la carpeta de adentro un nivel arriba)
5. Cierra tu sesión de Claude Code y abre una nueva.
6. Prueba igual que arriba: *"¿Tienes la skill media-prompting? Dame un prompt de prueba para Kling"*.

**Extra recomendado (solo Claude Code):** pega el contenido del archivo `CLAUDE-SNIPPET.md` (te lo pasan junto con los ZIP) al final de tu archivo `%USERPROFILE%\.claude\CLAUDE.md` — si no existe, créalo como archivo de texto con ese nombre. Eso le dice a tu Claude cuándo usar las skills sin que se lo pidas.

**Cuando te manden una versión nueva:** borra la carpeta vieja (por ejemplo `skills\media-prompting`) y extrae el ZIP nuevo en el mismo lugar.

---

## Reglas de uso

- **No edites los archivos de las skills.** Se actualizan desde Colek y cualquier cambio tuyo se pierde con la siguiente versión. Si algo está mal o falta, repórtalo a Adrian.
- Al pedir un prompt, **di siempre en qué herramienta y modelo lo vas a usar** (ej. "Higgsfield con Kling") — la skill escribe distinto para cada motor.
- Si tienes una **imagen de referencia** del estilo, adjúntala: manda más que cualquier descripción.
