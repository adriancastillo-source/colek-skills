---
herramienta: Veo (Google)
modelo-vigente: Veo 3.1 (oct-2025; no existe Veo 4 a 2026-08 — Google pivotó a Gemini Omni como plataforma multimodal)
dominio: video
updated: 2026-08-13
status: vigente
---

# Ficha: Veo 3.x

## Identidad

Modelo de video de Google, fuerte en **exteriores/atmósfera y adherencia cinematográfica** (la recomendación del propio Higgsfield). Clips cortos (4/6/8 s) con audio nativo rico. Elegirlo para: planos atmosféricos, realismo fotográfico, beats cortos con diálogo. **Es el más corto de los tres grandes** (Seedance 2.5 = 30 s, Kling 3.0 = 15 s): escenas largas se encadenan con first/last frame o extensión en Flow.

## Gramática oficial

Fuente: Google Cloud Blog — "Ultimate prompting guide for Veo 3.1" (2025-10-15, cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1). Consultada 2026-08-13.

- **Fórmula de 5 slots:** `[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]`. Ej. oficial: *"Medium shot, a tired corporate worker, rubbing his temples in exhaustion, in front of a bulky 1980s computer in a cluttered office late at night… Retro aesthetic, shot as if on 1980s color film, slightly grainy."*
- **Timestamp prompting:** `[MM:SS-MM:SS] descripción del beat. SFX: … Emotion: …` (ej. oficial: 4 segmentos de 2 s en un clip de 8 s).
- **Audio por prefijos de línea:** `SFX: thunder cracks…` · `Ambient noise: the quiet hum of…` · música también vía `SFX: a swelling orchestral score begins to play.`
- **Diálogo:** entre comillas — `A woman says, "We have to leave now."` Lip-sync automático.
- **Referencias:** SIN sintaxis `@` — "ingredients to video" sube imágenes y el prompt las alude en lenguaje natural: *"Using the provided images for the detective and the office setting, create a medium shot of…"*. First/last frame: dos imágenes + prompt del movimiento entre ambas. Flujo oficial recomendado: generar las referencias con la familia Gemini de imagen (Nano Banana).
- **Negativos: exclusión DESCRIPTIVA, no "no X":** oficial — *"a desolate landscape with no buildings or roads"* mejor que *"no man-made structures"*.

## Plantilla

```
[SHOT TYPE + camera movement], [SUBJECT: age, look, wardrobe], [ACTION],
[CONTEXT: location, time, background]. [STYLE & AMBIANCE: lighting, film stock, grade].

[Timeline opcional:]
[00:00-00:0X] [beat 1]. SFX: [sound].
[00:0X-00:08] [beat 2]. Emotion: [emotion].

[CHARACTER] says: "[dialogue line]" (no subtitles)
Ambient noise: [cama sonora]. SFX: [efectos]. [descripción de música | sin música → describirlo en positivo]

[Con refs:] Using the provided images for [X] and [Y], create [shot].
```

## Parámetros

- Duración: 4, 6 u 8 s por clip (tope duro).
- Resolución: 720p / 1080p. Aspect ratios: 16:9 y 9:16 (el 1:1 que circula es workaround de comunidad, no oficial).

## Gotchas documentados

- **Subtítulos que "sangran"** al pedir diálogo — el gotcha más citado del modelo (ver folklore para la mitigación).
- Tope duro de 8 s por clip; encadenar con first/last frame o extensión en Flow.
- "Add/remove object" corre sobre **Veo 2** y no genera audio (oficial).
- Todo output lleva watermark SynthID (oficial) — considerar en entregables.
- Cámara oficial: dolly, tracking, crane, aerial, slow pan, POV; wide/close-up/extreme close-up, low angle, two-shot; shallow/deep focus, macro, wide-angle.

## Folklore de comunidad

- **Colon antes de la comilla** (`Character says: "line"`) + refuerzo `(no subtitles)` para suprimir subtítulos — `reproducible` (guía snubroot en GitHub, adoptado masivamente; ~95% de efectividad reportada por su autor, sin medición independiente).
- `"(thats where the camera is)"` tras describir la posición de cámara — `anecdótico` (snubroot).
- Plantilla textual de personaje repetida entre tomas (`[NAME], [AGE] [ETHNICITY]…, wearing [CLOTHING]`) para consistencia sin refs — `anecdótico`; el camino oficial es ingredients-to-video.
- "realistic physics" para manos/física — `anecdótico`, sin fix oficial.
- Listas de negativos ("no text overlays, no watermarks…") — `anecdótico` y contrario a la recomendación oficial de exclusión descriptiva; preferir lo oficial.

## Iteración

Un beat/slot por ronda manteniendo los otros 4 slots idénticos. Para series consistentes: mismas imágenes de ingredients en cada toma + aludirlas igual. Lo que 3.1 rompió de 3.0: i2v ahora genera audio/diálogo — prompts i2v "mudos" de la era 3.0 quedaron obsoletos.

## Historial

- 2026-08-13 — alta de la ficha (Veo 3.1).
