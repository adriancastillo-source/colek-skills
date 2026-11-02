---
herramienta: Kling AI Avatar (Kuaishou)
modelo-vigente: Avatar 2.0 (lanzado 2025-12-04) — en fal `fal-ai/kling-video/ai-avatar/v2/pro` y `/v2/standard`
dominio: video
updated: 2026-10-20
status: vigente
---

# Ficha: Kling AI Avatar 2.0 (pro)

## Identidad

Imagen + audio → video del personaje hablando, con lipsync al audio que se le da. La imagen es
también el **primer frame** del video, y el audio fija la duración. Lo que lo distingue de otros
motores de avatar: un **prompt libre de actuación** que, según la API oficial, define *"avatar
actions, emotions, and camera movements"* — o sea, a diferencia de HeyGen, aquí **sí** se dirige la
cámara y se encadenan acciones. Sirve igual con humanos, animales, caricaturas y personajes
estilizados. Elegirlo para: presentador a cámara con la locución ya sellada y gesto dirigido, tomas
de hasta 5 minutos. **No** elegirlo para: escenas con varios personajes hablando, ni para generar la
voz (la voz es entrada; hay un TTS aparte).

**Desambiguación.** No es Kling 2.x/3 de texto o imagen a video (otra ficha, otra gramática) ni el
*Lip Sync* de Kling (que re-sincroniza un video que ya existe). En la API oficial, Avatar es una
capacidad **independiente de la versión del modelo**: el *Capability Map* la lista como *"All model
versions"* y el endpoint no tiene campo de versión.

## Gramática oficial

Fuentes, consultadas **2026-10-20**:
- (A) kling.ai/document-api/api/video/avatar — referencia oficial de la API (`/v1/videos/avatar/image2video`).
- (B) kling.ai/quickstart/kling-ai-avatar-2-user-guide — *"Kling AI Avatar 2.0 User Guide"*, publicada
  **2025-12-04**, con los prompts de ejemplo oficiales.
- (C) fal.ai/models/fal-ai/kling-video/ai-avatar/v2/pro (y su `/api`) — esquema y precio en fal.
- (D) fal.ai/docs/model-api-reference/video-generation-api/kling-ai-avatar — doc de fal de los dos tiers.

### Qué va en el prompt

(A) lo define como *"Positive text prompt — Can be used to define avatar actions, emotions, and camera
movements"*, **máximo 2,500 caracteres**. En fal el campo es opcional y su default es `"."` (C).

La guía oficial (B) no da una fórmula con nombre, pero todos sus ejemplos siguen el mismo patrón,
que es la gramática de facto: **emoción/actitud → acciones en orden de ocurrencia → cámara**, en
prosa corta en inglés, con conectores de secuencia (`while`, `then`, `finally`, `occasionally`).
Ejemplos literales de (B):

- Gesto con cierre dirigido a cámara: `He raised his hand to touch his glasses and then angrily
  pointed at the camera with his finger.`
- Secuencia con remate: `Put hands together in front of your chest, and finally hold them together
  and tell a story naturally.`
- Conductor/explicación: `Professional explanations, natural movements, and sometimes use gestures to
  assist in the explanation.`
- Cámara fija: `... occasionally looking and smiling at the camera, hand on the microphone, natural
  movements on the arms, stationary shot.`
- Mano abierta a cámara: `... laughs and interacts with the camera, gesturing with open hands ...`
- Emoción en cara y cuerpo: `The man is angry, shown in both facial expression and action.`
- Movimiento de cámara: `... camera zooms in.` · `... gradually zooming in on the face.`

Lectura: **la secuencia se dirige con conectores, no con segundos.** Ningún ejemplo oficial usa
timestamps ni ata un gesto a una palabra del audio; `finally` y `then` son la forma documentada de
decir "al final".

### Imagen y audio (A)

- Imagen: `.jpg / .jpeg / .png`, **≤ 10 MB, lado ≥ 300 px, proporción entre 1:2.5 y 2.5:1**. URL o
  Base64 **sin** prefijo `data:image/...`.
- Audio (`sound_file`): `.mp3 / .wav / .m4a / .aac`, **≤ 5 MB, entre 2 y 300 s**. O `audio_id` de su
  TTS (generado en los últimos 30 días). Excluyentes.
- En fal se aceptan además JPG/PNG/WebP/GIF/AVIF y MP3/OGG/WAV/M4A/AAC; fal **no publica** límites de
  duración ni de tamaño (C, D).

### Duración

La salida dura lo que el audio (C, D). La guía oficial (B) anuncia *"full coverage for 5-minute-long
content scenes"*, coherente con el tope de 300 s de (A).

## Plantillas

En inglés, prosa corta. `[SLOTS]` entre corchetes.

### A — Presentador a cámara (gesto + remate)

```
[ATTITUDE / EMOTION], [ROLE] speaks directly to the camera with [DELIVERY QUALITY].
[OPENING GESTURE] while talking, [OCCASIONAL SECONDARY MOVEMENT], and finally [CLOSING GESTURE at the camera].
[Stationary shot | CAMERA MOVE].
```

### B — Actuación emocional (sin gesto preciso)

```
[EMOTION], shown in both facial expression and action. [ONE OR TWO NATURAL MOVEMENTS]. [CAMERA].
```

### C — Caso de uso: conductor de capacitación sobre croma, ~11 s, español mexicano

**Insumos:** foto en plano medio sobre verde liso (será el primer frame: el encuadre y el fondo se
heredan de ella) · locución de ~11 s en español mexicano · endpoint `.../ai-avatar/v2/pro`.

```json
{
  "image_url": "[IMAGE_URL — medium shot, flat chroma-green backdrop]",
  "audio_url": "[AUDIO_URL — ~11 s Mexican Spanish voiceover]",
  "prompt": "Energetic and upbeat, a corporate training host speaks directly to the camera with a confident smile. At the start he opens his right hand palm-up toward the camera in a welcoming gesture, keeps natural, lively arm movements while talking, and finally points his index finger straight at the camera on the last sentence. The plain green background stays flat and unchanged. Stationary shot."
}
```

- `finally ... on the last sentence` es la forma más cercana a la documentada de pedir "al final";
  la parte *"on the last sentence"* **no** tiene respaldo oficial (ver Gotchas).
- `The plain green background stays flat and unchanged` no está en la guía: es descripción positiva
  de lo que debe permanecer, para que el modelo no invente sombras o fondo. No medido.

## Parámetros

- **API oficial (A):** `POST https://api-singapore.klingai.com/v1/videos/avatar/image2video`;
  campos `image`, `sound_file` | `audio_id`, `prompt`, `mode` (`std` default | `pro`),
  `watermark_info`, `callback_url`, `external_task_id`. Consulta: `GET .../image2video/{task_id}`.
  ⚠️ Los videos generados **se borran a los 30 días** (A).
- **fal (C, D):** `image_url` (req.), `audio_url` (req.), `prompt` (opcional, default `"."`),
  `enable_safety_checker`. Salida: `video` + `duration` (float, s). No hay campos de resolución,
  ratio ni duración.
- **Ratio:** no hay campo; la imagen es el primer frame (B), así que el ratio sale de la imagen
  (inferencia, no documentado como regla).
- **Resolución:** **no documentada** en (A), (C) ni (D). Un comunicado de lanzamiento del producto
  Avatar (2025-09-19, reproducido por barchart.com) habla de *"up to 1080p"* y 48 FPS: es anterior a
  Avatar 2.0 y de segunda mano.
- **Precio:** fal **<costo interno>** pro y **<costo interno>** standard (C, D; 2026-10-20). Oficial: **8
  créditos/s** Professional y **4 créditos/s** Standard, redondeado al segundo, mínimo 2 s (B).

## Gotchas documentados

- **No hay control temporal fino.** Ni (A) ni (B) documentan atar un gesto a una palabra o a un
  segundo. `then` / `finally` ordenan; no sincronizan.
- **Idiomas listados: inglés, japonés, coreano y chino** (B, sección *Multilingual Support*). El
  español **no aparece**. Como el lipsync es al audio dado debería funcionar, pero no hay
  confirmación oficial: medir antes de comprometerlo.
- **Imagen fuera de rango → error**: menos de 300 px, más de 10 MB o proporción fuera de 1:2.5–2.5:1
  (A). Un 9:16 (1:1.78) entra; un 1:3 no.
- **Audio > 5 MB → error en la API oficial** (A): un WAV de 11 s entra; un WAV largo puede no entrar
  aunque dure menos de 300 s. Exportar a MP3 si se va por la API directa.
- El sistema *"will verify audio content"* y puede rechazarlo con código de error (A).

## Folklore de comunidad

- Plantilla `role, emotion, gestures, pace, camera` (ej. *"confident news anchor, medium close-up,
  subtle hand gestures, steady pace"*) — post de Higgsfield del 2025-09-13. `anecdótico`: es la
  envoltura de Higgsfield; coincide en espíritu con los ejemplos de (B) pero no es gramática de Kling.
- *"Use the text prompt to explicitly guide the avatar's emotional delivery, specific gestures, and
  camera movements"* — página del modelo en hedra.com. `reproducible` en cuanto a que repite lo que
  dice (A); la redacción es de Hedra.
- Prompts con negativos (*"No distortions"*, *"No cars passing by"*) aparecen en un ejemplo de
  creador incluido en (B), no en la descripción del campo, que habla de *"positive text prompt"* (A).
  `anecdótico`: no hay campo de negativos y la API llama "positivo" al prompt.

## Iteración

Fijar imagen y audio; mover una sola cláusula del prompt por corrida, en este orden: (1) el gesto de
cierre, (2) la intensidad de la actitud, (3) la cámara. Si el gesto final no aparece, primero
simplificar a dos acciones con `then` / `finally` (el patrón de los ejemplos oficiales) antes de
agregar adjetivos.

## Historial

- 2026-10-20 — alta de la ficha (Avatar 2.0, endpoint v2/pro de fal y API oficial
  `/v1/videos/avatar/image2video`). Motivada por un plano de conductor de capacitación sobre croma.
