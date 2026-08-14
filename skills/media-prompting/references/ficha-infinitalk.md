---
herramienta: InfiniteTalk (MeiGen-AI)
modelo-vigente: InfiniteTalk (pesos abiertos, NeurIPS 2025; servido en fal como `fal-ai/infinitalk`)
dominio: video
updated: 2026-08-14
status: descartado-colek
---

# Ficha: InfiniteTalk

## Identidad

Modelo **audio-driven** de MeiGen-AI (pesos abiertos): recibe UNA imagen + UNA pista de audio y anima
al/los personajes hablando esa pista **TAL CUAL** — no re-genera la voz (a diferencia de
Seedance/Kling/Veo, que re-actúan todo audio de entrada). Elegirlo cuando **la voz y la
interpretación ya existen y son intocables** (TTS de personaje, locutor real): apego al guion 100%
por construcción. No compite en puesta en escena: **anima el cuadro que le des, sin cortes de plano**
— los planos los pone la edición (receta de capas: una toma por plano).

⚠️ **Nombre secuestrado por clones SEO:** `infinitetalk.net` y similares NO son el modelo — venden
otro servicio detrás del nombre. Un modelo open-weights se usa en su endpoint de proveedor (fal,
WaveSpeed, Replicate), nunca en el dominio homónimo.

## Gramática oficial (contrato del endpoint)

Fuente: fal.ai/models/fal-ai/infinitalk/api (schema, consultado 2026-08-13).

- **Inputs:** `image_url` (obligatorio) · `audio_url` (obligatorio) · `prompt` (texto que guía el
  MOVIMIENTO, no el habla) · `num_frames` (41–721; default 145) · `resolution` (480p/720p) ·
  `seed` · `acceleration`.
- **El prompt NO lleva diálogo** — el habla ES el audio. El prompt describe: quiénes están en cuadro,
  quién habla en qué orden, gestos y reacciones del que escucha.
- **Variantes:** video-to-video (re-anima la boca de un video existente) · single-text (TTS interno,
  con voces propias) · **multi** (`first_audio_url` + `second_audio_url`, orden de habla
  configurable) — pero multi está **capada a 81–129 frames (~3–5 s)** y factura 1.25× sobre 81.

## Plantilla

```
[N characters] at [setting], having a conversation, taking turns speaking.
The [descripción del personaje 1, posición] speaks first, then the [personaje 2, posición] replies,
alternating naturally. Subtle head movements and gestures while each one talks;
the listener reacts quietly.
```
Parámetros: `num_frames = floor(duración_audio × 25) − 2` · `resolution: 720p` para entregar.

## Parámetros

- 41–721 frames (~1.6–28.8 s @25fps) por toma en el endpoint estándar.
- Precio fal: ~$0.2/s base, 720p ×2 → **~$0.41/s medido** (con ±$1.2 de ambigüedad en la corrida).

## Gotchas documentados (verificados con gasto propio, torneo Foliatti 2026-08-13)

- **`num_frames` vs duración es ESTRICTO:** el endpoint exige audio ≥ num_frames/25 con decimales;
  redondear al frame exacto rebota 422 ("Audio is too short"). Restar 2 frames al cálculo.
- **Es LENTO:** ~440 frames tardan >15 min (difusión frame a frame). Poll con timeout ≥45 min, o el
  cliente muere con el job vivo en fal (rescatable por `request_id`).
- **Passthrough de audio verificado:** correlación de envolvente r=1.000, desfase 0 ms — la pista
  sale intacta, con las pausas e interpretación originales.
- **Dos personajes en un cuadro con pista combinada: funciona** — anima a ambos alternando con el
  turno del audio (una imagen con los 2, pista con las voces intercaladas). La variante multi formal
  no hace falta para escenas cortas… y por su tope de frames tampoco alcanza.

## Folklore de comunidad

- WaveSpeed lo sirve ~10× más barato ($0.03–0.06/s) — `sin verificar` (precios secundarios
  2026-08-13); si el volumen crece, medir ahí antes de asumir.
- "Hasta 10 min por clip" — es de la variante/serving largo de WaveSpeed, NO del endpoint fal
  (tope 721 frames) — no confundir capa.

## Iteración

La voz no se itera aquí (es input). Iterar = cambiar imagen de entrada (pose, encuadre, boca
entreabierta) o el prompt de movimiento. Un cambio por ronda.

## Historial

- 2026-08-13 — alta de la ficha (torneo Foliatti R1; runner operativo en
  `agentic-video-engine/scripts/infinitalk.mjs`).
- 2026-08-14 — **status → descartado-colek.** En su prueba justa (plano medio, caras grandes, pista
  TTS expresiva propia, 18.6 s) el veredicto humano fue lapidario: *"pésimo comparado contra Seedance
  o incluso vs Kling; no es opción aplicable en nada"*. El passthrough perfecto del audio (r=1.000,
  su única ventaja) no compensa la calidad de animación. La ficha se conserva por si el modelo
  mejora (pesos abiertos, itera rápido) — re-evaluar solo con versión nueva, no re-probar esta.
