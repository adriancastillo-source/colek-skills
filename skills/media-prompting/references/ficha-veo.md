---
herramienta: Veo (Google)
modelo-vigente: Veo 3.1 (oct-2025; sigue siendo el modelo de first/last frame de Google a 2026-08-15)
dominio: video
updated: 2026-08-15
status: vigente
---

# Ficha: Veo 3.x

## ⚠️ Desambiguación — Veo 3.1 NO es Gemini Omni

Google tiene **dos** modelos de video vivos y **gramáticas distintas**. Confundirlos es el error más caro de esta ficha (ya ocurrió: 2026-08-15).

| | **Veo 3.1** (esta ficha) | **Gemini Omni Flash** (`gemini-omni-flash-preview`) |
|---|---|---|
| First + last frame | **Sí** — "Frames to Video" en Flow | **No.** Oficial: *"Video extension and video interpolation (generating video between a first and last frame) are not supported."* |
| Imagen inicial sola | Sí | Sí, con tag `<FIRST_FRAME>` |
| Refs de personaje/objeto | "Ingredients to Video", aludidas en lenguaje natural, **sin tags** | Tags `<IMAGE_REF_0>`, `<IMAGE_REF_1>`… numerados desde 0 |
| Negativos | **Exclusión descriptiva** ("a landscape with no buildings") | **Negación simple** ("No dialogue", "No extra sound effects") |
| Timeline | `[MM:SS-MM:SS]` | `[0-3s] … [3-6s] …` |

**Si el trabajo exige interpolar entre dos imágenes → Veo 3.1 en Flow, no Omni.** Y **no se trasplanta sintaxis entre los dos** (los tags de Omni no existen en Veo; los negativos descriptivos de Veo son lo contrario de lo que pide Omni).

Fuente Omni: ai.google.dev/gemini-api/docs/omni, consultada 2026-08-15. *"Veo 4" no es nombre oficial* — es apodo de blogs de terceros para Omni; el ID real es `gemini-omni-flash-preview`. Omni merece **ficha propia**; hasta que exista, esta tabla es el único puente y no basta para redactar un prompt de Omni.

## Identidad

Modelo de video de Google, fuerte en **exteriores/atmósfera y adherencia cinematográfica** (la recomendación del propio Higgsfield). Clips cortos (4/6/8 s) con audio nativo rico. Elegirlo para: planos atmosféricos, realismo fotográfico, beats cortos con diálogo, y **todo lo que necesite first/last frame**. **Es el más corto de los tres grandes** (Seedance 2.5 = 30 s, Kling 3.0 = 15 s): escenas largas se encadenan con first/last frame o extensión en Flow.

Vigencia verificada 2026-08-15: "Frames to Video" (first+last) sigue activo en Flow y desde la actualización de ene-2026 **lleva audio**, igual que Ingredients to Video y Extend; Ingredients to Video ganó además salida **vertical nativa**. Fuente: blog.google/innovation-and-ai/products/veo-updates-flow/, consultada 2026-08-15.

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

- **Pedirle first/last frame a Gemini Omni no falla: simplemente no existe** (ver desambiguación arriba). Si el brief dice "de esta imagen a esta otra", el motor es Veo 3.1 en Flow.
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

- 2026-08-15 — corregido el frontmatter (decía que Google "pivotó a Omni como plataforma": Omni es un **modelo** con gramática propia, no una plataforma) y añadida la desambiguación Veo 3.1 vs Gemini Omni. Motivo: una sesión pidió un prompt "para Google Omni" con first/last frame y esta ficha la mandó a Veo sin avisar que Omni no interpola. Pendiente: ficha propia de Omni.
- 2026-08-13 — alta de la ficha (Veo 3.1).
