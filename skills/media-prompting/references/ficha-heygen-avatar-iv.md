---
herramienta: HeyGen (API v3)
modelo-vigente: Avatar IV (motor por defecto de `POST /v3/videos`; Avatar V y Avatar III conviven como opt-in)
dominio: video
updated: 2026-10-20
status: vigente
---

# Ficha: HeyGen Avatar IV (API v3)

## Identidad

Motor de avatar parlante de HeyGen: una foto (o un avatar registrado) + un audio o un guion → video
de la persona hablando con lipsync. Lo que lo distingue en la API v3 es que **acepta una imagen
cualquiera** (`type: "image"`, sin dar de alta un avatar) y expone dos perillas de actuación:
`motion_prompt` (gesto en lenguaje natural) y `expressiveness` (`high | medium | low`). Elegirlo para:
presentador a cámara con la locución ya sellada (el audio entra tal cual y manda la duración),
largos de minutos, salida 1080p. **No** elegirlo para: caminar, pararse, mover la cámara, cambiar de
lugar o tocar objetos — la propia guía de HeyGen los excluye del `motion_prompt` (ver Gramática).

**Desambiguación.** En la misma API conviven tres motores: **Avatar IV** (el de esta ficha, default),
**Avatar V** (mayor fidelidad, solo `digital_twin`, sin `expressiveness`, sin imagen arbitraria) y
**Avatar III** (foto a video, 4K, sin `motion_prompt`). Además existe `cinematic_avatar`, otro `type`
con prompt de escena de hasta 10,000 caracteres y duración 4-15 s: **no es Avatar IV** y no se rige
por esta ficha.

## Gramática oficial

Fuentes, todas consultadas **2026-10-20**:
- (A) developers.heygen.com/avatar-iv — página del motor.
- (B) developers.heygen.com/reference/create-video — esquema de `POST /v3/videos`.
- (C) developers.heygen.com/models — comparativa III / IV / V.
- (D) developers.heygen.com/photo-avatar — requisitos de foto y ejemplos de `motion_prompt`.
- (E) developers.heygen.com/audio-to-video — audio propio como fuente del lipsync.
- (F) help.heygen.com/en/articles/12805098 — *"Fine-tune avatar gestures and movements with custom
  motion prompts (Avatar IV & V)"*, el artículo de ayuda con la gramática del gesto. Sin fecha de
  actualización visible.
- (G) developers.heygen.com/docs/usage-limits — límites de entrada.

### El prompt no es un prompt de escena: es UNA instrucción de gesto

`motion_prompt` es un string en lenguaje natural que *"controls body motion and hand gestures"* (A).
No describe al personaje, ni el fondo, ni la cámara: la imagen ya fija todo eso. La fórmula
documentada (F):

> **`[Body part] + [Action] + [Emotion or intensity]`** — ejemplo oficial:
> `Right arm raises in a wave, enthusiastic and friendly.`

Reglas de la misma fuente (F):
- **Un gesto por prompt**, *"under two clauses"*. Una secuencia corta de dos tiempos sí aparece como
  ejemplo válido: `Avatar nods confidently, then points forward`. Una cadena de cuatro gestos
  (saludar, cruzar brazos, señalar, encoger hombros) aparece como **mal ejemplo**.
- **No se escriben segundos ni velocidad**: el ritmo lo pone el sistema. **No hay forma documentada
  de atar un gesto a una palabra del audio.**
- Verbos visibles: *point, nod, turn, wave, smile*. La emoción puede ir en el mismo prompt
  (`smiles gently`, `looks surprised`).
- Otros ejemplos oficiales: `Avatar smiles softly while raising a hand` (F) · `nodding gently` y
  `gesturing with hands while presenting` (D) · `walk towards the camera slowly` (A, ver Gotchas).

### Lo que el `motion_prompt` NO controla (F, lista *"What you can NOT control here"*)

Movimiento de cámara (*zoom, pan, dolly*) · cambiar de lugar o escena · props y acciones con objetos
(beber café) · **pararse o caminar** · fondo o iluminación.

### El techo de 10 segundos del gesto

> *"Custom motion generation has a maximum duration of 10 seconds"* — y después *"the motion will be
> generated for the first 10 seconds and then loop or hold for the remainder"* (F).

Para tomas largas la guía recomienda dejar el movimiento por defecto en la mayor parte y usar gestos
cortos solo donde se quiere énfasis (F). Con Avatar IV *"you can adjust motion scene by scene"* (F):
la unidad de control es la escena, no el segundo.

### `expressiveness`

`high | medium | low`; **default `low`** si se omite (A, B). Solo con fotos/imagen arbitraria y solo
en Avatar IV (en Avatar V se rechaza) (B). La documentación **no define** qué cambia entre niveles
más allá del nombre (*"controls energy and range of movement"*, A).

### La imagen

- Debe tener **una cara humana claramente visible**; sin cara detectable → `400`. Personajes no
  humanos van por otra ruta (`/v3/models/videos`) (B).
- PNG o JPEG; frontal, bien iluminada, expresión neutra (D).
- Evitar: lentes de sol, sombreros que tapen la frente, ángulos de cámara extremos (D).

### El audio manda la duración

No hay campo `duration` en `type: "image"`: el largo lo da el audio o el guion (B). Audio propio por
`audio_url` (URL pública) o `audio_asset_id` (subido a `/v3/assets`), **excluyentes con `script`** (B, E).
Subida: MP3 o WAV, hasta 32 MB (E).

## Plantillas

`motion_prompt` va en inglés y en una sola oración. Los `[SLOTS]` se llenan; lo demás es literal.

### A — Presentador a cámara con un gesto de énfasis

```
[BODY PART] [ACTION toward/at the camera], [EMOTION or INTENSITY].
```

### B — Dos tiempos (gesto de apertura → gesto de cierre)

```
[Avatar / Both hands] [FIRST ACTION], [EMOTION], then [SECOND ACTION].
```

### C — Caso de uso: conductor de capacitación sobre croma, ~11 s, español mexicano

**Insumos:** foto en plano medio de la persona **ya sobre verde liso** (la cara frontal, manos visibles
en cuadro si se quiere que gesticule) · locución `.wav` de ~11 s en español mexicano · `aspect_ratio`
del proyecto · `resolution: "1080p"`.

```json
{
  "type": "image",
  "image": { "type": "url", "url": "[IMAGE_URL — medium shot, flat chroma-green backdrop]" },
  "audio_url": "[AUDIO_URL — ~11 s Mexican Spanish voiceover]",
  "motion_prompt": "Right hand opens palm-up toward the camera, energetic and confident, then points forward at the camera.",
  "expressiveness": "high",
  "resolution": "1080p",
  "aspect_ratio": "[16:9 | 9:16 | auto]"
}
```

- La cámara fija **no se pide**: el `motion_prompt` no controla cámara (F); el plano lo hereda de la foto.
- El fondo verde viene **de la foto**. Alternativa documentada: `background: {"type":"color","value":"#00B140"}`
  con `remove_background: true` (B) — no medido si el recorte del fondo deja borde.
- ⚠️ **El "señala en la frase final" no es controlable:** no hay sincronía gesto-palabra documentada,
  y en 11 s el último segundo cae fuera de la ventana de 10 s del gesto (F). Si el señalamiento debe
  caer en la última frase, partir la locución en dos llamadas — cuerpo con gesto A
  (`Right hand opens palm-up toward the camera, energetic and welcoming.`) y frase final con
  `Right index finger points straight at the camera, decisive and energetic.` — y cortar en montaje.

## Parámetros

Todo de (B) salvo donde se indica; consultado 2026-10-20.

- **Endpoint:** `POST /v3/videos` → `video_id`; se consulta con `GET /v3/videos/{video_id}` hasta
  `completed` (A). Webhook opcional: `callback_url` + `callback_id`.
- **`type: "image"`** + `image` como `{url}`, `{asset_id}` o `{base64, media_type, data}`. No lleva
  `avatar_id` ni `engine`.
- **Voz:** `audio_url` | `audio_asset_id` | (`script` + `voice_id`). `voice_settings` (speed 0.5-1.5,
  pitch −50..50, volume 0-1, `locale`) solo afecta a voz sintetizada.
- **`resolution`:** `1080p` | `720p` (`4k` solo Avatar III digital twin / studio).
- **`aspect_ratio`:** `16:9` (default) · `9:16` · `4:5` · `5:4` · `1:1` · `auto` (recomendado por (E)
  para conservar el de la imagen). **`fit`:** `contain` | `cover`.
- **`output_format`:** `mp4` (default) | `webm` (fondo transparente; exige avatar con *matting* y
  rechaza `background`). Que `webm` funcione con `type: "image"` **no está confirmado**.
- **`caption`:** siempre devuelve un `.srt` aparte.
- El cuerpo rechaza campos desconocidos (`additionalProperties: false`).
- **Límites de entrada (G):** guion 5,000 caracteres; audio 10 min (600 s). ⚠️ (E) dice 30 min por
  petición: las dos páginas oficiales se contradicen; usar el menor.
- **Concurrencia (G):** pay-as-you-go 10 flujos simultáneos; `POST /v3/videos` 10/s.
- **Precio:** **no publicado** en la documentación pública; vive en el dashboard de la cuenta (G).

## Gotchas documentados

- **Caminar: la documentación se contradice.** (A) pone como único ejemplo
  `walk towards the camera slowly`; (F) lista *"Standing up or walking around"* entre lo que NO se
  controla. Tratar caminar como no soportado hasta medirlo.
- **`motion_prompt` con `type: "image"`: otra contradicción.** (A), (B) y (C) dicen que funciona con
  imagen arbitraria; la página developers.heygen.com/image-to-video (consultada 2026-10-20) dice que
  image-to-video *"does not support motion prompts or expressiveness"* y que hay que crear un Photo
  Avatar (`POST /v3/avatars`) para tenerlos. Si el gesto no aparece, la primera sospecha es esta: dar
  de alta el Photo Avatar y repetir con `type: "avatar"`.
- **Más de un gesto por prompt degrada** (F): se repite, se cicla o se ignora.
- **Después de 10 s el gesto se repite o se congela** (F).
- **Idioma del lipsync:** la API no publica lista de idiomas (E). El audio manda, pero no hay
  confirmación oficial para español.

## Folklore de comunidad

- *"Keep gesture prompts short to avoid looping or overuse"* y prompts de una o dos palabras
  (`waving`, `sipping coffee`) — recap del webinar de producto de junio 2025 en community.heygen.com,
  que llama *beta* a la función. `anecdótico`; además `sipping coffee` choca con la exclusión de props
  de (F), que es más reciente.
- *"Expressive audio helps because motion is driven by voice"* — página de onboarding de Avatar IV en
  heygen.com/academy. `reproducible` en cuanto a la arquitectura (el motor es audio-driven), pero sin
  medición.
- La Academy dice que el campo Custom Motion trae presets para Avatar IV; (F) dice que los presets
  (Expression / Gesture / Gaze) son de Avatar V. `anecdótico`; manda (F).

## Iteración

Cambiar **una sola cosa** por corrida: primero el verbo del gesto, después la intensidad
(`expressiveness`), al final la emoción. La guía lo dice así: *"minor edits can make a large
difference"* — simplificar a una acción antes de agregar (F). La imagen y el audio son invariantes:
si cambian, ya no se compara el prompt.

## Historial

- 2026-10-20 — alta de la ficha (Avatar IV en API v3). Motivada por un plano de conductor de
  capacitación sobre croma; trae dos contradicciones de la documentación oficial sin resolver
  (caminar; `motion_prompt` con `type: "image"`).
