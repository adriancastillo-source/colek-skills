---
herramienta: InfiniteTalk (MeiGen-AI)
modelo-vigente: InfiniteTalk sobre Wan2.1-I2V-14B-480P; en fal el slug es `infinitalk` (sin segunda "e"), en wavespeed `infinitetalk`
dominio: video
updated: 2026-08-13
status: vigente
---

# Ficha: InfiniteTalk (talking head / video dubbing audio-driven)

## Identidad

Framework de **sparse-frame video dubbing**: sincroniza labios, cabeza, cuerpo y expresiones con un AUDIO dado. Variantes: **I2V** (imagen + audio → presentador hablando), **V2V** (video + audio → re-doblaje), single/multi-persona, y `single-text` en fal (texto + voz TTS integrada). Elegirlo para: presentador/avatar hablando a cámara desde una foto, o re-doblar un video existente. **Regla rectora: aquí el prompt es SECUNDARIO — el audio manda** (y en V2V, la cámara la manda el video fuente). No elegirlo para escenas de acción o cámara dirigida por texto.

## Gramática oficial

Fuentes: README github.com/MeiGen-AI/InfiniteTalk + fal.ai/models/fal-ai/infinitalk/api (+ /video-to-video, /single-text) + wavespeed.ai/docs/docs-api/wavespeed-ai/infinitetalk. Consultadas 2026-08-13.

- **El prompt de texto es condicionamiento de escena, no de sync:** describe "scene, pose, or behavior" (wavespeed). **Corto y en inglés** — la doc de wavespeed advierte literal que prompts largos o en otro idioma producen "analysis errors, resulting in noisy and unexpected videos". Ejemplo del playground de fal: `"A woman with colorful hair talking on a podcast."` La restricción de inglés aplica al PROMPT; el audio puede ser en español (el dubbing multilingüe es use case anunciado).
- **Sin negative prompt** en los providers.
- **Inputs:** `image_url` (I2V) o `video_url` (V2V) + `audio_url` (mp3/ogg/wav/m4a/aac) + `prompt`. Imagen con aspect ratio distinto al output → **resize + center crop automático** (encuadres descentrados pierden al sujeto).
- **Truco oficial para >1 min:** I2V se degrada (~1 min, color shift progresivo); el README recomienda convertir la imagen en un video con paneo/zoom lento y usar **V2V**, que sí es "unlimited".
- **Multi-persona (wavespeed `/multi`):** imagen con ambas personas + audio por lado + orden de habla (left-to-right / right-to-left / simultáneo).

## Plantilla (I2V "presentador a cámara")

Prompt de 1-2 frases, inglés, sin listas de estilo ni negativos:

```
[SUBJECT: presenter, edad/look breve] speaks [energía: confidently/calmly/enthusiastically] to the camera, [gesto/expresión: subtle hand gestures, warm expression], [escena breve: modern studio background, soft lighting].
```

Preparación de inputs (pesa más que el prompt):
- **Imagen:** frontal o 3/4, boca visible y bien iluminada, alta resolución, sujeto centrado, ya en el aspect ratio destino (16:9 o 9:16).
- **Audio:** limpio, sin música pesada de fondo, ritmo natural (no acelerado); duración ≤ `num_frames`/~25 s.

## Parámetros (fal `infinitalk`)

- `num_frames`: 41-721 en I2V (default 145 ≈ ~5.8 s); 81-129 en V2V (>81 factura 1.25x).
- `resolution`: `480p` (default) / `720p` — no hay más.
- `acceleration`: `none` (máxima calidad) / `regular` (default) / `high`.
- `seed` (default 42) — fijarlo para reproducibilidad.
- No exponen fps (~25 fps por la familia Wan-audio — cifra no-oficial, estimarla así) ni CFG de audio.
- **Costo:** fal ≈ $0.20/s (720p x2, página del playground); **wavespeed mucho más barato**: $0.03/s (480p) / $0.06/s (720p), mín 5 s, tope 600 s, y ofrece `mask_image` (región a animar).

## Gotchas documentados

- **Lip-sync flojo → el fix oficial es subir el audio CFG (3-5)**, pero los providers NO lo exponen: en fal/wavespeed la única palanca es mejorar el audio (limpio, más lento).
- I2V >1 min: color shift (usar el truco imagen→video + V2V).
- V2V imita la cámara del video fuente "aunque no idénticamente" (README).
- Audio más largo que `num_frames` → se corta al tope de frames.
- wavespeed: `mask_image` con la imagen completa puede devolver video **negro** — la máscara es para regiones parciales.
- Center-crop automático: verificar el encuadre del sujeto antes de gastar.

## Folklore de comunidad

(Capa más débil que la oficial en este modelo — blogs de comunidad, sin hilos de Reddit sustantivos localizados; consultados 2026-08-13.)

- Especificar emoción + acción concreta (`"speaks enthusiastically, gesturing with both hands"`), anclar orientación (`"turns slightly toward the camera with a warm smile"`), y si la cara sale rígida añadir `micro-expressions, subtle head turns` — `anecdótico` (infinitetalk.net, runcomfy).
- Emparejar energía del prompt con la del audio (voz calmada → `"speaks quietly and thoughtfully"`) — `anecdótico`, pero coherente con que el audio manda.
- Sujeto frontal + iluminación consistente + fuente de alta resolución mejoran el sync — `anecdótico` (tutoriales ComfyUI), coherente con la doc.

## Iteración

Con `seed` fijo, cambiar UNA cosa por ronda — y antes de tocar el prompt, revisar los inputs: la mayoría de los defectos (sync, rigidez, encuadre) se corrigen en el audio o la imagen fuente, no en el texto. Piezas >30 s: partir el audio en cortes o usar wavespeed (hasta 10 min).

## Historial

- 2026-08-13 — alta de la ficha (para el torneo InfiniteTalk + Seedance 2.5).
