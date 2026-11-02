---
herramienta: Kling (Kuaishou)
modelo-vigente: Kling 3.0 / 3.0 Omni (anunciados 2026-02-05); línea 2.x vigente para t2v/i2v simple
dominio: video
updated: 2026-08-13
status: stale
---

# Ficha: Kling 2.x / 3.0

## Identidad

Modelo de video de Kuaishou, fuerte en **personajes** (el propio Higgsfield lo recomienda para "personajes en 4K"). 3.0 Omni añade audio/diálogo nativos, multi-shot (hasta 6 shots / 15 s) y voice binding. Elegirlo para: actuación de personajes, diálogo con lip-sync nativo, secuencias cortas multi-shot. La línea 2.x sigue para clips simples de 5/10 s.

## Gramática oficial

Fuentes: kling.ai/quickstart/text-to-video-prompt-guide (fórmula 2.x) + kling.ai/blog/kling-ai-prompt-guide (2026-08-07, marco 3.0) + kling.ai/quickstart/klingai-video-3-omni-model-user-guide (multi-shot, @elements, voice binding). Consultadas 2026-08-13.

- **Fórmula 2.x:** `Subject (descripción) + Subject Movement + Scene (descripción) + (Camera Language + Lighting + Atmosphere)` — los 3 primeros obligatorios. **Image-to-video:** solo `Subject + Movement, Background + Movement` (la imagen ya aporta apariencia; describir SOLO lo que se mueve).
- **Marco 3.0 (blog oficial):** 6 elementos — Subject · Action · Scene · Camera Language · Lighting · Mood. Cita oficial: "Strong cinematic prompts are built from clear scene direction rather than secret formulas."
- **Multi-shot 3.0 Omni:** `Shot [n] ([duración]s): [framing/angle], [contenido], [movimiento de cámara]` — ej. oficial: `"Shot 1 (3s): Mid-shot, background @Image. @Grace sits on the sofa eating cookies as @un personaje recurrente walks in."` Alterno por timestamps `[00:00 - 00:02] … Audio: …`.
- **Elements/referencias (3.0):** menciones `@Nombre` (`@Grace`, `@Image`). Hasta 7 imágenes (≥300 px, ≤10 MB) — o hasta 4 si además hay video de referencia (1 video de 3-10 s, ≤200 MB).
- **Diálogo (solo 3.0 Omni):** inline con comillas — `@Grace says, "Hey! Watch your dog!"`. Entiende shot-reverse-shot, cross-cutting, voice-over. **Audio/SFX:** línea `Audio:` propia.
- **Voice binding (3.0 Omni):** audio de 5-30 s de UNA persona (fondo limpio) o video de 3-8 s del personaje (extrae apariencia + voz).
- **Start & End Frame (first/last):** soportado en 3.0 junto con t2v, i2v, elements y multi-shot. Guía oficial dedicada: kling.ai/quickstart/ai-video-start-end-frames (consultada 2026-08-15 vía buscador; el fetch directo del dominio devuelve HTTP 446 — la existencia y el alcance de la feature están confirmados, el texto literal de esa guía **no** pudo leerse). Regla de redacción en §Start/End abajo.
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

Start & End Frame (first/last) — **prompt mínimo, no máximo:**
```
[SOLO el movimiento entre las dos imágenes: qué hace el sujeto].
[UN movimiento de cámara, simple]. [Audio: SFX/ambiente]  ← solo 3.0 Omni
```

## Start / End Frame — la regla que invierte el instinto

Procedencia: guía de plataforma de Higgsfield ("Kling is King: Start & End Frames", higgsfield.ai/blog, consultada 2026-08-15) + resúmenes de la guía oficial de Kling. **No es doc de Kuaishou**: confianza `reproducible en lo estructural` (ratio, duraciones, modos de falla coinciden entre fuentes), `anecdótico` en los detalles de redacción.

- **Menos prompt es mejor. Se puede ir en blanco:** *"You can go promptless. Kling will infer the motion."* El prompt solo agrega lo que las imágenes no dicen — movimiento de cámara, una transformación puntual. **Trasplantar aquí un prompt largo estilo Veo (5 slots + timeline + ambiance) es contraproducente por diseño**, y coincide con lo que ya dice la fórmula i2v de Kling: describir SOLO lo que se mueve.
- **El aspect ratio del START FRAME manda sobre todo el clip**: el end frame se recorta o se expande para encajar. Igualar ambas imágenes antes de subirlas.
- **Start wide + end telefoto confunde al modelo.** Si entre las dos imágenes cambia la distancia focal aparente, o se acepta que lo resuelva como movimiento (dolly), o se re-encuadran.
- Start y end muy distintos en color/luz/estilo **rompen** la transición: acercarlos antes de generar.
- Duración: **5 s** para transiciones dinámicas; **10 s** solo si la transformación es compleja (en transiciones simples se siente largo).
- Modos de falla y su fix: transición "rara" → acercar los frames · movimiento excesivo o jitter → **quitar** direcciones de cámara y recortar el prompt · escala irreal → arreglarla en las imágenes fuente, no en el prompt.
- **Hueco abierto:** si el audio nativo de 3.0 Omni funciona en modo start/end no está confirmado en ninguna fuente leída — verificar en la corrida, no asumir.

## Parámetros

- 2.x: 5 s o 10 s; 16:9 / 9:16 / 1:1; modos Standard/Professional.
- 3.0 Omni: hasta 15 s, hasta 6 shots; 1080p/720p según la guía Omni (el "4K nativo" circula en anuncios/terceros, no en la guía de prompting — tomarlo con reserva).

## Gotchas documentados

- Un solo movimiento de cámara por clip; transformaciones simultáneas ("360° + zoom-in") distorsionan — secuenciarlas.
- Movimientos físicos complejos y conteos/números fallan (oficial 2.x); split-screen exige especificar ángulos.
- Términos de luz contradictorios ("golden hour" + "studio lighting") confunden el estilo.
- Con video de referencia: tope de Elements baja a 4 y el audio nativo NO funciona sobre video de input (oficial Omni).
- Cámara vaga ("cinematic movement") da resultados inconsistentes — nombrar framing + movimiento + ritmo.

## Verificado con gasto propio (torneo un cliente de entretenimiento, 2026-08-13)

- **Diálogo nativo en español es-MX: NO confiable** (2/2 corridas de 15 s, vía Higgsfield):
  deformó nombres propios ("Don Fortuno" → "Funutro" / "Fortunino"), rompió una línea completa en
  papilla fonética, añadió interjecciones no escritas ("¡Oh!") y **adoptó acento con mezcla italiana**
  (veredicto de el director). Descartado para diálogo es-MX de serie; posible combo video-Kling +
  voice-swap en post (sin medir). — `reproducible (2 corridas)`.
- **Shot-list multi-shot SÍ la obedece** (formato oficial `Shot N (ns):`): CU/OTS/two-shot y
  apertura con llegada de personaje, correctos en ambas corridas. El problema es el audio, no la
  puesta en escena. — `reproducible`.
- **Deforma proporciones del personaje** aun partiendo de start_image: engordó al personaje robusto
  más allá de su diseño (veredicto de el director contra el character sheet, corrida 2). En apego a
  referencias de personaje, Seedance 2.5 le ganó con claridad en el mismo caso. — `reproducible
  (consistente con el "morphing object problem" del folklore fal)`.
- **Audio sucio:** risas tipo estudio colgadas al inicio en corrida 1 pese a pedir solo ambiente
  (los negativos in-prompt no tienen respaldo oficial en Kling — ver Gramática). — `anecdótico`.
- **Precio real vía Higgsfield:** 15 s std 16:9 con audio = **30 créditos** (~<costo interno> al pack top-up)
  ≈ 2 cr/s. — `medido`.

## Folklore de comunidad

- Énfasis `++elemento++`, negativos in-prompt ("No people, no text overlays"), lentes virtuales ("24mm f/2.8") — `anecdótico`: vienen de fal.ai (guía 2.6 Pro), NO están en docs oficiales.
- Tope práctico de 4 referencias aunque el máximo sea 7 ("más confunde prioridades") — `anecdótico` (fal).
- "Morphing object problem" en clips largos → añadir "maintains exact appearance throughout" o Elements multi-ángulo — `anecdótico` (fal).
- Texto en pantalla: sin sintaxis documentada en ninguna guía oficial — si el texto importa, ponerlo en post.

## Iteración

Un cambio por ronda. Identidad de personaje: por Elements/@ y voice binding, NO por re-describir al personaje en texto. En i2v, si algo se deforma: describir menos (solo el movimiento) — sobre-describir lo que ya está en la imagen es contraproducente por diseño de la fórmula i2v.

## Historial

- 2026-08-15 — añadida la sección **Start / End Frame** (first/last): la ficha no documentaba una capacidad central de Kling 3.0 y un pedido de first/last frame la habría redactado con la gramática equivocada (prompt largo). Disparado por el gate de coincidencia del router.
- 2026-08-13 — alta de la ficha (Kling 3.0/Omni; fórmula 2.x vigente como base del contenido por shot).
