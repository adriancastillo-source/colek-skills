---
herramienta: MiniMax H3 (Hailuo)
modelo-vigente: MiniMax-H3 (API desde 2026-07-31; pesos abiertos en Hugging Face) · variante MiniMax-H3-Max (fal)
dominio: video
updated: 2026-10-30
status: vigente
---

# Ficha: MiniMax H3

## Identidad

Modelo **omni-modal** de MiniMax: un Transformer denso de **33B parámetros** (≈13B en ramas AdaLN)
que entiende texto, imagen, video y audio, y genera **video con audio estéreo nativo en una sola
pasada** — voz, efectos y música salen del mismo modelo (github.com/MiniMax-AI/MiniMax-H3, README,
consultado 2026-10-20). Tomas de **4 a 15 s**. Elegirlo para: tomas cortas donde el personaje habla
**y la voz la genera el modelo** a partir del texto, con hasta 9 imágenes de referencia; diálogo en
11 idiomas, español incluido. **No** elegirlo para: lipsync a una locución ya sellada (no está
documentado como su modo principal, ver Gotchas), ni tomas de más de 15 s.

**Su gramática es un FORMATO ESTRUCTURADO, no prosa libre ni brackets por canal.** El modelo fue
entrenado sobre una representación intermedia (*Context-IR*) con campos con nombre
(`integrated_multimodal_description:`, `overall_soundscape:`, `non_diegetic_music:`), hablantes con
ID `(S1)` y diálogo entre tokens `<d>…</d>`. No trasplantar los `{ }` de Seedance ni el orden por
capas de Wan.

**H3 Max** es otra cosa: *"post-trained by fal.ai on MiniMax H3 and optimized for faster
generation"*, solo 480P/768P y 5-15 s (platform.minimax.io/docs/guides/video-generation, 2026-10-20).
Esta ficha es de H3; ver la nota de H3 Max en Parámetros.

## En el motor: `avatar-h3` (avatar a cámara sobre croma)

**Para un avatar que habla a cámara sobre croma, no se escribe el prompt a mano ni con un script suelto.**
Se usa el CLI del AVE, que lleva esta gramática y los gotchas de abajo ya cosidos:
`python <ruta interna> <subcomando>`. Contrato, flujo y
umbrales: `<ruta interna>`.

- `voz`: ElevenLabs por tramo, gate palabra por palabra y atempo.
- `logo` y `ancla`: logo oficial en la ropa del cuadro inicial, y el video quieto de 3 s que va como `<Video 1>`.
- `prompts`: un prompt por tramo. El personaje, la voz y el croma son datos del proyecto en `avatar.json`. La duración sale del audio + 1.5 s.
- `solicitudes`: los `params` de `generate_video` para el MCP de Higgsfield. La subida y el gasto siguen por MCP.
- `revisar`: mide fondo, cabeza, cola muda, guion y voz de cada toma, y deja una hoja de 8 cuadros para mirarla.
- `fondo`: recolorea el azul apagado al estándar.
- `empalmar`: si la imagen de una toma salió bien pero H3 dijo mal el guion, pone encima la voz limpia y re-cronometra la imagen, sin pagar otra toma. Así van TP-03, TP-06 y TP-11 en el V5 de un proyecto de avatar (2026-11-02).

Sus prompts reproducen byte a byte los que se pagaron en un proyecto de avatar (16 de 16 tramos comparados, 2026-10-30).
Si un gotcha nuevo cambia la gramática, se corrige en `plantilla_h3()` del CLI y aquí, en el mismo cambio.

## Gramática oficial

Fuentes, todas consultadas **2026-10-20**:
- (A) github.com/MiniMax-AI/MiniMax-H3 — README (specs, idiomas, ejemplo de Context-IR).
- (B) huggingface.co/MiniMaxAI/MiniMax-H3 — model card (mismo contenido que A) y sus guías:
  `docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md` (T2VA / I2VA / FL2VA / L2VA) y
  `docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md` (modo referencia, Ref2VA). Son idénticas a
  `skills/h3-prompt-writing/references/base-en.txt` y `ref-en.txt` del GitHub.
- (C) platform.minimax.io/docs/guides/video-generation — API hospedada de MiniMax.
- (D) fal.ai/models/minimax/h3/reference-to-video/api y fal.ai/models/minimax/h3/image-to-video/api.
- (E) fal.ai/learn/devs/minimax-h3-prompting-guide — guía de fal, publicada 2026-07-31.

### Estructura del prompt (B, guía base §2)

Modo **I2VA** (imagen = primer frame), que es el del caso de uso:

```
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...
```

- La **primera línea es literal** y va seguida de una línea en blanco (B §2.1).
- `integrated_multimodal_description` es el cuerpo: estilo y composición al abrir `[Shot 1]`, luego
  acciones, hablantes, diálogo y sonido diegético **en orden de reproducción** (B §4.1).
- I2VA se escribe así: *first-frame anchor → action onset → continuous development → result or
  reaction*, conservando identidad, ropa, colores y relaciones espaciales de la imagen (B §3.1).
- `overall_soundscape`: 1-4 oraciones de ambiente y sonidos físicos, **sin repetir el diálogo**;
  `N/A` solo si se pide silencio total (B §4.6).
- `non_diegetic_music`: 1-3 oraciones de instrumentación y tempo, o `N/A` (B §4.7).
- El modo referencia (Ref2VA) usa **seis** secciones en otro orden: `subject_definitions`,
  `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`,
  `non_diegetic_music`; el cuerpo mide normalmente **350-500 palabras en inglés**, salvo que el
  diálogo pida más (B, guía ref §1 y §5.2).

### Diálogo: `<d>[Idioma] …</d>` y hablantes `(S1)` (B §4.4)

Sintaxis literal, ejemplos oficiales:

```
The young woman with a quiet, breathy voice (S1) says: <d>[English] I get off at the next station.</d>
The two children (S1,S2) shout together, <d>[English] Wait for us!</d>
The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d> while his lips remain completely closed.
```

Reglas (B §4.4):
- **Dentro de `<d>` solo van la etiqueta de idioma y las palabras**, verbatim, sin traducir. Todo lo
  demás —quién habla, su ID, la acción, la entrega— va **fuera**.
- La **primera vez** que aparece un hablante se describe para fijar identidad: tipo, edad, género,
  si está en cuadro, **tono, timbre, velocidad y acento**. El acento va aquí, no en la etiqueta.
- ID estable por hablante `(S1)`, `(S2)`; compuesto `(S1,S2)` si hablan a la vez; quien no habla no
  lleva ID.
- `<scenetrans>` si una línea cruza un corte; `<cutoff>` si el video la trunca al final.
- `<d>` es un **token especial del tokenizer** (A): por eso la sintaxis es literal y no admite
  variantes.

**Español:** la lista oficial de idiomas estables es *"Arabic, Chinese, English, French, German,
Italian, Japanese, Korean, Portuguese, Russian, and Spanish"* (A). La forma de la etiqueta es
`<d>[Language] …</d>` (B, guía ref §5.1) y el único ejemplo literal es `[English]`; por lo tanto la
etiqueta para español es **`<d>[Spanish] …</d>`** (derivado del nombre en la lista; **no hay ejemplo
oficial en español**). No existe etiqueta de dialecto: "mexicano" se dice en la descripción del
hablante (`a Mexican Spanish accent`).

### Audio de referencia: timbre o copia, según se declare (B, guía ref §2.4, §4.2, §5.4)

- Como **ancla de timbre**: `<Audio 1> is the voice-timbre reference for <Subject 1> (S1).` y en
  `retention_analysis`: `<Audio 1>: reference - the target speaker follows <Audio 1>'s voice timbre
  and measured delivery without copying the original signal.`
- Regla: *"When only timbre, rhythm, emotion, or delivery is referenced, do not carry the original
  dialogue from the reference audio into the target video."* — **las palabras salen del `<d>`, no del
  audio.**
- Como **copia**: `<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete
  final audio track.` Existe en la gramática; su lipsync no está medido (ver Gotchas).

### Cámara: frase natural, no etiquetas (B §4.3)

Vocabulario: `Zoom In/Out` · `Push In / Pull Out` · `Pan Left/Right` · `Truck Left/Right` ·
`Tilt Up/Down` · `Pedestal Up/Down` · `Arc Shot` · `Tracking Shot` · **`Static Shot`** ·
`Shake Slightly/Strongly` · `POV` · `Roll`. Modificadores opcionales `with small|large amplitude`,
`at slow|fast speed`. Se escribe **dentro de la oración**, *"rather than stacked as separate labels
at the end of a sentence"*: `The camera holds a static shot as the runner exits the frame.`

⚠️ La doc de la API hospedada (C) sugiere en cambio agregar `[pan]`, `[zoom]` o `[static]` *"directly
after key descriptions"*, y solo da esos tres. Son dos capas distintas: (B) es la gramática del modelo;
(C) es un atajo de la plataforma, que reescribe el prompt con su Context-IR antes de generar. Esta
ficha usa (B).

### Tomas y cortes (B §4.2)

`[Shot 1]` **sin** timestamp; las siguientes empiezan con `[Shot N] At MM:SS.mmm, the camera cuts to…`,
tiempos estrictamente crecientes dentro de la duración. Un corte debe traer información nueva; si solo
cambia la distancia, mejor un movimiento de cámara. **Dentro de una toma no hay timestamps**: los
gestos se ordenan por su relación con las líneas (`As he delivers the line, …` es el patrón del
ejemplo oficial de A).

## Plantillas

⚠️ Los slots van como `[[SLOT]]` (doble corchete) porque los corchetes simples son sintaxis literal
del modelo (`[Shot 1]`, `[Spanish]`). Todo lo que no está en `[[ ]]` se copia tal cual; para otro
idioma se cambia `Spanish` por su nombre en inglés de la lista oficial.

### A — I2VA: persona a cámara con diálogo generado

```
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] [[STYLE: Live-action]], a [[FRAMING]] frames the [[PERSON: 2-3 visible traits]] shown in <Picture 1>, preserving [[his/her]] appearance, clothing, position and the [[SETTING]]. The camera holds a static shot throughout. The [[SPEAKER: age, gender, pitch, timbre, speaking rate, accent]] (S1) [[OPENING ACTION]] and says: <d>[Spanish] [[LINE 1]]</d> [[CONTINUOUS ACTION]] as [[he/she]] continues: <d>[Spanish] [[LINE 2]]</d> As [[he/she]] delivers the final line, [[CLOSING ACTION]]: <d>[Spanish] [[FINAL LINE]]</d> Exactly as [[his/her]] voice stops, [[END STATE]], and the camera holds the static shot through the end of the video.

overall_soundscape: [[AMBIENCE + PHYSICAL SOUNDS, 1-4 sentences, no dialogue]]

non_diegetic_music: [[N/A | instrumentation + tempo]]
```

### B — Caso de uso: conductor de capacitación sobre croma, ~11 s, español mexicano

**Insumos:** foto en plano medio de la persona sobre verde liso como primer frame (`image_url` en fal
`minimax/h3/image-to-video`) · `duration: 11` · `resolution: "768P"` (nativo) · el ratio sale de la
imagen. Las líneas en español deben caber en 11 s; la guía prioriza que quepa el diálogo completo.

```
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Live-action, a medium shot frames the [[PERSON: e.g. man in his thirties with short dark hair and a navy polo shirt]] shown in <Picture 1>, standing in front of a flat, evenly lit chroma-green backdrop, preserving his appearance, clothing, position and the plain green background. The camera holds a static shot throughout. Looking directly into the camera lens, the energetic corporate training host with a bright, mid-pitched voice, a brisk speaking rate and a Mexican Spanish accent (S1) opens his right hand palm-up toward the camera in a welcoming gesture and says: <d>[Spanish] [[LINE 1]]</d> He keeps lively, natural arm movements and a confident smile as he continues: <d>[Spanish] [[LINE 2]]</d> As he delivers the final line, he points his index finger straight at the camera: <d>[Spanish] [[FINAL LINE]]</d> Exactly as his voice stops, his lips close into a confident smile while his finger stays pointed at the lens, and the camera holds the static shot through the end of the video.

overall_soundscape: A quiet, dry studio room tone with the faint rustle of fabric as the host moves his arms.

non_diegetic_music: N/A
```

### C — Variante con la voz de una persona real (Ref2VA, timbre)

Endpoint `minimax/h3/reference-to-video`, imagen como `reference_image_urls[0]`, un clip limpio de
2-15 s de la voz como `reference_audio_urls[0]`. Las secciones son las de Ref2VA (ver Gramática);
lo esencial:

```
subject_definitions:
<Subject 1> is the [[PERSON: visible traits]] from <Picture 1>, standing in front of a flat chroma-green backdrop.
<Picture 1> is the first frame of the target video.
<Audio 1> is the voice-timbre reference for <Subject 1> (S1).

summary:
[keyframe completion + audio reference] [[ONE-SENTENCE SUMMARY]]

retention_analysis:
<Picture 1>: fully_preserved - [[what stays: identity, clothing, framing, green backdrop]].
<Audio 1>: reference - the target speaker follows <Audio 1>'s voice timbre without copying the original signal.

detailed_description:
The target video is live-action with flat, even studio lighting.
[Shot 1] The shot begins from <Picture 1>. [[... same body as Template B, with "<Subject 1> (S1)" as the speaker and "with his voice timbre referencing <Audio 1>" ...]]

overall_soundscape: [[...]]

non_diegetic_music: N/A
```

## Parámetros

- **API hospedada (C):** modelo `MiniMax-H3`; `POST https://api.minimax.io/v2/video_generation`,
  consulta `GET /v2/query/video_generation/{task_id}`. Duración **4-15 s, enteros**; resolución
  **768P / 2K**; prompt **≤ 7,000 caracteres**; `ratio` obligatorio en texto-a-video (sin
  `adaptive`), `adaptive` en imagen-a-video. Imágenes 256-5760 px por lado, proporción 2:5 a 5:2.
  Archivos: video ≤ 50 MB, imagen ≤ 30 MB, audio ≤ 15 MB (WAV, MP3). Existe una tarea
  `task_type=h3_context_ir` que devuelve **solo el prompt reescrito**, sin video: útil para ver cómo
  la plataforma estructura un prompt antes de pagar la generación.
- **Referencias (A, C, D):** hasta **9 imágenes**, **3 videos** (2-15 s c/u, ≤ 15 s en total),
  **3 audios** (2-15 s c/u, ≤ 15 s en total), máximo **12 archivos** combinados.
- **Salida (A):** 24 FPS, audio 32 kHz estéreo; lado corto 768 px por defecto. 2K/4K son
  **regeneración/upscale de una base 768P** (A, D).
- **fal `minimax/h3/image-to-video` (D):** `prompt`, `image_url` (primer frame), `end_image_url`,
  `duration` (entero, default 5), `resolution` (`480P` | `768P` | `2K` | `4K`; **default `2K`**),
  `seed`, `prompt_expansion_mode` (`disabled` | `fast` | `balanced` default | `quality`),
  `target_audio_url` (ver Gotchas). La salida trae `expanded_prompt`: leerlo siempre que algo salga raro.
- **fal `minimax/h3/reference-to-video` (D):** `reference_image_urls`, `reference_video_urls`,
  `reference_audio_urls` (se citan como `Image 1`, `Video 1`, `Audio 1`), `aspect_ratio`
  (`adaptive` default, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16`).
- **Precio fal reference-to-video (D, 2026-10-20):** 480p **<costo interno>** · 768p **<costo interno>** · 2K
  **<costo interno>** · 4K **<costo interno>**; las 5 primeras imágenes de referencia gratis, cada extra <costo interno>. La
  página de image-to-video no publica precio. Ojo: el default de fal es 2K, más del doble que 768P.
- **H3 Max:** 480P/768P, 5-15 s (C). Endpoints de fal `minimax/h3-max/text-to-video`,
  `minimax/h3-max/image-to-video`, `minimax/h3-max/reframe-video` y
  `minimax/h3-max/reference-director` (E y listado de fal; no se leyó el esquema de cada uno). Precio
  de lista reportado <costo interno> 480p y <costo interno> 768p tras una promoción que terminó el 1 de septiembre —
  **dato de segunda mano** (búsqueda 2026-10-20), no verificado en la página de precios de fal.

## Gotchas documentados

- **`target_audio_url` no es lipsync.** En fal image-to-video el audio *"replaces the output
  soundtrack, padded with silence if shorter than the video, without changing playback speed"*;
  si es más largo se recorta (D). La página **no dice** que la boca se sincronice a ese audio. Para
  una locución sellada, H3 no es el motor documentado: usar uno audio-driven.
- **Sin el Context-IR la calidad cae.** El README: *"H3-Context-IR is critical to the quality of the
  final output"* (A). Si se manda prosa libre, dejar `prompt_expansion_mode` encendido (la
  plataforma la reescribe); si se manda el formato estructurado de esta ficha, la reescritura
  podría duplicarse — el ejemplo de fal usa `disabled` (D), pero **no está medido cuál conviene**.
- **Etiquetas de referencia en dos dialectos:** fal pide `Image 1` / `Audio 1` en texto plano (D);
  la guía del modelo usa `<Picture 1>`, `<Subject 1>`, `<Audio 1>` (B). Mezclarlos en un mismo prompt
  no está documentado.
- **Duración:** H3 4-15 s (A, C); H3 Max 5-15 s (C); la guía de fal dice 5-15 s para sus endpoints
  (E). Un plano de 4 s puede fallar en fal.
- **Guía de fal sin `<d>`:** (E) escribe el diálogo en prosa con comillas (*The character says:
  "…"*) y la clonación como *"Match the voice in Audio 1"*. Funciona porque la plataforma reescribe,
  pero no es la gramática del modelo: no usarla como fuente de sintaxis.
- **Moderación automática** de texto, imágenes, videos y prompts reescritos, con falsos positivos
  reconocidos (A).
- **Medido en el estudio (torneo AVATAR CANALES, 2026-10-20; `<ruta interna>`):**
  - **Higgsfield no deja fijar la imagen como primer cuadro si hay voz.** `start_image` junto con
    `audio_references` responde 422, sin cobro: *"start_image/end_image cannot be mixed with reference
    media"*. La imagen entra como `image_references` y **H3 puede cambiar el fondo** (inventó una pared
    de logos, una oficina y fondos oscuros de estudio).
  - **Lo que ancla el fondo y el encuadre:** un video de 3 s de la misma imagen quieta como
    `video_references`, declarado en el prompt como `<Video 1>` de fondo y encuadre. Con eso, croma azul
    2 de 2 al primer intento.
  - **Color del croma:** verde y azul se sostienen; **magenta liso no** (1 de 5 intentos). Si la ropa es
    verde, croma azul con jeans oscuros. Al recortar magenta, los labios se transparentan si la tolerancia
    es amplia.
  - **El estilo del prompt tiene que coincidir con la imagen.** Pedir «photorealistic» para un personaje
    semirrealista coincidió con los fondos que derivaban.
  - **La voz de referencia se copia, pero no siempre igual:** correlación de envolvente contra la
    original de 0.56 a 0.99 según la toma, y una toma se comió una palabra. Oír y transcribir cada toma.
  - **Costo en Higgsfield 2K:** 2 créditos por segundo (`get_cost`: 20 por 10 s, 30 por 15 s).
- **Medido en producción: una promocion de refrescos, avatar Pixar 9:16 sobre croma azul, 11 tomas (2026-10-21).**
  Se pagaron 24 tomas para quedarse con 11. Al primer intento sirvieron 7 de 11. Fallas: 7 de fondo,
  1 de encuadre, 1 palabra trabada y 1 toma corta (recuento sobre los archivos de
  `<ruta interna>` y su `TEMP BORRAR`, más las
  variantes no subidas en `<ruta interna>`).
  - **Las palabras del `summary` se vuelven escenografía.** Con «about the una marca de refrescos loyalty lottery» metió
    vasos y botellas de una marca de refrescos al fondo. Con «to a small shop owner» armó una tienda completa. El
    `summary` describe solo al hablante y el croma: *«A friendly host stands in front of a blue
    chroma-key screen and talks directly to the camera»*. La marca que va dentro de `<d>` no estorbó.
  - **Pasa aunque haya video de referencia:** 4 de 24 tomas cambiaron el azul por azul marino con
    viñeta, y una por un azul más apagado que no se recorta con la misma llave. Hay que medir el borde de
    cada toma, no revisarlo a ojo.
  - **Puede cerrar el encuadre** y cortar la cabeza aunque el cuadro inicial sea abierto. Ayudó pedir
    *«camera locked off… no zoom and no push-in»*.
  - **Duración de la toma: audio del tramo + ~1.5 s**, y pedir *«holds the static shot for about one
    second»*. Con +0.8 s, la voz llegó al último cuadro y el montador no pudo cortar limpio.
  - **En 9:16, Nano Banana no achica la figura en el cuadro inicial:** se le da aire por código
    (escalar anclada abajo y rellenar con el azul medido).

- **Medido en la prueba de avatar en ingles (un personaje recurrente y otro conductor en inglés, 9:16, 8 tomas, 2026-10-29):**
  - **H3 re-actúa la voz más lento que la referencia** y mete pausas propias de 0.6 a 2 s entre frases (aun con la referencia ya apretada estilo tiktok). Se resuelve en el montaje: recortar cada pausa de más de 0.35 s a 0.20 s con corte en salto (`<ruta interna>`; promoverlo si se reusa).
  - **Repite o cambia palabras** aunque la referencia diga bien el guion: «partners, partners» y «first player» por «first play». Transcribir CADA toma palabra por palabra; una repetición se quita en el corte.
  - **Fondo azul marino con viñeta: 1 de 8 tomas**, aun con video ancla. Se caza midiendo el azul del primer cuadro (`[0,15,51]` contra `[0,121,251]`).

## Folklore de comunidad

- La cita *"Exact speech content comes from the text, not the audio clip"* circula atribuida a la
  documentación oficial, pero **no aparece** en el README, el model card ni las dos guías (búsqueda
  literal en los cuatro archivos, 2026-10-20). Lo que sí dice la guía es la regla de §5.4 citada en
  Gramática, que significa lo mismo. Citar esa, no la otra.
- Una reseña de terceros aparecida en búsqueda web (2026-10-20) reporta audio "speech-like garbage"
  cuando el prompt no trae dirección de audio y no se leyó la guía — `anecdótico`, pero coherente con
  la regla de B de describir al hablante y poner las palabras en `<d>`.
- *"Mexican Spanish accent"* en la descripción del hablante como forma de fijar el dialecto —
  `reproducible` en cuanto a que B lista el acento entre los rasgos del hablante; **sin medición** de
  que el modelo distinga variantes del español.

## Iteración

Invariantes: la primera línea I2VA, la descripción del hablante en su primera aparición (rasgos de
voz incluidos) y el texto dentro de `<d>`. Se cambia **una cosa por corrida**, en este orden: el gesto
atado a la línea, la descripción de la voz, la cámara. Antes de pagar una corrida a 2K, iterar a 768P
(es la base de la que sale el 2K) y, si se va por la API de MiniMax, pedir primero la tarea
`h3_context_ir` para ver cómo quedó el prompt reescrito.

## Historial

- 2026-10-20 — alta de la ficha (MiniMax H3, API desde 2026-07-31; nota de H3 Max). Motivada por un
  plano de conductor de capacitación sobre croma. Corrige dos supuestos previos: los tags `[pan]`
  `[zoom]` `[static]` son atajo de la API hospedada, no gramática del modelo; y el audio de referencia
  puede ser timbre **o** copia, según se declare.
- 2026-10-20 (noche) — gotchas medidos en el torneo AVATAR CANALES: sin primer cuadro fijo con voz en
  Higgsfield, ancla de fondo con video de referencia, croma azul sí y magenta no, costo por segundo.
- 2026-10-21 — gotchas de producción (una promocion de refrescos, 11 tomas 9:16): el `summary` se vuelve
  escenografía, el fondo se pierde aun con video de referencia, el encuadre se cierra, y la duración
  necesita colchón.
- 2026-10-30 — el flujo de avatar sobre croma se gradúa al CLI `avatar-h3` del AVE (sección «En el
  motor»), tras correrlo a mano en una promocion de refrescos, otros dos proyectos.
