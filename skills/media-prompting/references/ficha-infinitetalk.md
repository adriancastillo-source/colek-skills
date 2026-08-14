---
herramienta: InfiniteTalk (MeiGen-AI)
modelo-vigente: InfiniteTalk (pesos abiertos, NeurIPS 2025; servido en fal como `fal-ai/infinitalk` — sin la segunda "e")
dominio: video
updated: 2026-08-14
status: descartado-colek
---

# Ficha: InfiniteTalk

> **Status: descartado-colek (2026-08-14, torneo Foliatti).** En su prueba justa (plano medio, caras grandes, pista TTS expresiva propia, 18.6 s) el veredicto humano fue lapidario: *"pésimo comparado contra Seedance o incluso vs Kling; no es opción aplicable en nada"*. Su única ventaja real —passthrough perfecto del audio— no compensa la calidad de animación. La ficha se conserva por si el modelo mejora (pesos abiertos, itera rápido) — re-evaluar solo con versión nueva, no re-probar esta.

## Identidad

Modelo **audio-driven** de MeiGen-AI (pesos abiertos, base Wan2.1-I2V-14B-480P): recibe UNA imagen + UNA pista de audio y anima al/los personajes hablando esa pista **TAL CUAL** — no re-genera la voz (a diferencia de Seedance/Kling/Veo, que re-actúan todo audio de entrada). Elegirlo cuando **la voz y la interpretación ya existen y son intocables** (TTS de personaje, locutor real): apego al guion 100% por construcción. No compite en puesta en escena: **anima el cuadro que le des, sin cortes de plano** — los planos los pone la edición.

⚠️ **Nombre secuestrado por clones SEO:** `infinitetalk.net` y similares NO son el modelo — venden otro servicio detrás del nombre. Un modelo open-weights se usa en su endpoint de proveedor (fal, WaveSpeed, Replicate), nunca en el dominio homónimo.

## Gramática oficial (contrato del endpoint + README)

Fuentes: fal.ai/models/fal-ai/infinitalk/api (schema) + github.com/MeiGen-AI/InfiniteTalk (README). Consultadas 2026-08-13.

- **Inputs:** `image_url` (obligatorio) · `audio_url` (obligatorio; mp3/ogg/wav/m4a/aac) · `prompt` (texto que guía el MOVIMIENTO, no el habla) · `num_frames` (41–721; default 145) · `resolution` (480p/720p — no hay más) · `seed` · `acceleration` (none/regular/high).
- **El prompt NO lleva diálogo** — el habla ES el audio. El prompt describe: quiénes están en cuadro, quién habla en qué orden, gestos y reacciones del que escucha. Corto y en inglés (la doc de WaveSpeed advierte que prompts largos o en otro idioma ensucian el resultado). El audio sí puede ser en español.
- **Imagen con aspect ratio distinto al output → resize + center crop automático** — sujeto centrado o se pierde.
- **Variantes:** video-to-video (re-anima un video existente; imita la cámara del fuente "aunque no idénticamente" — README) · single-text (TTS interno) · multi (`first_audio_url` + `second_audio_url`, orden de habla configurable) — pero multi está **capada a 81–129 frames (~3–5 s)** y factura 1.25× sobre 81.
- **Trucos oficiales del README:** I2V se degrada tras ~1 min (color shift progresivo) → convertir la imagen en video con paneo/zoom lento y usar V2V (ese sí "unlimited"). Lip-sync flojo → subir audio CFG 3–5 (NO expuesto en fal/WaveSpeed: ahí la única palanca es mejorar el audio).

## Plantilla

```
[N characters] at [setting], having a conversation, taking turns speaking.
The [descripción del personaje 1, posición] speaks first, then the [personaje 2, posición] replies,
alternating naturally. Subtle head movements and gestures while each one talks;
the listener reacts quietly.
```

Parámetros: `num_frames = floor(duración_audio × 25) − 2` · `resolution: 720p` para entregar. Imagen frontal/3-4, boca visible, ya en el ratio destino; audio limpio a ritmo natural.

## Parámetros

- 41–721 frames (~1.6–28.8 s @25fps) por toma en el endpoint estándar de fal.
- Precio fal: ~$0.2/s base, 720p ×2 → **~$0.41/s medido** (con ±$1.2 de ambigüedad en la corrida).

## Gotchas documentados (verificados con gasto propio, torneo Foliatti 2026-08-13)

- **`num_frames` vs duración es ESTRICTO:** el endpoint exige audio ≥ num_frames/25 con decimales; redondear al frame exacto rebota 422 ("Audio is too short"). Restar 2 frames al cálculo.
- **Es LENTO:** ~440 frames tardan >15 min (difusión frame a frame). Poll con timeout ≥45 min, o el cliente muere con el job vivo en fal (rescatable por `request_id`).
- **Passthrough de audio verificado:** correlación de envolvente r=1.000, desfase 0 ms — la pista sale intacta, con las pausas e interpretación originales.
- **Dos personajes en un cuadro con pista combinada: funciona** — anima a ambos alternando con el turno del audio (una imagen con los 2, pista con las voces intercaladas). La variante multi formal no hace falta para escenas cortas… y por su tope de frames tampoco alcanza.

## Folklore de comunidad

- WaveSpeed lo sirve ~10× más barato ($0.03–0.06/s) — `sin verificar` (precios secundarios 2026-08-13); si el volumen crece, medir ahí antes de asumir.
- "Hasta 10 min por clip" — es de la variante/serving largo de WaveSpeed, NO del endpoint fal (tope 721 frames) — no confundir capa.
- Emparejar la energía del prompt con la del audio y añadir `micro-expressions, subtle head turns` si la cara sale rígida — `anecdótico` (blogs de comunidad; ojo: varios son los clones SEO del punto de Identidad).

## Iteración

La voz no se itera aquí (es input). Iterar = cambiar imagen de entrada (pose, encuadre, boca entreabierta) o el prompt de movimiento. Un cambio por ronda.

## Historial

- 2026-08-13 — alta de la ficha (torneo Foliatti R1; runner operativo en el motor de video interno).
- 2026-08-14 — **status → descartado-colek** tras la prueba justa del torneo (ver encabezado). Consolidada con la ficha hermana `ficha-infinitalk.md` (slug de fal) en este único archivo.
