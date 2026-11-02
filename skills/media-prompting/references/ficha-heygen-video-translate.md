---
herramienta: HeyGen Video Translate (API v3)
modelo-vigente: Video Translation v3 (`POST /v3/video-translations`), modos `speed` (default) y `precision`
dominio: video
updated: 2026-10-29
status: vigente
---

# Ficha: HeyGen Video Translate (API v3)

## Identidad

Doblaje de un video **ya hecho** en un solo paso: transcribe, traduce, clona la voz del hablante,
genera el audio traducido y, salvo que se pida solo audio, redibuja la boca con su motor de lipsync.
**No hay prompt que redactar**: la "gramática" es el cuerpo JSON (video fuente + idiomas + modo +
perillas). Elegirlo para: talking head frontal, un hablante, entregar en varios idiomas a la vez
conservando la voz. **No** elegirlo para: personajes sin cara humana detectable (ver Gotchas), voz
nueva escrita a mano (eso es el Lipsync API con audio propio), ni fuentes sin habla.

**Desambiguación.** Video Translate ≠ **Lipsync API** (`/v3/lipsyncs`): los dos usan el mismo motor
de lipsync, pero Lipsync solo cambia la boca sobre un audio que tú traes, sin traducir (A). Tampoco
es **Avatar IV** (`POST /v3/videos`, genera un video nuevo desde foto + audio): sus reglas, su límite
de cara y su precio son de otro endpoint.

## Gramática oficial

Fuentes, todas consultadas **2026-10-29** salvo donde se indica:
- (A) developers.heygen.com/docs/video-translate — guía, modo Speed.
- (B) developers.heygen.com/docs/video-translation-precision — guía, modo Precision.
- (C) developers.heygen.com/reference/create-video-translation — esquema OpenAPI de `POST /v3/video-translations`.
- (D) developers.heygen.com/reference/get-video-translation — esquema de `GET /v3/video-translations/{id}`.
- (E) developers.heygen.com/reference/list-supported-translation-languages — más la respuesta real del
  endpoint leída con una llave de cuenta el 2026-10-29 (190 idiomas).
- (F) developers.heygen.com/docs/usage-limits — concurrencia y límites.
- (G) developers.heygen.com/docs/upload-assets — subida de archivos.
- (H) developers.heygen.com/user-profile — `GET /v3/users/me` (saldo).
- (I) developers.heygen.com/docs/pricing.md — **instantánea de web.archive.org del 2026-06-13**; la URL
  viva responde 404 el 2026-10-29 y la tarifa vigente vive en el dashboard (platform.heygen.com/pricing,
  que solo carga con JavaScript).
- (J) developers.heygen.com/skills/heygen-translate — skill oficial de HeyGen para agentes (guía de uso,
  no referencia de API).
- (K) github.com/heygen-com/skills, `heygen-translate/references/troubleshooting.md`, commit `1bd5e4d`
  del 2026-07-14 — repositorio oficial de HeyGen; ya no está en la rama principal.
- (L) help.heygen.com/en/articles/10029081 — *Video Translation 101*, centro de ayuda de la **app web**
  (créditos de plan, no API). Sin fecha visible.

### Autenticación y base

`https://api.heygen.com`, cabecera `x-api-key` (C). Cuerpo JSON, `additionalProperties: false`: un
campo desconocido se rechaza (C). Cabecera opcional `Idempotency-Key` (1-255 caracteres
`[A-Za-z0-9_:.-]`): un reintento en 24 h con la misma llave repite la respuesta original sin crear otro
trabajo; si el original sigue en vuelo devuelve `409 request_in_progress` (C).

### El ciclo: crear → consultar → descargar

1. **Crear:** `POST /v3/video-translations` → `data.video_translation_ids[]`, **un id por idioma** (A, C).
2. **Consultar:** `GET /v3/video-translations/{video_translation_id}` → `data.status` en
   `pending | running | completed | failed` (A). Alternativa: `callback_url` + `callback_id` (webhook) (C).
3. **Descargar:** con `completed`, `data.video_url` (video traducido) y `data.audio_url` (audio
   traducido aparte) son **URLs presignadas** (D). Subtítulos `srt_caption_url` y `vtt_caption_url`: se
   generan siempre, pero el campo **se omite** (no llega `null`) si aún no existe — leer con chequeo de
   presencia (A). Con `failed`: `failure_message` y, a veces, `failure_code` (D).

### Campos de `POST /v3/video-translations` (C)

Obligatorios: `video` y `output_languages`.

| Campo | Tipo / default | Qué hace |
|---|---|---|
| `video` | `{type:"url", url}` o `{type:"asset_id", asset_id}` | Fuente. La URL debe ser pública (A) |
| `output_languages` | `string[]`, mín. 1 | **Nombres** de idioma tal cual los da el endpoint de idiomas, no códigos ISO |
| `mode` | `"speed"` (default) \| `"precision"` | Precision usa *avatar inference*: más lento, mejor lipsync (B) |
| `translate_audio_only` | `false` | `true` = solo audio traducido, boca intacta; en Precision anula su ventaja (B) |
| `speaker_num` | `null` (auto) | Número de hablantes. (B): "especialmente importante en Precision" |
| `enable_dynamic_duration` | `true` | Deja que la duración de salida varíe al ritmo natural del idioma. **No cambia el cobro**, que siempre es por la duración de la fuente (A, B) |
| `input_language` | `null` (auto) | "Source language code"; el formato exacto no está documentado |
| `keep_the_same_format` | `null` | Conserva resolución y bitrate de la fuente |
| `disable_music_track` | `false` | Quita la música de fondo |
| `enable_speech_enhancement` | `false` | Mejora el audio de la voz |
| `brand_glossary_id` | `null` | Glosario: `do_not_translate_terms` y `forced_translations` en todos los idiomas. `brand_voice_id` es el nombre viejo, deprecado (A, C) |
| `audio` | `null` | Audio propio para el doblaje (`url` o `asset_id`) |
| `srt` / `srt_role` | `null` | Subtítulo propio, `input` u `output`. **Solo Enterprise** (B) |
| `stock_voice_config` | `null` | Voz de catálogo en lugar del clon. **Solo Enterprise**, por solicitud (A) |
| `start_time` / `end_time` | `null` | Traducir solo un tramo (segundos) |
| `fps_mode` | `null` | `vfr \| cfr \| passthrough`; solo actúa con `audio` propio |
| `title`, `folder_id`, `callback_url`, `callback_id`, `enable_watermark` | — | Administración |
| `enable_caption` | — | Deprecado e ignorado |

### Idiomas: nombres exactos

`GET /v3/video-translations/languages` → `data.languages[]` (E). Leído con llave el 2026-10-29 (190 nombres):
- Español de México: **`Spanish (Mexico)`** (existen además `Spanish`, `Spanish (Latin America)`, `Spanish (Spain)` y otras 18 variantes).
- Chino mandarín: **`Chinese (Mandarin, Simplified)`** (existe también un `Mandarin` a secas, sin documentar en qué difiere, y `Chinese (Taiwanese Mandarin, Traditional)`).
- Francés: **`French (France)`** (existen `French`, `French (Canada)`, `French (Belgium)`, `French (Switzerland)`).

(J) advierte que las variantes regionales sí cambian el resultado: *Spanish (Spain) ≠ Spanish (Mexico)*.

### Speed vs Precision (A, B)

| | Speed | Precision |
|---|---|---|
| Tiempo | Más rápido | Más lento; sondear cada 30-60 s (B) |
| Traducción | "Adequate" | "Context- and Gender-Aware" |
| Lipsync | Estándar | Alto |
| Para | Caras con poco movimiento, borradores | Caras con mucho movimiento, ángulos laterales, oclusiones; entrega final |

(J) recomienda Precision por default salvo que se pida velocidad.

### Entrada: subir el archivo

Por URL pública, o subiendo antes con `POST /v3/assets` (`multipart/form-data`, campo `file`, tope
**32 MB**; el MIME se detecta por los bytes) → `data.asset_id` (G). Más de 32 MB: flujo de subida directa
`POST /v3/assets/direct-uploads`, hasta 200 MB por video (G). Formatos de video: MP4, WebM (G).

### Saldo sin gastar

`GET /v3/users/me` devuelve `billing_type` y, con llave de API, `wallet.remaining_balance` en USD (H).
Gratis; sirve de preflight. El endpoint heredado `GET /v2/user/remaining_quota` responde con otra unidad
(cuota), no con dólares.

## Plantillas

No hay texto de prompt: lo que se redacta es el cuerpo. Los `[SLOTS]` se llenan; lo demás es literal.

### A — Doblaje con lipsync a varios idiomas (una llamada, un id por idioma)

```json
{
  "video": { "type": "url", "url": "[PUBLIC_MP4_URL]" },
  "output_languages": ["[LANGUAGE NAME 1]", "[LANGUAGE NAME 2]"],
  "mode": "[speed | precision]",
  "speaker_num": [N_SPEAKERS],
  "title": "[JOB TITLE]"
}
```

### B — Solo audio traducido (para montarlo con otro lipsync)

```json
{
  "video": { "type": "asset_id", "asset_id": "[ASSET_ID]" },
  "output_languages": ["[LANGUAGE NAME]"],
  "translate_audio_only": true,
  "speaker_num": 1
}
```

Se lee `audio_url` del resultado (D).

### C — Caso de uso: clip de avatar 3D en inglés, ~28 s, 9:16 720x1280, un hablante → es-MX, mandarín, francés

**Insumos:** el MP4 tal cual salió (por URL pública o subido a `/v3/assets`; un clip de 28 s a 720p
debería quedar bajo 32 MB). Una llamada por modo; cada llamada devuelve 3 ids.

```json
{
  "video": { "type": "asset_id", "asset_id": "[ASSET_ID — 28 s EN avatar clip, 720x1280]" },
  "output_languages": ["Spanish (Mexico)", "Chinese (Mandarin, Simplified)", "French (France)"],
  "mode": "precision",
  "speaker_num": 1,
  "keep_the_same_format": true,
  "title": "[CHARACTER] EN to ES-MX/ZH/FR precision"
}
```

- `speaker_num: 1` explícito: (B) y (J) lo señalan como la palanca de calidad más importante.
- `keep_the_same_format: true` para no salir con otra resolución que la del clip; **sin medir** si
  respeta el 9:16.
- `enable_dynamic_duration` se deja en su default `true`: en→zh sale ~30 % más corto según (J), y sin
  él el mandarín suena lento. Consecuencia: **los tres videos no durarán 28 s** — si el montaje exige
  duración fija, correr una variante con `false` y compararla.
- Para el lado Speed del mismo torneo, cambiar solo `"mode": "speed"`.

## Parámetros

- **Concurrencia (F):** pay-as-you-go 10 flujos simultáneos (avatar + traducciones + Video Agent
  cuentan juntos); Enterprise 20. Exceder → `429` con `Retry-After`.
- **Lotes:** `POST /v3/video-translations/batches`, hasta 100 cargas por llamada (índice oficial de la doc).
- **Tiempo de render:** 10-20 min por idioma según (J) — orientativo, no SLA.
- **Duración / tamaño máximos por API:** **no publicados** en la referencia de API. La ayuda de la app
  web (L) da de 2 s a 30 min (Creator/Pro), 60 min (Business) o 5 h (Enterprise), y hasta 5 GB; eso
  es la app, no la API.
- **Salida:** MP4 con video traducido + audio aparte + SRT + VTT (D). Resolución: la ayuda de la app
  (L) limita la exportación por plan (gratis 720p, Creator 1080p, 4K desde Pro si la fuente lo es); en
  la API no está documentado.
- **Precio (I, instantánea del 2026-06-13 de la página oficial, hoy fuera de línea):** cobrado en USD
  por segundo, **sobre la duración de la fuente** (A, B):

  | Modo | Tarifa | Por minuto | Clip de 28 s, por idioma | 28 s × 3 idiomas |
  |---|---|---|---|---|
  | Speed — solo audio | <costo interno> | ≈ <costo interno> | ≈ <costo interno> | ≈ <costo interno> |
  | Speed — lipsync | <costo interno> | ≈ <costo interno> | ≈ <costo interno> | ≈ <costo interno> |
  | Precision — lipsync | <costo interno> | ≈ <costo interno> | ≈ <costo interno> | ≈ <costo interno> |

  La misma instantánea dice que el **proofread es solo Enterprise**; las guías vivas (A, B) lo
  documentan sin esa restricción. ⚠️ **No verificado al 2026-10-29:** una guía de multilingual-content
  citada por buscadores y varias fuentes secundarias dan **Precision a <costo interno>** (<costo interno>/min; <costo interno> por
  idioma en 28 s); la página viva de esa guía ya no trae la cifra. Antes de presupuestar, leer el
  dashboard. El "<costo interno>/min Precision" que circulaba en fuentes secundarias coincide con (I).
- **Créditos de plan web (L):** solo audio 4, Speed 6, Precision 10 créditos por minuto. **No aplica**
  a llamadas con llave de API, que descuentan de la cartera en USD (H, I).

## Gotchas documentados

- **Cara no detectada → falla el lipsync.** (K): `failed` con `failure_message: "lip-sync"` significa
  *"Face was not detected or detection was unstable"*; salida documentada: reenviar con
  `translate_audio_only: true`. Ninguna página oficial dice si acepta caras de animación 3D o no
  humanas. **Antecedente propio:** el 2026-09-04 (torneo T-2026-09-04-una mascota 3D-por-plano) HeyGen rechazó
  la imagen de una mascota no humanoide (hocico de pico, ojos muy separados) con
  `400 invalid_parameter: "No face detected in the image"`, en plano medio y en primer plano, mismo
  error; un personaje humanoide estilizado sí pasó. Eso fue **Avatar IV**, no Video Translate: el
  detector de este endpoint no está medido. Riesgo alto para un personaje con barba larga que tapa la
  boca o con cara de animal; riesgo menor para un humano estilo cartoon.
- **La fuente es el techo** (J): audio sucio, cortes rápidos, oclusión de la cara o resolución baja
  degradan el lipsync y la voz. Funciona mejor con planos frontales, estables, bien iluminados, ≥720p.
- **Fuente sin habla audible o animación muda:** falla en ~30 s; (K) dice que para animación, b-roll o
  fuentes mudas esta herramienta es la equivocada.
- **URL no pública:** falla casi al instante con *"Failed to download video from url…"* (K).
- **`speaker_num` mal puesto** es *"the #1 quality killer"*: las voces se cruzan entre hablantes (J).
- **Saldo que se acaba a medio trabajo:** una traducción rechazada al cobrar falla por la vía normal
  con el código de estado `400837`, sin código propio (doc de errores en el índice oficial completo).
  Hacer preflight con `GET /v3/users/me` antes de lanzar.
- **Subtítulos ausentes ≠ `null`:** el campo simplemente no viene (A).
- **Pedir varios idiomas en una llamada crea N trabajos cobrables**, uno por idioma (A, J).

## Folklore de comunidad

- Caras de cartoon o de render 3D con ojos grandes reciben *"No face detected"* — hilos del foro de
  docs.heygen.com (discuss), sin fecha legible en el resumen; se refieren a subir foto para avatar, no
  a Video Translate. `anecdótico`.
- Speed para hablantes frontales simples, Precision para perfiles y oclusiones; Precision cuesta el
  doble en créditos — reseñas de terceros 2026 (seedance.tv, fluxnote.io). `reproducible` en lo que
  coincide con (A, B); las tarifas citadas ahí no concuerdan entre sí.

## Iteración

No hay texto que afinar: se cambia **un campo por corrida** con la misma fuente. Orden útil: `mode`
(speed → precision) → `speaker_num` → `enable_dynamic_duration` → `enable_speech_enhancement`. La
fuente y los nombres de idioma son invariantes; si cambia la fuente, ya no se compara el modo. Para
corregir la traducción sin volver a pagar el render, el flujo de proofread (crear sesión → bajar SRT →
editar → subir → `.../generate`) existe en (A, B), con la duda de plan señalada en Parámetros.

## Historial

- 2026-10-29 — alta de la ficha (Video Translation API v3, modos speed y precision). Motivada por el
  competidor D del Torneo DOBLAJE + LIPSYNC 2026-10. Precio solo verificable en una instantánea
  archivada de la página oficial; detección de caras no humanas sin medir en este endpoint.
