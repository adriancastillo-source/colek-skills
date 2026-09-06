---
herramienta: Gemini TTS (Gemini API speech generation)
modelo-vigente: gemini-3.1-flash-tts-preview (hermanos: gemini-2.5-flash-tts, gemini-2.5-pro-tts)
dominio: voz
updated: 2026-08-21
status: vigente
---

# Ficha de prompting — Gemini TTS

## 1. Identidad

TTS "promptable" de Google: la actuación se dirige con lenguaje natural dentro del mismo texto de entrada (no hay campos separados de estilo en la API). Elegirlo para locución de personaje con dirección actoral fina y castings rápidos (30 voces prebuilt). No elegirlo para audio >60 s por llamada (degrada, ver §5) ni cuando se necesita clonación de voz (eso es ElevenLabs).

## 2. Gramática oficial

Fuentes: guía oficial de speech generation ([ai.google.dev/gemini-api/docs/speech-generation](https://ai.google.dev/gemini-api/docs/speech-generation), leída 2026-08-20) y blog oficial Google AI DevRel ([dev.to/googleai/how-to-prompt-gemini-31s-new-text-to-speech-model-24bb](https://dev.to/googleai/how-to-prompt-gemini-31s-new-text-to-speech-model-24bb), leído 2026-08-20).

- **Request:** `generateContent` con `responseModalities: ["AUDIO"]`; voz e idioma van en `speechConfig` (`prebuiltVoiceConfig.voiceName`, `languageCode`), NUNCA en el texto. Salida PCM 24 kHz mono.
- **Nivel básico (oficial):** instrucción antepuesta en texto plano — `Say in a spooky whisper: "..."`. Sirve para una línea con una sola intención.
- **Nivel estructurado (oficial):** encabezados markdown — `# AUDIO PROFILE`, `## THE SCENE`, `### DIRECTOR'S NOTES` (Style / Pace / Accent), `### SAMPLE CONTEXT`, `#### TRANSCRIPT`. Documentado literalmente en la guía oficial; es el formato para personaje sostenido.
- **Audio tags inline (oficial):** `[whispers]`, `[sighs]`, `[laughs]`, `[excitedly]`, `[bored]`, `[very fast]`, `[very slow]`, `[shouting]`, `[sarcastically, one painfully slow word at a time]`… Cita oficial: *"There is no exhaustive list on what tags do and don't work, we recommend experimenting."*
- **Tags en inglés aunque el transcript no lo sea** — recomendación oficial textual: *"if your transcript is not in English, we recommend that you still use English audio tags."*
- **Ritmo:** en lenguaje natural ("~15% faster than normal") o tags `[very fast]`/`[very slow]` por tramo. El parámetro numérico de la API (`speakingRate`) no es confiable (verificado en producción el estudio 2026-08; la doc oficial no lo ofrece para estos modelos).
- **Límite:** 32k tokens por sesión TTS (oficial); mantener el transcript en pocos minutos.
- **Anti-sobreactuación (oficial):** no describir todo — *"giving the model space to fill in the gaps helps naturalness"*.

## 3. Plantillas con slots

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

## 4. Parámetros

- 30 voces prebuilt (catálogo con característica oficial de cada una en la doc); la API no valida el nombre — un typo genera con otra cosa.
- `languageCode` (p. ej. `es-MX`) va en config, no en el prompt.
- Salida: PCM 24 kHz mono 16-bit (envolver a WAV es del cliente).
- **Cuota diaria de `gemini-3.1-flash-tts`, medida en producción (2026-08-20/21):** nivel gratuito = **10 requests/día** (`quotaId …PerDayPerProjectPerModel-FreeTier`); **Nivel 1 (facturación vinculada) = 100/día** (`…PerDayPerProjectPerModel`) — vincular facturación NO quita este tope en el preview, solo sube de 10 a 100. Es **por proyecto de Google Cloud**: otro proyecto = otro contador (de ahí el pool de claves). Los "retry in" del 429 son poco fiables (pasaron de "7 min" a "23 h" en 20 min); confiar en la cuenta propia, no en el reloj de Google. Aumento real: formulario de cuota (aistudio.google.com/rate-limit).

## 5. Gotchas documentados

- **Lee su propia dirección en voz alta** si las notas no están separadas del transcript con instrucción explícita. Mitigación: preámbulo *"Do NOT speak these notes. Speak ONLY the lines under TRANSCRIPT."* (guía LiveKit, ver §6; el bug está reproducido en producción el estudio).
- **Líneas de 1 palabra + persona larga → "respuesta sin audio"** casi determinista (reproducido el estudio 2026-07-07: 10-15 reintentos fallidos; foro oficial confirma el bug sin fix: [discuss.ai.google.dev/t/108163](https://discuss.ai.google.dev/t/gemini-2-5-pro-preview-tts-not-working-constant-no-audio-generated-error/108163)). Mitigación para monosílabos: estilo mínimo directivo ("identidad en 1 frase + 'di únicamente la palabra, [tono]'") — SOLO para esa línea, nunca como recorte permanente de identidad.
- **Degradación >60 s** en `gemini-3.1-flash-tts-preview`: medición de terceros (ttsaudit.com, 2026): 90% de generaciones >1 min degradan (ej. 92/100 primeros 16 s vs 34/100 último minuto). Generar por línea/segmento corto.
- **Nunca instruir "flat / monotone / quiet"** — apaga la voz entera; describir melodía en positivo ("phrases end flat or slightly downward" sí funciona: es melodía, no energía).
- **La consistencia entre llamadas NO está documentada por Google** y en la práctica la actuación varía por semilla con prompt idéntico: tirar 2-3 tomas y elegir sigue siendo el método.

## 6. Folklore de comunidad

Fuente principal: guía LiveKit ([livekit.com/blog/gemini-3.1-flash-tts-prompting-guide](https://livekit.com/blog/gemini-3.1-flash-tts-prompting-guide), leída 2026-08-20) — proveedor serio, no oficial. Confianza: `reproducible` salvo nota.

- Evitar apóstrofes en encabezados (`DIRECTOR'S` puede leerse en voz alta) → usar `DIRECTOR NOTES` o `### PERFORMANCE`.
- Comas entre cláusulas con tags; puntos solo en fin de oración real; elipsis (1-2 por enunciado) y em-dash para micro-pausas.
- No citar palabras literales del transcript dentro de las notas de Style/Pace (confunde al modelo y puede duplicarlas). `anecdótico`.
- Aislar la palabra a enfatizar entre `...` en el TEXTO (no en el estilo) — coincide con práctica reproducida en producción.

## 7. Iteración

Cambio único por tiro: primero persona (timbre), luego style (carácter), luego dirección de línea, al final tags inline. Anclar lo ganado: cuando un bloque de persona suena bien, se congela textual (en el estudio: receta sellada) y solo se itera la capa de línea. Para juzgar "¿suerte o proceso?": 3 tiros del MISMO prompt; si el carácter no se sostiene, falta especificación — subir de plantilla A a B, no engordar la prosa.

**Lecciones del primer casting real con estas plantillas (una serie de sketches EP2 V3, 2026-08-21):**
- **El formato no es universal.** La plantilla B (Director's Notes en inglés) ganó el casting de un personaje recurrente (3 tiros consistentes, comedia deadpan); a RH la volvió irreconocible en 5 rondas, y ganó la plantilla A en español con su persona previa + UNA frase nueva. Probar ambas por personaje; "la base que ya sonaba + cambio mínimo" vence a reescribir.
- **Declarar el género** (`Scene: a deadpan COMEDY sketch… no gravitas`) quitó el drama que el modelo ponía por defecto ante "irony" + intensidad 6; bajar a intensidad 4 ayudó.
- **Las direcciones de línea pertenecen al registro de la persona vigente**: direcciones "seco/deadpan absoluto" escritas para una persona sobria aplanaron a la persona juguetona aunque el bloque de identidad fuera el correcto.
- **Acciones visuales nunca al TTS** (van al prompt de video); **dirección por línea siempre**.

## 8. Historial

- 2026-08-21 — ficha creada desde investigación documental (corrida una serie de sketches-ep2-v3); modelo motivador: `gemini-3.1-flash-tts-preview`.
- 2026-08-21 (tarde) — cuota medida por tier y lecciones del casting un personaje recurrente/RH.
