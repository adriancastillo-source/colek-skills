---
herramienta: Seedance (ByteDance / Dreamina)
modelo-vigente: Seedance 2.5 (API pública 2026-08-07)
dominio: video
updated: 2026-08-13
status: vigente
---

# Ficha: Seedance 2.x

## Identidad

Modelo de video de ByteDance con **gramática formal publicada** (la más explícita del mercado: brackets tipados por canal de audio/texto y sistema de referencias `@`). Elegirlo para: multi-shot/ads, tomas largas (hasta 30 s — el más largo de los tres grandes), trabajo con muchas referencias (hasta 50 assets). Sus brackets son SUYOS — no trasplantar a Kling/Veo.

## Gramática oficial

Fuentes: BytePlus ModelArk — guía Seedance 2.0 (docs.byteplus.com/en/docs/ModelArk/2222480) y guía Seedance 2.5 (docs.byteplus.com/en/docs/ModelArk/2607689, actualizada 2026-08-13). Consultadas 2026-08-13.

- **Estructura 2.5 en 3 bloques:** (1) resumen de una frase `Subject + Location + Event + Genre/Style + Camera movement`; (2) plot detallado por timestamps (`0-3s: …`) o `Shot N (0-3s): …`; (3) notas de consistencia (ángulo, entorno, atmósfera).
- **Brackets tipados (cada canal el suyo):** `( )` música/BGM · `< >` efectos de sonido · `{ }` diálogo hablado · `【 】` subtítulos/texto en pantalla. Declarar idioma/entrega del diálogo aparte ("Dialogue language: British English, warm and low") y dentro de `{ }` SOLO las palabras.
- **Referencias:** `@Image 1`, `@Video 1`, `@Audio 1` (numeradas por orden de subida). Binding: `"Define [rasgos] in @Image 1 as <Subject_1>"` y reutilizar la etiqueta. Exclusión parcial: `"@Image 1 defines the facade. Do not use its sky."` Límites 2.5: 30 imágenes + 10 videos (≤30 s comb.) + 10 audios (≤30 s comb.) = 50 assets.
- **Cámara:** vocabulario directo (push in, pull out, pan, track, orbit, handheld, Hitchcock zoom, speed ramp); término raro → `[término + explicación]`. **Un movimiento por shot.**
- **Negativos: SÍ existen y son oficiales**, en frase explícita: `"no subtitles"`, `"no BGM; generate only environmental sounds"`, `"Do not generate a watermark"`, `"Do not generate duplicate characters"`.
- **Duración/ratio 2.5:** hasta 30 s por toma; ratio libre en rango [0.4, 2.5]. Modos LOCKED (edición, first/last frame, extensión — heredan ratio/duración; `ratio="adaptive"`, `duration="-1"`) vs UNLOCKED (referencia general/storyboard). **No se reencuadra 16:9→9:16 por edición** — generar al ratio destino.

## Plantilla

```
[SUBJECT + LOCATION + EVENT + STYLE + CAMERA — one sentence summary]

Shot 1 (0-[T1]s): [framing + angle], [subject action], [ONE camera movement]. <[SFX]> ([music bed])
Shot 2 ([T1]-[T2]s): [framing], [action]. {[dialogue line]} 【[on-screen text]】
Shot 3 ([T2]-[T3]s): [framing], [action].

Dialogue language: [idioma, tono].
@Image 1 is [Character A: 2-3 rasgos estables]; @Image 2 is [Character B]. Refer to camera movement in @Video 1.
Maintain consistency: [nº de personajes, ropa, props, espaciado].
Style: [estilo visual, grade]. No subtitles. [No BGM / (music: …)]. Do not generate watermark.
```

## Parámetros

- Toma única hasta 30 s (2.5); ratio [0.4, 2.5]; timestamps recomendados en 2.5.
- Existe skill oficial de reescritura de prompts `sd25-pe` en ModelArk.

## Gotchas documentados

- Timing exacto era **inestable en 2.0** (oficial recomendaba ritmo natural); en 2.5 los timestamps SÍ son el método — no aplicar consejos 2.0 a 2.5.
- Estabilidad cae con >8 sujetos; óptimo 1-5. Con 5+ sujetos, referencias de una sola vista son más estables. NO escribir nombres sobre las imágenes de referencia.
- Continuación de video: máx 3 clips / 15 s combinados (guía 2.0).
- Storyboards multi-panel: ≤15 paneles, line-art simple; la alineación no es estricta (alineación dura → keyframes).

## Verificado con gasto propio (torneo Foliatti, 2026-08-13)

- **La gramática oficial PAGA — A/B medido:** misma escena/refs/motor, solo cambió la sintaxis. Con
  la capa de fal (comillas + "0-3 seconds:" + "NO music" casero): música orquestal colada TODO el
  clip y marca deformada ("Folletti"). Con esta ficha (`{ }`, negativos oficiales): limpio y "Foliati".
  El negativo que funciona es literal: `No BGM; generate only environmental sounds`. — `reproducible`.
- **Shot-list por timestamps: obediencia real** (2 corridas, 6-7 shots c/u): CU/OTS/two-shot cortados
  donde se prescribió, apertura con acción previa al diálogo (personaje B entrando a cuadro) también
  obedecida. Español es-MX: 6/6 líneas palabra×palabra en ambas corridas. — `reproducible`.
- **`@Audio` como referencia RE-ACTÚA, no sincroniza** (medido con envolvente: r=0.32 vs r>0.7 de
  passthrough): toma el texto y aproxima el timbre, pero re-genera fraseo y pausas. Sirve para fijar
  QUÉ dice; NO para fijar la voz de un personaje de serie. — `reproducible`.
- **Precio real en fal** (`bytedance/seedance-2.5/reference-to-video`, 720p/16:9): **$0.4623/s** por
  delta de saldo — 54% arriba del precio de 2.0 std. — `medido`.

## Folklore de comunidad

- Umbral de 2-3 foley concretos por prompt y el tope de 8 sujetos como cifra — `anecdótico` (Segmind, "testing" propio, feb-2026).
- Diálogo en comillas dobles y duraciones 4-15 s — `parámetros de la plataforma fal`, no del modelo (fal.ai/learn); no confundir capa.
- "Instrucciones de cámara contradictorias → mush" — `reproducible` (consistente con la regla oficial de un movimiento por shot).

## Iteración

Cambiar un shot/canal por ronda manteniendo el resumen y las notas de consistencia idénticos. Para recasting o variantes: mismas referencias `@`, mismo binding `<Subject_N>`, solo cambia el asset referenciado.

## Historial

- 2026-08-13 — alta de la ficha (Seedance 2.5; brackets y @refs heredados de 2.0 siguen vigentes).
