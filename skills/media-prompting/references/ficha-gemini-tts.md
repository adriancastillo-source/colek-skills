---
herramienta: Gemini TTS (Gemini API speech generation)
modelo-vigente: gemini-3.8-flash-tts y gemini-3.8-flash-lite-tts (GA, 2026-09-23) · gemini-3.1-flash-tts-preview (preview; el de las recetas en producción a 2026-10-01)
dominio: voz
updated: 2026-10-06
status: vigente
---

# Ficha de prompting — Gemini TTS

## ⚠️ Desambiguación — 3.8 y 3.1 son GRAMÁTICAS DISTINTAS

Misma familia, mismo catálogo de 30 voces, **pero el prompt se arma al revés**. Esta ficha tiene dos partes: **Parte A = 3.8** (abajo) y **Parte B = 3.1 preview** (§2 en adelante, la que rige las recetas selladas). **No se trasplanta un prompt de una a la otra.**

| | **3.8 Flash / Flash-Lite TTS** (Parte A) | **3.1 Flash TTS preview** (Parte B) |
|---|---|---|
| Dónde va la dirección | En un campo aparte: `speech_metadata.style`, por turno | **Dentro del mismo texto** (Director's Notes + TRANSCRIPT) |
| Qué es el `text` | *"strictly as a verbatim transcript"* — todo lo que va ahí se considera guion | Prompt + guion mezclados |
| Etiquetas inline | **Ángulo**: `<sigh>`, `<laugh>`, `<short pause>` — solo eventos puntuales | **Corchete**: `[sighs]`, `[whispers]`, `[very fast]`, también estados sostenidos |
| Idioma | Detección automática; no hay `languageCode` documentado | `languageCode` en `speechConfig` |
| Salida por defecto | WAV con cabecera RIFF, 24 kHz mono 16-bit | PCM crudo (L16) sin cabecera |
| Voz propia | Diseño de voz (descripción) y réplica de voz (audio + audio de consentimiento) | No existen |
| Estado | GA | Preview, id mutable |

Fuente: [ai.google.dev/gemini-api/docs/speech-generation](https://ai.google.dev/gemini-api/docs/speech-generation) y [ai.google.dev/gemini-api/docs/generate-content/speech-generation](https://ai.google.dev/gemini-api/docs/generate-content/speech-generation), leídas 2026-10-01 (sección de migración desde 3.1).

> **Consecuencia directa:** una receta escrita para 3.1 (persona + notas de director + `#### TRANSCRIPT` en el texto) **no es un prompt de 3.8 con otro id**. Mandada tal cual, el modelo la recibe como transcript literal. Que la lea en voz alta es la hipótesis obvia, **no está verificada** (la doc no dice qué pasa; ver A6).

---

# PARTE A — Gemini 3.8 Flash TTS / Flash-Lite TTS

## A1. Identidad

Sucesor GA del 3.1 preview (lanzado 2026-09-23, [blog.google/…/gemini-3-8-text-to-speech](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-text-to-speech/), leído 2026-10-01). Separa **guion** (`text`, literal) de **dirección** (`style`, corta) y mueve la identidad del personaje a la **voz** (prebuilt, diseñada o replicada) en lugar de a un bloque largo de persona. Oficial: *"Use Gemini 3.8 Flash TTS when maximum acoustic fidelity, nuanced acting, and expressive control are top priority"*; Flash-Lite para *"high-volume bulk production, conversational voice agents"* (speech-generation, 2026-10-01). Elegirlo cuando se quiera salir del preview o bajar costo; no asumir que una receta de 3.1 suena igual sin probar.

## A2. Gramática oficial

Fuentes (todas leídas 2026-10-01): [speech-generation](https://ai.google.dev/gemini-api/docs/speech-generation) (Interactions API) · [generate-content/speech-generation](https://ai.google.dev/gemini-api/docs/generate-content/speech-generation) (generateContent) · [models/gemini-3.8-flash-tts](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-tts) · [voice-design](https://ai.google.dev/gemini-api/docs/voice-design) · [voice-replication](https://ai.google.dev/gemini-api/docs/voice-replication) · [api/voices](https://ai.google.dev/api/voices).

- **Ids:** `gemini-3.8-flash-tts` · `gemini-3.8-flash-lite-tts`. Estado GA. Límites del modelo Flash: **8,192 tokens de entrada, 16,384 de salida** (página del modelo).
- **Dos puertas de API, misma gramática:**
  - **generateContent** — `speech_metadata` es anotación **a nivel de part**, junto al `text`; `responseModalities: ["AUDIO"]` y `speechConfig` en `generationConfig`. Ejemplo oficial (REST): `parts: [{ text: "Have a wonderful day!", speech_metadata: { style: "cheerful and friendly" } }]`, `speechConfig: { voiceConfig: { voice: "Kore" } }`. ⚠️ El nombre del campo de voz en el ejemplo es `voiceConfig.voice`, no el `prebuiltVoiceConfig.voiceName` de 3.1: **confirmarlo en la primera llamada** (leído vía resumen de la página, no copiado del código fuente).
  - **Interactions API** — `POST /v1beta/interactions`, `content[].annotations[{type: "speech_metadata", style}]`, `generation_config.speech_config: [{voice}]`, `response_format: {type: "audio"}`.
- **El texto es transcript literal.** Cita: *"Gemini 3.8 TTS treats input text strictly as a verbatim transcript."* Migración oficial: *"Move sustained acting, tone, prosody, and pacing instructions … out of plain text and into `speech_metadata.style`. Keep `text` strictly as the verbatim transcript."*
- **`style` = dirección sostenida del turno** (emoción, prosodia, ritmo, volumen). Ejemplos oficiales: `"cheerful and friendly"`, `"whispered urgently"`, `"out of breath"`, `"casual, friendly"`, `"muttering, then reassuring"`. **Corta**: *"Add a concise `style` string … only for turns that need a specific delivery adjustment, and reuse that exact short string across turns."* Límite de longitud del `style`: **no documentado**.
- **Flujo recomendado oficial (4 pasos):** (1) crear el personaje con diseño de voz o elegir una voz regional de la Extended Voice Library; (2) escribir el texto como transcript hablado real, con disfluencias; (3) **sintetizar primero con `style` vacío** — *"most requests need no style instruction at all"*; (4) agregar `style` solo donde haga falta.
- **Persona: en la voz, no en bloques de estilo.** Cita: *"Design personas upfront in Voice design instead of long style blocks."* Evitar re-enviar la descripción del personaje en cada turno.
- **Etiquetas inline en ángulo, solo para eventos puntuales:** `<argh>`, `<breath>`, `<heavy breath>`, `<exhales>`, `<cackle>`, `<cheer>`, `<chuckle>`, `<cough>`, `<cry>`, `<gasp>`, `<giggle>`, `<groan>`, `<growl>`, `<grunt>`, `<grr>`, `<hiss>`, `<laugh>`, `<moan>`, `<pant>`, `<pff>`, `<scream>`, `<shout>`, `<shriek>`, `<sigh>`, `<sneeze>`, `<snicker>`, `<snort>`, `<sob>`, `<throat-clearing>`, `<tsk>`, `<whimper>`, `<whispers>`, `<yawn>`, `<short pause>`, `<long pause>`. **En inglés aunque el transcript no lo sea** (*"continue to use English inline tags for best results"*).
- **Multi-speaker:** `speech_config.speakers` con `{speaker, voice}`, máximo **2 voces prebuilt** por solicitud; `speaker` en el `speech_metadata` de cada turno; reacciones superpuestas entre pipes: `"So the launch is Thursday |oh hmm|"`.
- **Idioma:** *"The TTS models detect the input language automatically."* Flash: 130+ idiomas; Flash-Lite: 100+; ambos listan **"Mexican Spanish"**. No hay campo de idioma documentado para 3.8.
- **Voces:** las mismas **30 prebuilt** que 3.1 (Zephyr, Puck, Charon, Kore, Fenrir, Leda, Orus, Aoede, Callirrhoe, Autonoe, Enceladus, Iapetus, Umbriel, Algieba, Despina, Erinome, Algenib, Rasalgethi, Laomedeia, Achernar, Alnilam, Schedar, Gacrux, Pulcherrima, Achird, Zubenelgenubi, Vindemiatrix, Sadachbia, Sadaltager, Sulafat) + **Extended Voice Library**: `GET /v1beta/voices` con filtros `language_code` (BCP-47), `gender`, `pitch` (`low|medium|high`), `context`, `persona`, `accent`. No encontré ejemplo con `es-MX` en la doc.
- **Diseño de voz (en la API):** `POST /v1beta/voices`, `type: "prompted"`, `prompted.input: "<descripción>"`, `store: true` → devuelve `voice_…` persistente + `sample_audio` WAV. Guía oficial: *"A clear 1–2 sentence description … produces cleaner, more consistent results than contradictory or overly long paragraphs"*; definir lo inmutable: *"age, gender, timbre, vocal texture, and regional accent"*. El `voice_…` se usa donde va un nombre de voz.
- **Réplica de voz (en la API):** `POST /v1beta/voices`, `type: "replicated"`, con `source_audio` (*"A 10–30 second clip of clean, natural speech"*; WAV 24 kHz mono 16-bit recomendado) **y `consent_audio`**: el hablante recita una frase de consentimiento literal (*"I am the owner of this voice and I consent to Google using this voice to create a synthetic voice model"*, o su equivalente en uno de 30 idiomas). El blog dice "a 30-second audio sample" y **la bloquea en Illinois, Texas, EEE, Reino Unido, Suiza e India**. Almacenamiento: `store=true` → `voice_…`, **200 voces por proyecto, 1 año**; `store=false` → `voicekey_…`, **7 días**.
- **Salida:** unaria `audio/wav` (RIFF, 24 kHz, mono, 16-bit); streaming `audio/l16`. Configurable en `response_format.mime_type` (`audio/wav|audio/l16|audio/mulaw|audio/alaw`).
- **SynthID:** todo audio de Gemini sale con marca de agua imperceptible (blog, 2026-10-01).

## A3. Plantillas con slots (3.8)

**A-1 — Línea de personaje con voz prebuilt** (la forma para comparar contra una receta de 3.1):
```
text:  [VERBATIM LINE — exactly as it must be spoken; Spanish OK; English <tags> only for point events]
style: [3-10 words, English: how THIS line is delivered, e.g. "warm, teasing, quick"]
voice: [PREBUILT VOICE NAME]
```
Primero con `style` vacío; luego con `style`. El `style` describe **actuación**, no timbre ni identidad (eso lo pone la voz).

**A-2 — Personaje diseñado** (identidad en la voz, no en el estilo):
```
voice design (prompted.input): [Native Mexican Spanish speaker]. [GENDER], [AGE]. [TIMBRE / TEXTURE — 1 phrase]. [REGIONAL ACCENT]. [PERSONA in 3-5 words].
then per line → text: [VERBATIM LINE]   style: [SHORT DELIVERY STRING or empty]
```
*(La primera frase "Native Mexican Spanish speaker" es mía, no oficial: la doc pide fijar el acento regional, no da plantilla de idioma.)*

**A-3 — Diálogo a dos voces:**
```
speakers: [{speaker: "[NAME1]", voice: "[V1]"}, {speaker: "[NAME2]", voice: "[V2]"}]
turn: text "[LINE]"  speech_metadata {speaker: "[NAME1]", style: "[SHORT]"}
turn: text "[LINE] |[backchannel]|"  speech_metadata {speaker: "[NAME2]"}
```

## A4. Parámetros (3.8)

- **Precio** ([ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing), leído 2026-10-01): **Flash** entrada <costo interno>/M tokens de texto, salida **<costo interno>/M tokens de audio** (≈ <costo interno> por 10 s) **hasta 2026-12-31**; desde 2027-01-01, <costo interno> / **<costo interno>**. Batch: <costo interno> / <costo interno>. **Flash-Lite**: <costo interno> / **<costo interno>** (≈ <costo interno> por 10 s), batch <costo interno> / <costo interno>. Comparación: 3.1 preview <costo interno> / <costo interno>. Nivel gratuito: la página lista Flash como "Free of charge" en el tier gratuito. **Diseño y réplica de voz: sin precio publicado** en esa página.
- **Cuotas (RPM/RPD) del 3.8: no publicadas.** La página de rate limits manda a verlas en AI Studio ([aistudio.google.com/rate-limit](https://aistudio.google.com/rate-limit)) — leída 2026-10-01.
- **Seed / determinismo:** la doc de 3.8 no menciona `seed` ni garantías de consistencia.
- APIs soportadas por el modelo Flash: Batch, Flex y Priority sí; **Live API no** (página del modelo).

## A5. Gotchas documentados (3.8)

- **No meter dirección en el `text`.** Es transcript literal por diseño (cita en A2).
- **Las etiquetas cambiaron de forma:** `<sigh>` en ángulo y solo eventos puntuales. Los estados sostenidos de 3.1 (`[excitedly]`, `[very fast]`, `[sarcastically, …]`) van al `style`, no inline.
- **`style` largo va contra la guía**: la doc pide una cadena corta reutilizada entre turnos y la persona en la voz.
- **Multi-speaker: 2 voces prebuilt máximo** por solicitud.
- **Réplica: exige audio de consentimiento del hablante** y está bloqueada por región (A2). Una voz sintética o un actor sin consentimiento grabado no se puede replicar por esta vía.
- **Discrepancia oficial:** réplica con "10–30 s" (doc) contra "30-second sample" (blog). Usar 30 s si se puede.
- Foro oficial reporta `POST /v1beta/voices` devolviendo **500 INTERNAL** en réplica ([discuss.ai.google.dev/t/184692](https://discuss.ai.google.dev/t/gemini-3-8-voice-replication-post-v1beta-voices-returns-500-internal-with-rest-and-google-genai-2-25-0/184692), título visto en búsqueda 2026-10-01, hilo no leído).

## A6. Leyes medidas en 3.1 — ¿aplican a 3.8?

Ninguna está medida en 3.8. Lo que sigue es la hipótesis de trabajo; **sin toma propia, cada una es "medida en 3.1; no verificada en 3.8"**.

| Ley medida en 3.1 (Parte B / prácticas el estudio) | En 3.8 |
|---|---|
| Lee su propia dirección en voz alta (envoltorio `plano` 3/6, `notas-director` 1/8) | Cambia el mecanismo: la dirección sale del texto. Si se le manda la receta de 3.1 tal cual, el riesgo es **mayor**, no menor. No verificada |
| El catálogo miente en el género (Gacrux "Mature" = 147 Hz hombre; Fenrir, Achird miden mujer) | Mismas voces por nombre; **no verificada** que suenen igual. Medir F0 siempre |
| Texto corto sube el tono (1 línea 118-133 Hz vs bloque 104-111 Hz) | No verificada |
| Pedir energía sube el tono (259 vs 183 Hz) | No verificada |
| Describir el timbre lo vuelve impostado | No verificada; en 3.8 el timbre va a la voz (diseño), lo que coincide con la ley |
| Líneas de 1-2 palabras → sin audio o dice otra cosa | No verificada |
| Degrada > 60 s | No verificada |
| Puntuación gobierna prosodia y pitch (guion largo vs suspensivos) | No verificada |
| No determinista (9 % de diferencia de duración, misma receta) | No verificada; la doc no ofrece `seed` |
| Tope ~100 requests/día por proyecto en Nivel 1 | **No publicado para 3.8**; la primera llamada debe registrar el `quotaId` del 429 si ocurre |
| `speakingRate` no confiable; el ritmo pedido no controla la magnitud → `atempo` | No verificada |

## A7. Iteración (3.8)

Orden recomendado por la doc, que coincide con la disciplina de 3.1: **voz primero** (prebuilt o diseñada), **`style` vacío**, luego un `style` corto por turno, al final etiquetas puntuales. Cambio único por tiro. Para comparar contra una receta sellada de 3.1: misma voz prebuilt, transcript limpio, y la dirección de la receta **condensada** al `style` — guardando el prompt de cada tiro junto a la toma.

---

# PARTE B — Gemini 3.1 Flash TTS preview (recetas en producción)

> Todo lo que sigue es de `gemini-3.1-flash-tts-preview`. Las leyes con fecha y número están **medidas en 3.1; no verificadas en 3.8** (tabla A6).

## 1. Identidad (3.1)

TTS "promptable" de Google: la actuación se dirige con lenguaje natural dentro del mismo texto de entrada (no hay campos separados de estilo en la API). Elegirlo para locución de personaje con dirección actoral fina y castings rápidos (30 voces prebuilt). No elegirlo para audio >60 s por llamada (degrada, ver §5) ni cuando se necesita clonación de voz (eso es ElevenLabs, o la réplica de 3.8).

## 2. Gramática oficial (3.1)

Fuentes: guía oficial de speech generation ([ai.google.dev/gemini-api/docs/speech-generation](https://ai.google.dev/gemini-api/docs/speech-generation), leída 2026-08-20) y blog oficial Google AI DevRel ([dev.to/googleai/how-to-prompt-gemini-31s-new-text-to-speech-model-24bb](https://dev.to/googleai/how-to-prompt-gemini-31s-new-text-to-speech-model-24bb), leído 2026-08-20).

- **Request:** `generateContent` con `responseModalities: ["AUDIO"]`; voz e idioma van en `speechConfig` (`prebuiltVoiceConfig.voiceName`, `languageCode`), NUNCA en el texto. Salida PCM 24 kHz mono.
- **Nivel básico (oficial):** instrucción antepuesta en texto plano — `Say in a spooky whisper: "..."`. Sirve para una línea con una sola intención.
- **Nivel estructurado (oficial):** encabezados markdown — `# AUDIO PROFILE`, `## THE SCENE`, `### DIRECTOR'S NOTES` (Style / Pace / Accent), `### SAMPLE CONTEXT`, `#### TRANSCRIPT`. Documentado literalmente en la guía oficial; es el formato para personaje sostenido.
- **Audio tags inline (oficial):** `[whispers]`, `[sighs]`, `[laughs]`, `[excitedly]`, `[bored]`, `[very fast]`, `[very slow]`, `[shouting]`, `[sarcastically, one painfully slow word at a time]`… Cita oficial: *"There is no exhaustive list on what tags do and don't work, we recommend experimenting."*
- **Tags en inglés aunque el transcript no lo sea** — recomendación oficial textual: *"if your transcript is not in English, we recommend that you still use English audio tags."*
- **Ritmo:** en lenguaje natural ("~15% faster than normal") o tags `[very fast]`/`[very slow]` por tramo. El parámetro numérico de la API (`speakingRate`) no es confiable (verificado en producción el estudio 2026-08; la doc oficial no lo ofrece para estos modelos).
- **Límite:** 32k tokens por sesión TTS (oficial); mantener el transcript en pocos minutos.
- **Anti-sobreactuación (oficial):** no describir todo — *"giving the model space to fill in the gaps helps naturalness"*.

## 3. Plantillas con slots (3.1)

**A — Línea suelta de personaje (nivel básico):**
```
[PERSONA: age, vocal weight, pitch, accent — 2-4 sentences max]. STYLE: [CHARACTER STYLE — positive terms]. Direccion de esta linea: [LINE DIRECTION]. [PACE PHRASE, e.g. "Fast conversational pace, ~15% faster than normal"]:
[LINE TEXT — may include inline English tags like [sighs], [deadpan]]
```

**B — Personaje sostenido (nivel estructurado, recomendado para series):**
```
### DIRECTOR'S NOTES
Do NOT speak these notes. Speak ONLY the lines under TRANSCRIPT.
Voice: [AGE + GENDER + VOCAL QUALITIES].
Accent: [ACCENT SPEC].
Character: [PERSONALITY — 1-2 traits, concrete].
Style: [DELIVERY STYLE — positive terms, melody, what it never is].
Emotional intensity: [N] out of 10.

#### TRANSCRIPT
[LINE TEXT with optional inline English tags]
```

**C — Multi-speaker (una llamada, 2+ voces):**
```
TTS the following conversation between [NAME1] and [NAME2]. Make [NAME1] sound [STYLE1] and [NAME2] sound [STYLE2]:
[NAME1]: [LINE]
[NAME2]: [LINE]
```
Config aparte mapea cada `speaker` a su voz; los nombres deben coincidir EXACTO con los del texto (alias alfanuméricos sin espacios).

## 3b. El prompt de cada párrafo (la "dirección") — medido en 3.1

El prompt que recibe Gemini TTS tiene tres pedazos: **quién es** el personaje (su receta sellada, no se toca) · **cómo dice este párrafo** (lo escribe el storyteller, o quien saque la voz) · **qué dice** (el guion, palabra por palabra). Esta sección rige el segundo pedazo. `node scripts/receta.mjs ver <serie.json>` (motor AVE) la imprime junto con ejemplos aprobados de cada personaje, y el storyteller está obligado a correrlo antes de escribir; para una voz suelta, `node scripts/locutar.mjs <personaje> --guia`, y `locutar` la muestra compacta en toda corrida con un prompt nuevo. Los ejemplos crecen solos: al elegir una locución con ✓ en el panel, su prompt entra al registro de aprobadas. Nació del un cliente industrial EP3 (2026-09-25): el diagnóstico completo está en `<ruta interna>`.

1. **Un prompt por segmento de voz, escrito de un tirón.** Si el personaje se genera por párrafo (un personaje recurrente, ley L12), su prompt es UN arco que recorre el párrafo en orden. No se arma pegando la nota de cada plano de cámara con anclas `«…»:` o separadores `·`: eso lo hizo un script de un solo uso, no un director (copia en `…\<ruta interna>`). En la escaleta el prompt vive en `voz.segmentos[]` y `locutar.mjs --escaleta` lo lee tal cual. *(Forma, no ley medida: la 1.1.1 llevaba anclas y se aprobó.)*
2. **Di qué HACE cada frase, no qué adjetivo lleva:** "como llamada de atención", "pregunta de verdad, la entonación sube al final", "imita a un compañero despreocupado", "como título", "como quien te cuenta algo que no es tan obvio". Las 41 aprobadas de un personaje recurrente traen 1.5 de estas marcas por cada 100 palabras; las del storyteller rechazadas en EP3, 0.6; el re-tiro aprobado, 2.3 (`node rasgos-texto.mjs` en `<ruta interna>`, 2026-09-25).
3. **Nunca dos registros opuestos sobre la misma frase.** "Lo de doble aguas va coloquial y serio a la vez" hizo que "doble aguas" sonara afectado (el director, 2026-09-26 00:30); "'doble aguas' como llamada de atención" se aprobó a la primera. *(n=1: dato, no ley.)*
4. **Una inflexión concreta se pide citando la frase y describiendo la melodía.** Citar "que se fije bien" ganó el A/B de §7; "'¿no?' es una pregunta de verdad, con la entonación que sube al final" arregló la 1.2.1 que había salido plana. Esto contradice el folklore de §6 y aquí manda lo medido.
5. **La dirección no toca identidad ni timbre** ("voz grave y asentada", "sobria", "otra voz"): eso es de la receta. El 2026-09-23 una dirección reescrita así dejó a un personaje recurrente plano ("no suena a un personaje recurrente", EP2 R1).
6. **Texto corto sube el tono.** Un segmento de pocas palabras arranca agudo: se junta con el vecino (§5). En EP3, "La técnica de evasión se hace en tres tiempos" (8 palabras) sola salió a 170 Hz y "no suena a un personaje recurrente"; en bloque con el siguiente, 154 Hz y aprobada.
7. **Lo que NO es problema** (medido sobre las 41 aprobadas de un personaje recurrente): "cómplice" (29 %), "sin X / no X" (78 %), etiquetas "A cámara / Voz en off" (61 %), citar frases del guion (88 %). Un lint con esas palabras reprobaría 29 de las 41. Tampoco el tono medio separa lo bueno de lo malo: las tomas rechazadas del storyteller midieron 134 Hz y las aprobadas del re-tiro, 145 Hz (`python medir-f0.py`, misma carpeta `_lab`, 93 tomas).

8. **El texto es solo lo que se dice; la acotación del guion va en la dirección.** Lo que el guion trae entre paréntesis, corchetes o asteriscos (`(se ríe sutilmente)`, `[risas]`, `*susurra*`) y el nombre del personaje (`una personaje recurrente:`) no son texto. Si es actuación de voz, se escribe en la dirección del párrafo ("se ríe sutilmente al decir 'Ay, mijo'"); si es acción visual, va al prompt de video; el nombre se quita. Gemini dice todo lo que esté en el transcript, y el gate no lo caza porque compara contra el mismo texto: a una personaje recurrente se le coló `(se ríe sutilmente)` en la t42 y lo leyó en voz alta (2026-09-01). `locutar` avisa cuando ve una marca así, pero no bloquea: un paréntesis que sí se dice («el director (el director de el estudio) te saluda») es legítimo, y decide quien escribe (el director, 2026-10-06).

**Lo que ninguna regla garantiza:** que el párrafo suene al personaje. Eso lo decide el oído de el director en el panel; las reglas solo quitan las causas que ya se vieron.

### Por personaje

Los EJEMPLOS de cada personaje no se copian aquí: salen de su registro de direcciones aprobadas (`direcciones.json` junto a su `serie.json`) y `receta.mjs ver` los imprime. Aquí van solo las reglas medidas que son SOLO suyas.

#### un personaje recurrente
- "Serio" es un cambio LOCAL ("se pone serio en 'X'", "baja un tono"), nunca el tono de todo el segmento.
- Su idioma aprobado: abre con el encuadre y la función del beat ("A cámara, baja la guardia: esto es consejo entre compañeros") y luego recorre las frases citadas en orden, diciendo qué hace cada una.

#### aoede-storytelling
- No pedir energía, variación ni velocidad: sube el tono y se rechaza por agudo (253 Hz contra 216 Hz de la aprobada). Fuente: `<ruta interna>`.

#### un personaje recurrente
- Las direcciones se escriben en el registro de su persona VIGENTE ("playful dry irony"): las 12 escritas para la persona anterior ("seco sobrio") lo aplanaron (§7, una serie de sketches EP2 V3, 2026-08-21).

## 4. Parámetros (3.1)

- 30 voces prebuilt (catálogo con característica oficial de cada una en la doc); la API no valida el nombre — un typo genera con otra cosa.
- `languageCode` (p. ej. `es-MX`) va en config, no en el prompt.
- Salida: PCM 24 kHz mono 16-bit (envolver a WAV es del cliente).
- **Cuota diaria de `gemini-3.1-flash-tts`, medida en producción (2026-08-20/21):** nivel gratuito = **10 requests/día** (`quotaId …PerDayPerProjectPerModel-FreeTier`); **Nivel 1 (facturación vinculada) = 100/día** (`…PerDayPerProjectPerModel`) — vincular facturación NO quita este tope en el preview, solo sube de 10 a 100. Es **por proyecto de Google Cloud**: otro proyecto = otro contador (de ahí el pool de claves). Los "retry in" del 429 son poco fiables (pasaron de "7 min" a "23 h" en 20 min); confiar en la cuenta propia, no en el reloj de Google. Aumento real: formulario de cuota (aistudio.google.com/rate-limit).

## 5. Gotchas documentados (3.1 — medidos en 3.1; no verificados en 3.8)

- **Lee su propia dirección en voz alta** si las notas no están separadas del transcript con instrucción explícita. Mitigación: preámbulo *"Do NOT speak these notes. Speak ONLY the lines under TRANSCRIPT."* (guía LiveKit, ver §6; el bug está reproducido en producción el estudio). **La mitigación es PARCIAL, medido 2026-09-07** (casting del Detective, `<ruta interna>`, mismo texto y misma persona): con envoltorio `plano`, **3 de 6** tomas leyeron la dirección; con `notas-director`, **1 de 8** — y apareció un artefacto vecino, **2 de 8 repiten el último párrafo del guion**. Las tomas contaminadas duran 2-3× lo normal (44-53 s contra ~20 s), así que **la duración anómala es el detector barato**; el que decide es el gate de transcripción. Corolario para castings: se arranca en `notas-director` (SOP `video-receta-personaje` §3) y se transcriben TODAS las tomas, también las de casting.
- **Líneas de 1 palabra + persona larga → "respuesta sin audio"** casi determinista (reproducido el estudio 2026-07-07: 10-15 reintentos fallidos; foro oficial confirma el bug sin fix: [discuss.ai.google.dev/t/108163](https://discuss.ai.google.dev/t/gemini-2-5-pro-preview-tts-not-working-constant-no-audio-generated-error/108163)). Mitigación para monosílabos: estilo mínimo directivo ("identidad en 1 frase + 'di únicamente la palabra, [tono]'") — SOLO para esa línea, nunca como recorte permanente de identidad.
- **Degradación >60 s** en `gemini-3.1-flash-tts-preview`: medición de terceros (ttsaudit.com, 2026): 90% de generaciones >1 min degradan (ej. 92/100 primeros 16 s vs 34/100 último minuto). Generar por línea/segmento corto.
- **El REGISTRO depende del largo del texto: en pieza corta el modelo arranca más agudo** *(medido 2026-09-08, `algenib-detective`, misma persona y misma voz)*. La toma de casting —bloque de 3 líneas— salió a **107 Hz**; las piezas de producción de una o dos líneas, a **118-133 Hz**. el director lo oyó como *"suenan menos profundas, menos misteriosas"* antes de que nadie midiera. Re-generado en un solo bloque, volvió a **104-111 Hz**. **No es el envoltorio** (la misma persona en `notas-director` midió 108). Corolario práctico, y choca de frente con la ley de arriba: **para una voz que vive de su gravedad, generar por BLOQUES y cortar en montaje** — no por línea. El techo sigue siendo los 60 s de esa ley; entre 15 y 30 s está el punto dulce. *(Bloques y tomas: `<ruta interna>`; recontar con `scripts/qc/pitch_genero.py`.)*
- **La PUNTUACIÓN gobierna la prosodia — y también el pitch** *(medido 2026-09-08, mismo prompt y mismo texto salvo un signo)*: `una es-láid — una idea` (guion largo) dio **104 y 116 Hz**; `una es-láid… una idea` (suspensivos) dio **124 y 130 Hz** en las mismas condiciones. Los suspensivos piden suspender y suspender empuja hacia arriba; el guion largo pide una pausa firme. Para forzar una equivalencia hablada ("A **es** B") sin tocar el copy, el guion largo es la herramienta.
- **Nunca instruir "flat / monotone / quiet"** — apaga la voz entera; describir melodía en positivo ("phrases end flat or slightly downward" sí funciona: es melodía, no energía).
- **La consistencia entre llamadas NO está documentada por Google** y en la práctica la actuación varía por semilla con prompt idéntico: tirar 2-3 tomas y elegir sigue siendo el método.

## 6. Folklore de comunidad (3.1)

Fuente principal: guía LiveKit ([livekit.com/blog/gemini-3.1-flash-tts-prompting-guide](https://livekit.com/blog/gemini-3.1-flash-tts-prompting-guide), leída 2026-08-20) — proveedor serio, no oficial. Confianza: `reproducible` salvo nota.

- Evitar apóstrofes en encabezados (`DIRECTOR'S` puede leerse en voz alta) → usar `DIRECTOR NOTES` o `### PERFORMANCE`.
- Comas entre cláusulas con tags; puntos solo en fin de oración real; elipsis (1-2 por enunciado) y em-dash para micro-pausas.
- ~~No citar palabras literales del transcript dentro de las notas de Style/Pace~~ — **refutado en el estudio** con persona sellada: citar la frase exacta ganó el A/B (§7) y está en 36 de las 41 direcciones aprobadas de un personaje recurrente. Ver §3b regla 4.
- Aislar la palabra a enfatizar entre `...` en el TEXTO (no en el estilo) — coincide con práctica reproducida en producción.

## 7. Iteración (3.1)

Cambio único por tiro: primero persona (timbre), luego style (carácter), luego dirección de línea, al final tags inline. Anclar lo ganado: cuando un bloque de persona suena bien, se congela textual (en el estudio: receta sellada) y solo se itera la capa de línea. Para juzgar "¿suerte o proceso?": 3 tiros del MISMO prompt; si el carácter no se sostiene, falta especificación — subir de plantilla A a B, no engordar la prosa.

**Lecciones del primer casting real con estas plantillas (una serie de sketches EP2 V3, 2026-08-21):**
- **El formato no es universal.** La plantilla B (Director's Notes en inglés) ganó el casting de un personaje recurrente (3 tiros consistentes, comedia deadpan); a RH la volvió irreconocible en 5 rondas, y ganó la plantilla A en español con su persona previa + UNA frase nueva. Probar ambas por personaje; "la base que ya sonaba + cambio mínimo" vence a reescribir.
- **Declarar el género** (`Scene: a deadpan COMEDY sketch… no gravitas`) quitó el drama que el modelo ponía por defecto ante "irony" + intensidad 6; bajar a intensidad 4 ayudó.
- **Las direcciones de línea pertenecen al registro de la persona vigente**: direcciones "seco/deadpan absoluto" escritas para una persona sobria aplanaron a la persona juguetona aunque el bloque de identidad fuera el correcto.
- **Acciones visuales nunca al TTS** (van al prompt de video); **dirección por línea siempre**.

**A/B de dirección sobre una receta ya sellada (un cliente industrial EP3, 2026-09-25, voz Charon, envoltorio plano, mismo texto de 64 palabras, 2 tomas por lado):** A = dirección del storyteller tal cual (plano por plano, con anclas «…» que citan el guion, etiquetas "En off / A cámara" y varios "sin dramatizar / sin exclamar"); B = la misma intención reescrita con esta ficha (en positivo, sin etiquetas visuales, sin citar el transcript). **Ganó A:** *"tienen más estilo las A… la interpretación de 'que se fije bien' suena mejor"* (el director). B salió ~2 s más corta y fue "buena, pero no sé". Lectura: con una persona ya sellada, citar la frase exacta que hay que actuar (la imitación) le da al modelo el ancla que la reescritura en abstracto le quita. El folklore de §6 "no citar palabras del transcript" **no se sostuvo aquí**; los negativos "sin X" tampoco aplanaron. Muestra chica (n=2 por lado, un segmento): es un dato, no una ley.

**Validación de §3b (un cliente industrial EP3 1.3.1, 2026-09-25 23:07):** el párrafo que había fallado ("doble aguas"), con el prompt escrito por el storyteller contra §3b y SIN ver la dirección aprobada, 2 tomas (22.8 y 21.8 s, <costo interno>): el director, *"suenan bien"*. El prompt tenía 172 palabras contra 94 del aprobado y no sonó sobredirigido. Un párrafo: señal, no patrón (tomas `v05_guia`/`v06_guia` en `<ruta interna>`).

## 8. Historial (de toda la ficha)

- 2026-08-21 — ficha creada desde investigación documental (corrida una serie de sketches-ep2-v3); modelo motivador: `gemini-3.1-flash-tts-preview`.
- 2026-08-21 (tarde) — cuota medida por tier y lecciones del casting un personaje recurrente/RH.
- 2026-09-25 — §3b "El prompt de cada párrafo" (diagnóstico un cliente industrial EP3) con sus reglas por personaje; `receta.mjs ver` la imprime al storyteller. El folklore de §6 "no citar el transcript" queda refutado.
- 2026-10-01 — **Parte A: Gemini 3.8 Flash / Flash-Lite TTS** (GA 2026-09-23) desde la doc oficial de Google: gramática nueva (`text` literal + `speech_metadata.style` + etiquetas `<…>`), diseño y réplica de voz en la API, precios con fecha. Las leyes de 3.1 se conservan como Parte B, marcadas "medidas en 3.1; no verificadas en 3.8" (tabla A6). Motivo: prerrequisito del torneo de voz 2026-10. `status` vuelve a `vigente`.
- 2026-10-06 — §3b regla 8: la acotación del guion va en la dirección, no en el texto. `locutar` tenía un lint que bloqueaba esas marcas (exit 4) y el director eligió que solo avise: la regla pasa a donde el agente la lee al escribir.
