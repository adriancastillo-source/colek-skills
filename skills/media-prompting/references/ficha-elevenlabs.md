---
herramienta: ElevenLabs (TTS, Voice Design, Instant Voice Cloning, Dubbing)
modelo-vigente: eleven_v4 (2026-09-28) · eleven_v4_turbo (tiempo real) · eleven_v3 (generación anterior, sigue en la API) · dubbing_v2 (Alpha; doblaje, ver §Dubbing)
dominio: voz
updated: 2026-10-29
status: vigente
---

# Ficha de prompting — ElevenLabs (Eleven v4)

## ⚠️ Desambiguación — qué cubre esta ficha

| | **Eleven v4** (`eleven_v4`, esta ficha) | **Eleven v3** (`eleven_v3`) |
|---|---|---|
| Límite por solicitud | **10,000 caracteres** (~10 min) | 5,000 (~5 min) |
| Idiomas | 90+ (la tabla de modelos lista "Spanish, LatAm") | 70+ |
| Ajustes de voz | **Solo Stability y Similarity** — *"Style and Speed sliders are not available in Eleven v4"* | Ver nota de la guía de producto abajo |
| Etiquetas de actuación `[…]` | **Sí** (resuelto abajo, §2) | Sí |
| SSML `<break>` | No | No |

Lo de v3 que sigue vigente se marca **(v3)**. Fuentes: [docs/overview/models](https://elevenlabs.io/docs/overview/models) y [docs/eleven-creative/playground/text-to-speech](https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech), leídas 2026-10-01.

## 1. Identidad

TTS de ElevenLabs cuya actuación se dirige **dentro del texto**, con etiquetas en corchete y puntuación; no hay campo separado de "estilo". La identidad (timbre, edad, **acento**) la pone la **voz elegida**: de la biblioteca, diseñada por descripción o clonada. Elegirlo cuando se necesite un timbre concreto (clon), una voz de marca, o acento regional elegido por voz. No elegirlo cuando el control del ritmo deba venir del modelo: v4 no tiene control de velocidad (§4).

## 2. Gramática oficial

### ¿v4 acepta etiquetas de actuación inline? — **Sí. Fuente que decide:**
La guía oficial de prompting tiene una sección propia "Prompting Eleven v4" ([elevenlabs.io/docs/best-practices/prompting](https://elevenlabs.io/docs/best-practices/prompting) y su ancla de v4, leídas 2026-10-01): *"Eleven v4 handles them with a level of nuance beyond previous models."* Lo confirman la guía de producto de TTS (*"Both models support audio tags"*, v3 y v4) y la página del modelo ([elevenlabs.io/v4](https://elevenlabs.io/v4): *"Write direction into the script"*). La tabla de [docs/overview/models](https://elevenlabs.io/docs/overview/models) **no las menciona** para v4: es omisión de esa tabla, no restricción — la guía de prompting es la fuente específica. *(La página de capacidad de TTS atribuye "audio tags" solo a "v3 Conversational y v4 Turbo" en su resumen; las otras tres fuentes la contradicen.)*

### La gramática
- **Etiquetas en corchete, en inglés, dentro del texto.** Ejemplos oficiales de la guía v4/v3: voz `[laughs]`, `[laughs harder]`, `[starts laughing]`, `[wheezing]`, `[whispers]`, `[sighs]`, `[exhales]`, `[sarcastic]`, `[curious]`, `[excited]`, `[crying]`, `[snorts]`, `[mischievously]`; efectos `[gunshot]`, `[applause]`, `[clapping]`, `[explosion]`, `[swallows]`, `[gulps]`; experimentales `[strong X accent]`, `[sings]`. Página v4: `[pause]`, `[long pause]`, `[door slams]`. Blog v4: dirección en lenguaje natural dentro del corchete, p. ej. `[said angrily in French accent]` ([elevenlabs.io/blog/eleven-v4](https://elevenlabs.io/blog/eleven-v4), 2026-10-01).
- **Las etiquetas funcionan mejor si la entrega ya está en la voz:** *"Tags land more readily when the delivery is already in the voice's training data."* Elegir la voz para el papel; la etiqueta afina, no transforma.
- **Puntuación = control:** *"Ellipses (...) add pauses and weight"*, *"Capitalization increases emphasis"*, puntuación estándar para el ritmo. Ejemplo oficial: `It was a VERY long day [sigh] … nobody listens anymore.`
- **El texto manda:** *"Text structure strongly influences output with v4. Use natural speech patterns, proper punctuation, and clear emotional context."* (guía v4).
- **Sin SSML:** *"Eleven v4 and Eleven v3 do not support SSML break tags"*; *"SSML tags such as <break> are disabled in Eleven v4, so use the natural-language tags instead"* (elevenlabs.io/v4).
- **Pronunciación (v4):** IPA entre barras, `/ˈIPA/`, con acentos de intensidad primario (ˈ) y secundario (ˌ), *"only wrap specific words or phrases"* (guía, sección de controles). Diccionarios: hasta 3 `pronunciation_dictionary_locators` por solicitud.
- **Normalización de texto** activa por defecto (`apply_text_normalization: auto|on|off`) para números, monedas, fechas.
- **Idioma:** `language_code` ISO 639-1 (p. ej. `es`; **no hay locale `es-MX`** en ese campo). El acento lo pone la voz: *"When the language you're generating matches the language of your reference voice, the original accent is preserved exactly as before. When the language differs, Eleven v4 generates fluent, natural-sounding speech in the target language"* (guía de producto).

### Voz: biblioteca, diseño, clon
- **Biblioteca por descripción** — `GET /v1/shared-voices` con filtros `search`, `gender`, `age`, `accent`, `language`, `locale`, `use_cases`, `descriptives`, `category` (`professional|famous|high_quality`), `sort`, `page_size` ≤ 100 ([api-reference/voices/voice-library/get-shared](https://elevenlabs.io/docs/api-reference/voices/voice-library/get-shared), 2026-10-01). Cada voz trae `verified_languages[]` con `language`, `model_id`, `accent`, `locale`, `preview_url`: **filtrar por la verificación del modelo y locale que se va a usar**, no solo por la etiqueta de la voz. La doc de voces lista "Spanish (Spain, Mexico)" como soportados ([docs/capabilities/voices](https://elevenlabs.io/docs/capabilities/voices)).
- **Biblioteca por parecido a un audio** — `POST /v1/similar-voices` con `audio_file`, `similarity_threshold` (0-2), `top_k` → voces compartidas parecidas ([api-reference/voices/find-similar-voices](https://elevenlabs.io/docs/api-reference/voices/find-similar-voices), 2026-10-01). Útil para buscar el timbre de una toma aprobada sin clonarla.
- **Diseño de voz** — `POST /v1/text-to-voice/design`: `voice_description` (20-1000 caracteres), `text` de muestra (100-1000), `guidance_scale` (def. 5; más alto = más fiel al prompt, puede bajar calidad en voces raras), `loudness`, `seed`, `model_id` `eleven_multilingual_ttv_v2` (def.) o `eleven_ttv_v3`; se guarda con `/v1/text-to-voice` usando el `generated_voice_id` ([api-reference/text-to-voice/design](https://elevenlabs.io/docs/api-reference/text-to-voice/design)). *"Voices created with Voice Design work with Eleven v4"* ([docs/eleven-creative/voices/voice-design](https://elevenlabs.io/docs/eleven-creative/voices/voice-design)). Formato oficial de descripción: `Native <Language>. <Gender>, <Age range>. <Quality level>. Persona: <2–5 words>. Emotion: <2–3 adjectives>. <1–2 sentences about timbre, pacing, delivery>`. Para acento: *"'thick' often yields better results than 'strong'"*.
- **Clon rápido (IVC)** — `POST /v1/voices/add` con `name`, `files[]`, opcionales `remove_background_noise`, `description`, `labels` (language, accent, gender, age) ([api-reference/voices/ivc/create](https://elevenlabs.io/docs/api-reference/voices/ivc/create)). **Duración: las fuentes oficiales no coinciden** — blog y página v4: *"just 10 seconds of audio"*; guía de IVC: *"1–2 minutes of good audio"*, y *"Avoid recording more than 3 minutes"*; un solo hablante, sin ruido ni reverb, sin silencios largos, idealmente −23 a −18 dB RMS con pico verdadero −3 dB ([docs/eleven-creative/voices/voice-cloning/instant-voice-cloning](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/instant-voice-cloning), 2026-10-01). Antes de guardar se confirma tener *"the right and consent to clone the voice"*.

### Endpoints
- **Text to Speech:** `POST /v1/text-to-speech/{voice_id}` (y su stream) con `model_id: "eleven_v4"` — *"You can generate with Create speech and Stream speech using model ID eleven_v4"* (página v4). Campos: `text`, `model_id`, `language_code`, `voice_settings`, `seed` (0-4294967295), `previous_text`/`next_text`, `previous_request_ids`/`next_request_ids` (máx. 3), `apply_text_normalization`, `pronunciation_dictionary_locators` ([api-reference/text-to-speech/convert](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)).
- **Text to Dialogue:** `POST /v1/text-to-dialogue`, `inputs[{text, voice_id}]`, hasta 10 voces, **≤ 2,000 caracteres en total** por solicitud; `settings` con `stability` y `similarity`; `previous_text`/`future_text` ≤ 100 caracteres. El changelog del 2026-09-28 presenta v4 *"through the Text to Dialogue API for content creation and long-form audio"*; la referencia de la API aún muestra `eleven_v3` como valor por defecto ([docs/changelog/2026/9/28](https://elevenlabs.io/docs/changelog/2026/9/28), [api-reference/text-to-dialogue/convert](https://elevenlabs.io/docs/api-reference/text-to-dialogue/convert)).

## 3. Plantillas con slots

**A — Línea de personaje (una voz, TTS):**
```
[ENGLISH DELIVERY TAG — what the line DOES, e.g. "teasing, warm"] [SPANISH LINE, punctuated for rhythm…] [OPTIONAL POINT TAG, e.g. laughs] [REST OF LINE, CAPS only on the word to stress].
```
Voz = la del personaje · `model_id: eleven_v4` · `language_code: es` · `voice_settings: { stability: [0-1], similarity_boost: [0-1] }`.

**B — Descripción para elegir o diseñar la voz del personaje:**
```
Native Mexican Spanish. [Male/Female], [age range]. Studio quality. Persona: [2-5 words]. Emotion: [2-3 adjectives]. [1-2 sentences: timbre, pacing, delivery — thick Mexican accent if wanted].
```
Sirve para `voice_description` (diseño) y, recortada a palabras clave, para `search`/`descriptives` de la biblioteca.

**C — Clon de un timbre ya aprobado:**
```
files: [CLEAN APPROVED TAKES of ONE speaker, concatenated, no music/reverb, target 1-2 min per guide; 10 s is the advertised minimum]
labels: { language: "es", accent: "[mexican]", gender: "[..]", age: "[..]" }
then use template A with the cloned voice_id
```

## 3b. El prompt de cada párrafo (las etiquetas) — v4: doc oficial, casi nada medido todavía

En ElevenLabs no hay persona que escribir: la identidad (timbre, edad, acento) la pone **la voz** —el clon— y los ajustes, y las dos cosas viven selladas en la receta. Lo que se escribe por párrafo es **el texto con su dirección en etiquetas**. En el motor AVE la receta declara `envoltorio: "etiquetas"`: la dirección de la pieza entra como etiqueta inicial (`[dirección] texto`) y el texto puede traer más etiquetas dentro. `node scripts/locutar.mjs <personaje> [--variante <nombre>] --guia` imprime esta sección, y el gate de guion compara cada toma contra el texto **sin** etiquetas.

1. **La etiqueta dice qué HACE la frase, en inglés y entre corchetes:** `[calm, reflective]`, `[convinced]`, `[proud, clear]`, `[whispers]`, `[laughs]`. Nunca escena ni postura (`[standing]`, `[music]`, §5). *(Gramática oficial, §2.)*
2. **Una etiqueta por cambio de intención, al inicio de la frase que cambia.** Así salió la única escena de el estudio hecha con v4 y etiquetas que se aprobó: 3 párrafos con 7 etiquetas, cada una abriendo la frase que cambiaba (una serie de capacitacion EP5, escena 1; el director, 2026-10-05: «más consistente entre locuciones»). *(n=1: forma aprobada, no ley medida.)*
3. **El ritmo se escribe con puntuación, no con parámetros.** v4 no tiene `speed` ni `style`: las pausas van con comas, puntos, puntos suspensivos o `[pause]`, y SSML/`<break>` no funciona (§4, §5). Si hay que acelerar, es post (`atempo`) declarado en la receta.
4. **La etiqueta no pide identidad** (`[deeper voice]`, `[Mexican accent]` sobre un clon): timbre y acento son de la voz, y una etiqueta que contradice a la voz falla o sale débil (§5).
5. **Que las etiquetas se actúen y no se lean está medido en v3, no en v4** (§6). Por eso el gate corre en cada toma: si el modelo lee una etiqueta, la transcripción trae palabras de más y la toma no se entrega. Del otro lado, sin verificar: una risa (`[laughs]`) que el transcriptor escriba «ja ja» también cuenta como palabras de más y reprueba una toma buena.

6. **El texto es solo lo que se dice; la acotación del guion se vuelve etiqueta.** Una acotación en español del guion (`(se ríe)`, `*susurra*`) no se pega al texto: se traduce a etiqueta en inglés en su lugar (`[laughs]`, `[whispers]`) o pasa a la dirección de la pieza. El nombre del personaje (`una conductora:`) se quita. Todo lo que quede fuera de corchetes, el modelo lo dice. `locutar` avisa cuando ve una marca así fuera de corchetes, pero no bloquea: decide quien escribe (el director, 2026-10-06).

**Lo que ninguna regla garantiza:** que la frase suene al personaje. Eso lo decide el oído de el director; estas reglas solo evitan los errores que la documentación ya avisa.

## 4. Parámetros

- **`voice_settings` en v4: Stability y Similarity.** *"Both variants use two voice settings: Stability and Similarity. Stability controls how consistent the delivery stays, with lower values allowing more expressive variation and higher values favoring consistency"* (página v4). Descripción de la API: *"Lower values introduce broader emotional range … Higher values can result in a monotonous voice"*; defaults `stability 0.5`, `similarity_boost 0.75`. Guía de producto: *"stability around 50, similarity around 75, and keeping style at 0"*.
- **Velocidad: no disponible en v4** (*"Style and Speed sliders are not available in Eleven v4"*). La API acepta `speed` (0.7-1.2 en la guía) para otros modelos; **en v4 el ritmo se controla con puntuación, etiquetas (`[pause]`) y post** (`atempo`).
- **Determinismo:** *"Output is nondeterministic — use the `seed` parameter for more consistent results"*; *"Determinism is not guaranteed."* La página v4 afirma estabilidad de hablante entre regeneraciones: *"Redo a line once or fifty times and it's still the same person speaking"* — es identidad, no la misma toma.
- **Salida:** `output_format` `codec_samplerate_bitrate` (def. `mp3_44100_128`; también `pcm_*`, `opus`, `ulaw`, `alaw`).
- **Precio** ([elevenlabs.io/pricing/api](https://elevenlabs.io/pricing/api), leído 2026-10-01): **Eleven v4 <costo interno> por 1K caracteres (72 % de descuento) hasta el 2026-10-12; lista <costo interno>**. v4 Turbo <costo interno> promo / <costo interno> lista. v3 <costo interno>; v3 Conversational <costo interno>; Flash/Turbo <costo interno>. La página dice *"API usage is billed in US dollars, not credits"*, mientras el blog habla de *"3x credits included on Creator+ until October 12"* — cómo se cruzan el saldo del plan Creator y la facturación de API **no está claro** (ver Huecos). Diseño de voz y clon: sin precio en esa página.
- **Permisos de la llave:** las llaves se pueden restringir por endpoint y con tope de créditos ([api-reference/authentication](https://elevenlabs.io/docs/api-reference/authentication)). Los nombres de los permisos (TTS, Voices Read/Write) **no aparecen en esa página**: verificar en el panel de la llave antes de crear voces.

## 5. Gotchas documentados

- **Etiquetas que no son de voz no sirven:** evitar `[standing]`, `[grinning]`, `[pacing]`, `[music]` (guía v3; la de v4 hereda la advertencia de no contradecir el carácter de la voz).
- **Etiquetas contradictorias con la voz fallan o salen débiles** (*"Avoid tags contradicting the voice's character"*); las experimentales no son consistentes.
- **Sin `<break>` ni SSML** en v4/v3.
- **Sin `speed`/`style` en v4** — no portar la configuración de v2/Flash.
- **Text to Dialogue tiene tope de 2,000 caracteres** aunque el modelo acepte 10,000 en TTS.
- **El clon hereda el acento de la muestra en su idioma**: muestra en español MX → acento conservado (guía de producto). Muestra con ruido, reverb o música → clon sucio.
- **MEDIDO (torneo voz 2026-10): un clon instantáneo de una voz SINTÉTICA puede quedar bloqueado.** El clon de un personaje recurrente (voz Puck de Google TTS) dejó pasar la primera toma y desde la segunda respondió 403 `voice_access_denied` / `detected_captcha_voice`, pidiendo grabar al hablante en vivo; recrearlo con la misma fuente dio lo mismo (2 de 2 clones). un conductor, un personaje recurrente y Doña (también voces de Google) no se bloquearon. No hay hablante humano que verifique, así que **no se puede contar con el clon de una voz sintética para producción**; no se esquiva alterando la muestra. Evidencia: `<ruta interna>`.
- **SOSPECHA (n chico, sin medir): «clear» al abrir una pieza puede provocar un carraspeo.** En una serie de capacitacion EP13 (2026-10-07, clon de un conductor) arrancaron carraspeando P03 (2 de 2 tomas) y P04 (1 de 2), las dos abiertas con `[clear, explanatory]`. P05, abierta igual, y EP1 P02 no carraspearon. Mientras no se mida, conviene no abrir una pieza con «clear». Si el carraspeo queda antes de la primera palabra y hay silencio después, se corta en edición, sin regenerar.
- **MEDIDO: la búsqueda por similitud no filtra acento.** Con `similar-voices` y acento «latin american», 3 de 4 voces elegidas eran es-AR. Para un personaje mexicano, filtrar `locale es-MX` explícito (mismo veredicto).

## 6. Folklore de comunidad

Sin folklore incorporado en esta versión: no se leyó ninguna guía de terceros para v4 (el modelo tiene 3 días). Lo medido en el estudio es de **v3**:
- **(v3)** Las etiquetas `[cheerfully]`, `[mockingly]`, `[warmly]` **se interpretan, no se leen** — verificado por transcripción, casting un cliente de entretenimiento 2026-08-25. `reproducible` en v3; **no verificado en v4**.
- **(v3)** En ese casting v3 perdió contra Gemini 3.1 en los dos papeles (chavo de 25 y señora mayor), incluso con clon. Dato de v3, no de v4.

## 7. Iteración

Primero la **voz** (es la que trae timbre y acento), luego **Stability**, luego etiquetas y puntuación, de a un cambio. Para una serie: fijar voz + settings + `seed` y variar solo el texto. Si una etiqueta no "aterriza", cambiar de voz antes que sumar etiquetas. La toma aprobada se guarda: el `seed` no garantiza repetirla.

## Dubbing — doblaje que conserva la voz del hablante (`dubbing_v2`)

Otra puerta del mismo proveedor, con gramática propia: **no hay texto que redactar**. Se le da el clip y el idioma destino; transcribe, traduce y vuelve a decir cada línea clonando la voz del hablante. Todo lo de abajo se leyó el 2026-10-29 en [docs/overview/capabilities/dubbing](https://elevenlabs.io/docs/overview/capabilities/dubbing), la referencia de la API ([create-project](https://elevenlabs.io/docs/api-reference/dubbing/create-project), [create-language-target](https://elevenlabs.io/docs/api-reference/dubbing/language-targets/create-language-target), [get-language-target](https://elevenlabs.io/docs/api-reference/dubbing/language-targets/get-language-target)), el centro de ayuda y [elevenlabs.io/pricing/api](https://elevenlabs.io/pricing/api).

**No hace lipsync.** Centro de ayuda: *"At the moment, ElevenLabs does not offer lip syncing as part of Dubbing. Lip sync is available in Image & Video, Flows, and Studio via third party models."* El "Sync 3" de su app es el modelo de sync. labs, y **la API de Image & Video no lo expone** (solo la app web; además esa API pide plan Pro o superior).

### Flujo por API (proyecto + idioma)
1. `POST /v1/dubbing/project` con `file` (≤ 3 GiB) o `source_url`, `source_language` opcional (se autodetecta) y `model_id` `dubbing_v2` (por defecto) o `dubbing_v1`. El modelo queda fijo para todo el proyecto. `target_language` opcional crea el primer idioma en la misma llamada.
2. Esperar `status: ready` (transcrito).
3. `POST /v1/dubbing/project/{id}/language` con `target_language` (BCP-47) y `voice_settings` opcional. Se cobra un doblaje por cada idioma.
4. Esperar `completed`. `outputs` trae **`lossless_audio` (FLAC)** y **`subtitles` (WebVTT)**, con URLs firmadas que vencen en 1 hora. No hay un campo de video ni stems separados en esta API.
- `cloning_strength` 0 a 10 (def. 7). Más alto se parece más al hablante, pero puede sonar menos natural entre idiomas muy distintos y arrastrar más acento original.
- La API vieja (`POST /v1/dubbing`) sigue documentada, con `drop_background_audio`, `highest_resolution`, `watermark`, `disable_voice_cloning`, `num_speakers` y otros campos.

### Idiomas (Dubbing v2)
Español con dialectos `es-MX`, `es-AR`, `es-CL`, `es-ES`; francés `fr` (`fr-FR`, `fr-CA`); chino `zh` (`zh-TW`) y **mandarín `cmn`** como entrada propia. *"Dubbing v1 does not support dialects."*

### Música y fondo
*"The original background audio is retained"*: separa la voz por dentro, la dobla y vuelve a mezclar el fondo. **El FLAC que devuelve trae la mezcla**, no la voz sola. Para pasarlo a un lipsync (que quiere la voz limpia) hay que aislar la voz después, p. ej. con Voice Isolator (<costo interno>/min). `drop_background_audio` (API vieja) quita el fondo del doblaje.

### Salida, límites y precio
- *"Dubbed video is a high-quality preview, not a production master"* (suele salir a 1080p). Para producción, bajar el audio y reemplazar la pista del video original. Audio estéreo como máximo en v2.
- Planes: crear y descargar doblajes por API está en todos los planes; en el gratuito llevan marca de agua. Editar la transcripción y regenerar por API (v2) es solo Enterprise. Hasta 3 doblajes simultáneos en planes self-serve.
- **Precio** (pricing/api, 2026-10-29): **Dubbing v2 <costo interno> por minuto** de fuente, por idioma; v1 <costo interno> (sin marca de agua). El proyecto cobra un idioma por adelantado al crearse, y un fallo de v2 no se cobra. Si un clip de 27 s cuesta 27/60 del minuto o el minuto completo **no está verificado**.

### Gotchas del doblaje
- **El clon puede negarse.** La API devuelve un aviso `voices_not_permitted` con los `speaker_ids` *"whose voices were not permitted for cloning. The dub used a replacement voice"*. Es decir, entrega con **otra voz** sin fallar. Con una voz de origen sintética (TTS o cambiador de voz) ya se vio un bloqueo de clon instantáneo (§5). Revisar `warnings` en cada idioma antes de dar el doblaje por bueno.
- La traducción es automática y en v2 no se puede corregir por API fuera de Enterprise. Una línea mal traducida obliga a usar la app o a cambiar de flujo (TTS propio con el texto corregido).
- Clips con música: la separación interna puede dejar restos de música en la voz o voz en el fondo (sin medir).

## 8. Historial

- 2026-10-01 — ficha creada desde la doc oficial de ElevenLabs (modelos, guía de prompting v4/v3, API de TTS, Dialogue, biblioteca, diseño, IVC, precios) para `eleven_v4`, lanzado el 2026-09-28. Motivo: prerrequisito del torneo de voz 2026-10.
- 2026-10-06 — nueva §3b (el prompt de cada párrafo con etiquetas). Motivo: `locutar` del motor AVE aprendió a generar con ElevenLabs y muestra la §3b de la ficha del proveedor de cada voz; sin esta sección, una pieza de v4 habría mostrado las reglas de Gemini. Ese mismo día un clon rápido etiquetado solo `language: es` (sin `accent`) sonó «de España» con `eleven_multilingual_v2`; rehecho con `accent: es-mexican` y usado con v4, sonó mejor. Fueron dos cambios a la vez, así que la causa no está aislada; la plantilla C ya pedía el acento.
- 2026-10-06 (tarde) — §3b regla 6: la acotación del guion se vuelve etiqueta en inglés o va a la dirección; el nombre del personaje se quita. Misma decisión que la regla 8 de la ficha de Gemini TTS.
- 2026-10-29 — nueva sección Dubbing (`dubbing_v2`): flujo de proyecto e idioma por API, idiomas (es-MX, fr, cmn), fondo retenido en la mezcla, salida FLAC más WebVTT, precio <costo interno>/min, aviso `voices_not_permitted`, y que ElevenLabs no hace lipsync en Dubbing (su "Sync 3" es de sync. labs y no está en la API). Motivo: torneo de cambio de idioma de clips con lipsync.
