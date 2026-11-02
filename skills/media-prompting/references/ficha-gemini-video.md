---
herramienta: Gemini video understanding (Gemini API, modo agéntico y estático)
modelo-vigente: gemini-3.8-flash (agéntico también en gemini-3.7-flash, 3.6 Flash y 3.5 Flash-Lite)
dominio: video
updated: 2026-10-02
status: vigente
---

# Ficha de prompting — Gemini video understanding

> **Dominio "video" aquí es ENTENDER video, no generarlo.** Para generar video con Google es `ficha-veo.md`. Para voz, `ficha-gemini-tts.md`. Ninguna gramática se trasplanta entre ellas.

## ⚠️ Desambiguación — tres cosas que se llaman parecido

| Nombre | Qué es | Entrada |
|---|---|---|
| **Agentic Vision** (Gemini 3 Flash, ene-2026) | El modelo hace zoom, recortes y anotaciones con *code execution* antes de responder | **Imágenes**; el artículo no menciona video |
| **Agentic video understanding** (sep-2026) | El modelo recorre el video y decide qué tramo mirar, a qué fps y por qué modalidad (cuadros, audio, transcripción) | **Video** (archivo o YouTube) |
| **Static video processing** | Lectura del video a fps fijo (1 fps por defecto) | Video |

Fuentes: [blog Agentic Vision](https://blog.google/innovation-and-ai/technology/developers-tools/agentic-vision-gemini-3-flash/) y [blog agentic video](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-agentic-video-in-gemini/), leídos 2026-10-02. **Esta ficha cubre las dos últimas filas.** "Agentic video" es un **modo de procesamiento**, no un modelo: el id del modelo no cambia.

## 1. Identidad

Modelo multimodal que recibe un video con su audio y responde texto (o JSON) con referencias de tiempo. **Elegirlo** para preguntas sobre qué pasa en cuadro, en qué momento, y cruzar imagen con lo dicho. **No elegirlo** para tiempos exactos a nivel de cuadro o de borde de palabra sin verificarlos contra otra fuente: la doc habla de timestamps en `MM:SS`, no de precisión por cuadro. El modo agéntico rinde más en videos largos; en clips cortos agrega latencia (ver §5).

## 2. Gramática oficial

- **Orden de las partes:** con un solo video, **el texto va DESPUÉS del video**. *"If combining text and a single video, place the text prompt after the video part."* ([generate-content/video-understanding](https://ai.google.dev/gemini-api/docs/generate-content/video-understanding), 2026-10-02)
- **Referencias de tiempo:** formato `MM:SS` (`01:15`), en el prompt y pidiéndolo así en la respuesta. (misma fuente)
- **Activar el modo agéntico — DOS sintaxis según la API:**
  - **generateContent (REST):** en la parte del video, `"media_processing": "AGENTIC"` junto a `file_data`. (misma fuente)
  - **Interactions API:** en el input de video, `"processing": "agentic"`, o un objeto `{"type": "static", "fps": 0.5, "start_offset": <ms>, "end_offset": <ms>}` para estático con recorte. ([video-understanding](https://ai.google.dev/gemini-api/docs/video-understanding), 2026-10-02)
- **Modelos con modo agéntico:** Gemini 3.8 Flash, 3.7 Flash, 3.6 Flash y 3.5 Flash-Lite. Todos los modelos aceptan video en modo estático. (misma fuente)
- **Subida de archivo local:** Files API, subida resumible (`X-Goog-Upload-Protocol: resumable`, `start` y luego `upload, finalize`). Esperar a que el archivo quede en estado `ACTIVE` antes de usarlo. Tope por archivo: **2 GB en el tier gratuito, 20 GB en el de pago.** (ambas fuentes)
- **Límites:** hasta **10 videos por petición** (Gemini 2.5 en adelante); con ventana de contexto de 1M, videos de **hasta 3 h**. (generate-content/video-understanding)
- **Formatos:** `video/mp4`, `video/mpeg`, `video/mov`, `video/avi`, `video/x-flv`, `video/mpg`, `video/webm`, `video/wmv`, `video/3gpp`. (video-understanding)

## 3. Plantillas

**A · Decisiones de edición por línea de guion (salida JSON).**

```
You are reviewing raw camera takes for a vertical (9:16) social video.
The script lines, in order, are:
[NUMBERED_SCRIPT_LINES]

The attached videos are: [VIDEO_LIST_WITH_IDS]

For each script line, choose the best take and return JSON only:
{"lines":[{"line":<n>,"video":"<id>","in":"MM:SS.s","out":"MM:SS.s",
"why":"<one sentence>","framing_issues":["<what is wrong in frame, if anything>"]}]}

Criteria, in priority order: [CRITERIA]
Report anything in frame that is not the on-camera talent (set ceiling, lights, crew, equipment) as a framing issue, with its timestamp.
```

**B · QC de un corte terminado.**

```
This is an edited cut. List every moment where [INVARIANTS] is violated.
Return JSON only: {"issues":[{"at":"MM:SS","what":"<description>","severity":"high|low"}]}
If there are none, return {"issues":[]}.
```

## 4. Parámetros

| Campo | Valores | Nota |
|---|---|---|
| `media_processing` / `processing` | `AGENTIC` · estático (default) | Sintaxis según API, ver §2 |
| `fps` (estático) | p. ej. `0.5` | Default 1 fps |
| `media_resolution` | baja (default) · alta | Alta = más detalle, más tokens y latencia |
| `start_offset` / `end_offset` | milisegundos | Solo estático |

**Tokens (estático):** ~100 tokens por segundo de video a resolución baja, ~300 a alta; 66 o 258 tokens por cuadro, más 32 tokens por segundo de audio. En modo agéntico varía con el contenido; Google reporta "hasta 88 %" menos tokens en contenido largo. (video-understanding, 2026-10-02)

**Precio gemini-3.8-flash (tier de pago):** entrada **USD 0.75 / 1M tokens**, salida (incluye *thinking*) **USD 3.75 / 1M** hasta el 2026-12-31; **sube al doble** desde el 2027-01-01 (1.50 y 7.50). No hay recargo aparte por el modo agéntico; Batch y Flex cuestan 50 % menos. ([pricing](https://ai.google.dev/gemini-api/docs/pricing), 2026-10-02)

## 5. Gotchas documentados

- **Clips cortos (< 5 min):** el modo agéntico aumenta el tiempo hasta el primer token por su razonamiento interno; la doc recomienda estático para clips cortos sensibles a latencia. (video-understanding)
- **Conversaciones de varios turnos sin estado:** hay que conservar el `step_list` para que el modelo no pierda el contexto del video. (video-understanding)
- **La respuesta agéntica trae partes extra:** `tool_call` y `tool_response` con `tool_type: "MEDIA_PROCESSING"`. Un parser que lea solo la primera parte de texto puede romperse. (generate-content/video-understanding)
- **Salida estructurada con video:** la doc no dice si `response_schema` es compatible con el modo agéntico. **No verificado**: pedir JSON en el prompt y validarlo, o probar `response_schema` en una llamada antes de un lote.
- **YouTube en tier gratuito:** máximo 8 h de video al día. (video-understanding)

## 6. Folklore de comunidad

- Foro oficial, 2026: reporte de *"HTTP 200 then api_error after 23 processing calls"* con 3.8 Flash en modo agéntico ([discuss.ai.google.dev](https://discuss.ai.google.dev/t/gemini-3-8-flash-agentic-video-http-200-then-api-error-after-23-processing-calls/181801)). **Reproducido en casa (2026-10-04/05, torneo de visión de video): 3 de 3 llamadas agénticas terminaron con HTTP 200, `finishReason: TOO_MANY_TOOL_CALLS` tras 24 llamadas internas y SIN texto de respuesta**, en clips de 63.9 s y 103.6 s, con un prompt de edición y con uno corto de revisión. Confianza: `reproducible` para tareas con muchas preguntas sobre un clip corto. Consecuencia: para clips cortos usar el modo estático; tratar `finishReason` distinto de `STOP` como fallo.

**Medido en casa (mismo torneo), para no volver a pagarlo:**
- **El costo agéntico NO está en `promptTokenCount`**: va en `toolUsePromptTokenCount` (0.70–1.06 M tokens por llamada sobre ~100 s de video, USD 0.27–0.29 cada una aun sin respuesta), con parte cacheada en `cachedContentTokenCount`. Calcular: (prompt + toolUse − cacheado) × entrada + cacheado × caché + (candidatos + thoughts) × salida.
- **Estático ve bien y ubica mal**: detectó techo, claqueta, crew, risas y quién habla a cuadro en un sketch, pero dio entradas y salidas redondeadas al segundo y a veces desplazadas (una línea puesta sobre la repetición fallida de otra). **No usar sus tiempos para cortar sin verificarlos contra la alineación por palabra**; sí sirve como ojo de revisión.

## 7. Iteración

- Un cambio por vuelta: criterio, resolución o modo, nunca dos a la vez.
- Fijar el video subido (mismo `file_uri`) entre vueltas para comparar solo el prompt.
- Verificar los timestamps devueltos contra el material (extraer el cuadro en ese tiempo) antes de confiar en ellos para cortar.

## 8. Historial

- 2026-10-02 — creación, para el torneo de visión de video (gemini-3.8-flash, modos agéntico y estático).
