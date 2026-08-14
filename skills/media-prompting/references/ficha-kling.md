---
herramienta: Kling (Kuaishou)
modelo-vigente: Kling 3.0 / 3.0 Omni (anunciados 2026-02-05); línea 2.x vigente para t2v/i2v simple
dominio: video
updated: 2026-08-13
status: vigente
---

# Ficha: Kling 2.x / 3.0

## Identidad

Modelo de video de Kuaishou, fuerte en **personajes** (el propio Higgsfield lo recomienda para "personajes en 4K"). 3.0 Omni añade audio/diálogo nativos, multi-shot (hasta 6 shots / 15 s) y voice binding. Elegirlo para: actuación de personajes, diálogo con lip-sync nativo, secuencias cortas multi-shot. La línea 2.x sigue para clips simples de 5/10 s.

## Gramática oficial

Fuentes: kling.ai/quickstart/text-to-video-prompt-guide (fórmula 2.x) + kling.ai/blog/kling-ai-prompt-guide (2026-08-07, marco 3.0) + kling.ai/quickstart/klingai-video-3-omni-model-user-guide (multi-shot, @elements, voice binding). Consultadas 2026-08-13.

- **Fórmula 2.x:** `Subject (descripción) + Subject Movement + Scene (descripción) + (Camera Language + Lighting + Atmosphere)` — los 3 primeros obligatorios. **Image-to-video:** solo `Subject + Movement, Background + Movement` (la imagen ya aporta apariencia; describir SOLO lo que se mueve).
- **Marco 3.0 (blog oficial):** 6 elementos — Subject · Action · Scene · Camera Language · Lighting · Mood. Cita oficial: "Strong cinematic prompts are built from clear scene direction rather than secret formulas."
- **Multi-shot 3.0 Omni:** `Shot [n] ([duración]s): [framing/angle], [contenido], [movimiento de cámara]` — ej. oficial: `"Shot 1 (3s): Mid-shot, background @Image. @Grace sits on the sofa eating cookies as @Alan walks in."` Alterno por timestamps `[00:00 - 00:02] … Audio: …`.
- **Elements/referencias (3.0):** menciones `@Nombre` (`@Grace`, `@Image`). Hasta 7 imágenes (≥300 px, ≤10 MB) — o hasta 4 si además hay video de referencia (1 video de 3-10 s, ≤200 MB).
- **Diálogo (solo 3.0 Omni):** inline con comillas — `@Grace says, "Hey! Watch your dog!"`. Entiende shot-reverse-shot, cross-cutting, voice-over. **Audio/SFX:** línea `Audio:` propia.
- **Voice binding (3.0 Omni):** audio de 5-30 s de UNA persona (fondo limpio) o video de 3-8 s del personaje (extrae apariencia + voz).
- **Negativos:** campo aparte en UI/API 2.x; las guías oficiales NO documentan sintaxis de negativos in-prompt.

## Plantillas

Línea 2.x (t2v):
```
[SUBJECT + 2-4 appearance details]. [SUBJECT MOVEMENT — concreto, que quepa en 5-10 s].
[SCENE: foreground + background]. [FRAMING], [ONE camera movement, pace].
[LIGHTING], [ATMOSPHERE/MOOD].
```

3.0 Omni (multi-shot con audio):
```
Shot 1 ([n]s): [framing], background @Image. @[CharA] [action]. @[CharA] says, "[line]". Audio: [SFX/ambience].
Shot 2 ([n]s): [framing/angle], [action / cut to]. @[CharB] says, "[line]".
Shot 3 ([n]s): [framing], [resolution beat]. Audio: [score/ambience].
[Elements: @CharA = images 1-2 (+ voice audio 5-30s); @CharB = video ref 3-8s.]
```

## Parámetros

- 2.x: 5 s o 10 s; 16:9 / 9:16 / 1:1; modos Standard/Professional.
- 3.0 Omni: hasta 15 s, hasta 6 shots; 1080p/720p según la guía Omni (el "4K nativo" circula en anuncios/terceros, no en la guía de prompting — tomarlo con reserva).

## Gotchas documentados

- Un solo movimiento de cámara por clip; transformaciones simultáneas ("360° + zoom-in") distorsionan — secuenciarlas.
- Movimientos físicos complejos y conteos/números fallan (oficial 2.x); split-screen exige especificar ángulos.
- Términos de luz contradictorios ("golden hour" + "studio lighting") confunden el estilo.
- Con video de referencia: tope de Elements baja a 4 y el audio nativo NO funciona sobre video de input (oficial Omni).
- Cámara vaga ("cinematic movement") da resultados inconsistentes — nombrar framing + movimiento + ritmo.

## Verificado con gasto propio (torneo Foliatti, 2026-08-13)

- **Diálogo nativo en español es-MX: NO confiable** (2/2 corridas de 15 s, vía Higgsfield):
  deformó nombres propios ("Don Fortuno" → "Funutro" / "Fortunino"), rompió una línea completa en
  papilla fonética, añadió interjecciones no escritas ("¡Oh!") y **adoptó acento con mezcla italiana**
  (veredicto de Adrian). Descartado para diálogo es-MX de serie; posible combo video-Kling +
  voice-swap en post (sin medir). — `reproducible (2 corridas)`.
- **Shot-list multi-shot SÍ la obedece** (formato oficial `Shot N (ns):`): CU/OTS/two-shot y
  apertura con llegada de personaje, correctos en ambas corridas. El problema es el audio, no la
  puesta en escena. — `reproducible`.
- **Deforma proporciones del personaje** aun partiendo de start_image: engordó al personaje robusto
  más allá de su diseño (veredicto de Adrian contra el character sheet, corrida 2). En apego a
  referencias de personaje, Seedance 2.5 le ganó con claridad en el mismo caso. — `reproducible
  (consistente con el "morphing object problem" del folklore fal)`.
- **Audio sucio:** risas tipo estudio colgadas al inicio en corrida 1 pese a pedir solo ambiente
  (los negativos in-prompt no tienen respaldo oficial en Kling — ver Gramática). — `anecdótico`.
- **Precio real vía Higgsfield:** 15 s std 16:9 con audio = **30 créditos** (~$1.58 al pack top-up)
  ≈ 2 cr/s. — `medido`.

## Folklore de comunidad

- Énfasis `++elemento++`, negativos in-prompt ("No people, no text overlays"), lentes virtuales ("24mm f/2.8") — `anecdótico`: vienen de fal.ai (guía 2.6 Pro), NO están en docs oficiales.
- Tope práctico de 4 referencias aunque el máximo sea 7 ("más confunde prioridades") — `anecdótico` (fal).
- "Morphing object problem" en clips largos → añadir "maintains exact appearance throughout" o Elements multi-ángulo — `anecdótico` (fal).
- Texto en pantalla: sin sintaxis documentada en ninguna guía oficial — si el texto importa, ponerlo en post.

## Iteración

Un cambio por ronda. Identidad de personaje: por Elements/@ y voice binding, NO por re-describir al personaje en texto. En i2v, si algo se deforma: describir menos (solo el movimiento) — sobre-describir lo que ya está en la imagen es contraproducente por diseño de la fórmula i2v.

## Historial

- 2026-08-13 — alta de la ficha (Kling 3.0/Omni; fórmula 2.x vigente como base del contenido por shot).
