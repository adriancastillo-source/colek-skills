---
herramienta: GPT Image (OpenAI / ChatGPT)
modelo-vigente: gpt-image-2
dominio: imagen
updated: 2026-08-13
status: stale
---

# Ficha: GPT Image 2

## Identidad

Modelo de imagen de OpenAI con razonamiento O-series integrado: ejecuta bien **composiciones complejas en un solo tiro** (grids, layouts multi-panel, instrucciones largas). Elegirlo para: composiciones instruidas, edición dirigida, estilo fotográfico o ilustrado versátil. No elegirlo cuando el requisito dominante es texto-en-imagen denso o consistencia por imagen de referencia (ahí gana Nano Banana).

## Gramática oficial

Fuente: OpenAI Cookbook — Image Gen Models Prompting Guide (developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide, consultada 2026-08-13).

- **Formato libre, disciplina obligatoria:** "minimal prompts, descriptive paragraphs, JSON-like structures, instruction-style prompts, and tag-based prompts can all work well". Para pedidos complejos, recomienda **segmentos cortos etiquetados con saltos de línea** (contexto → sujeto → detalles → restricciones).
- **Patrón de iteración oficial:** "iterar en vez de sobrecargar" — base limpia + follow-ups de UN cambio, **repitiendo la preserve list** (invariantes) en cada iteración.
- **Texto literal:** entre **comillas o MAYÚSCULAS**; palabras difíciles deletreadas; exigir "verbatim, no extra characters"; `quality high` para texto pequeño.
- **Resolución:** `gpt-image-2`: flexible — lados múltiplos de 16, ratio máx 3:1, confiable hasta 2560x1440 (4K experimental).

## Plantilla (bloques etiquetados)

```
TASK: [qué imagen es, en una línea — tipo de pieza + propósito].

SUBJECT: [descripción canónica del sujeto — UNA sola vez, nunca reformular en otro bloque. Materiales, colores, un detalle por elemento.]

COMPOSITION: [layout explícito: encuadre, posición de elementos, paneles si aplica, espacio negativo. Para grids: número de paneles, orden, "equal margins, generous gutters".]

STYLE: [render + iluminación + acabado — específico, no adjetivos sueltos.]

TEXT (si aplica): exact text in quotes: "[TEXTO]", verbatim, no extra characters. [Si NO debe haber texto: mover a CONSTRAINTS "no text, no lettering".]

CONSTRAINTS: [exclusiones y reglas duras: single subject, no watermark, no extra text, anatomía, continuidad.]
```

## Parámetros

- Tamaños prácticos: 1536x1024 (3:2 landscape, el caballo de batalla), 1024x1536 (retrato), 2560x1440 (detalle). `quality: high` cuando hay texto o textura fina.
- API: `model="gpt-image-2"`; tolera `size` flexible (múltiplos de 16).
- ⚠️ **La edición con referencias va con `gpt-image-2` y SIN `input_fidelity`.** `gpt-image-1`
  salió de la API: `400 — "The model 'gpt-image-1' does not exist"` (2026-11-01).
  Y gpt-image-2 rechaza el parámetro: `400 — "The model 'gpt-image-2' does not support the
  'input_fidelity' parameter"` (verificado 2026-08-20). `images.edit(model="gpt-image-2", image=[...])`
  sin él conservó la identidad de una mascota de marca en 2 de 2 imágenes, y la etiqueta de un
  empaque de producto en 1 de 1 (2026-11-01). Mantiene el tamaño flexible. Si la fidelidad no alcanza, repetir en el prompt la preserve list.

## Gotchas documentados

- **Identity drift** si la descripción del sujeto se reformula en dos partes del prompt → descripción canónica única (Cookbook, patrón "preserve list").
- **Texto pequeño frágil** en layouts densos → pocas labels grandes; micro-anotaciones se rotulan después en diseño.
- **Sobrecargar un prompt** con múltiples propósitos (turnaround + expresiones + variantes) degrada todo → una imagen por propósito.
- Multi-panel: cara cambia entre paneles → añadir "same eye line, nose bridge, jaw length"; espalda inventa detalles → "continue every front seam logically".
- **Foto para ver a través de una ventana con forma (estrella, círculo):** si el prompt nombra la forma de destino, GPT puede entregar la foto ya recortada con esa forma y esquinas blancas. Pasó en 1 de 4 plates de una serie de capacitacion R2 (2026-10-05). El reintento salió bien al quitar toda mención de la forma y pedir *"Full-bleed square photograph… fills the entire square frame edge to edge, with no border, no frame, no shape cut-out and no white areas"*. La composición se pide en coordenadas: cabezas al ~40 % del alto, para que caigan en la banda ancha de la ventana. Prompt literal: `<ruta interna>`.
- **Extraer un asset limpio de una pieza propia funciona al primer intento en edición** (`images.edit`, 2.5 sunburst). Se usa el patrón TASK / CHANGE / PRESERVE / CONSTRAINTS. Dos casos de la misma ronda:
  - Quitar la estrella de un fondo, continuando degradado y bandas.
  - Aislar la pirámide sin su texto.
  Para recortar después por código, se pide *"on a plain flat pure white background… no cast shadow"* y se recorta por relleno desde las esquinas. Prompts: `BACK-EST1_DIAGONALES-SIN-ESTRELLA_GPT_R2.txt` y `PIRAMIDE-EST1_SIN-TEXTO_GPT_R2.txt`, en la misma carpeta.

## Folklore de comunidad

- Fórmula "Subject + Outfit + Pose + Views + Layout + Style" para model sheets (NanoPrompts, Dreamina, 2026) — `reproducible`: es aplicación directa del patrón oficial de bloques.
- "35mm film grain, cinematic quality" como acabado fotográfico (uso extendido, sin doc oficial) — `anecdótico pero inocuo`: describe estilo, no invoca magia.
- Quality tags heredados de difusión ("masterpiece, 8k") — `cargo cult`: sin efecto documentado en GPT Image; no usar.

## Iteración

Un cambio por edición; re-pegar SUBJECT y CONSTRAINTS completos en cada follow-up (la preserve list oficial). Para series consistentes: la primera imagen aprobada es el **ancla** y las siguientes la referencian en edición con restricciones explícitas ("same facial features, same outfit").

## Historial

- 2026-08-13 — alta de la ficha (modelo gpt-image-2).
- 2026-10-05 — dos gotchas en §Gotchas documentados: la foto que sale recortada con la forma de la ventana y
  la extracción limpia en edición. Cazados en la ronda 2 de la prueba de look de una serie de capacitacion.
- 2026-10-02 — **GPT Image 2.5 existe** y es la misma familia con la misma gramática (descripción en orden
  sujeto → composición → estilo → restricciones; texto literal entre comillas; en edición "change only X" +
  lista de lo que se preserva; sin pesos ni keyword stacking). Dos variantes: `flare` (chica, rápida) y
  `sunburst` (base, mejor para calidad y edición precisa). Calidad `low…max`; tamaños hasta 4K. Fuente:
  developers.openai.com/api/docs/guides/image-prompting (consultada 2026-10-02). Puerta probada: Higgsfield MCP
  (`gpt_image_2_5`, refs como `image_references`, aspecto 16:9) cuando la cuenta de OpenAI no tiene crédito.
  Cazado en la prueba de look de una serie de capacitacion. Esta ficha sigue `stale` para la reescritura completa.
- 2026-08-20 — precisión en §Parámetros: `input_fidelity` no existe en gpt-image-2, así que toda
  edición con referencia cae a gpt-image-1 (con su lista fija de tamaños y su costo real).
  Cazado al correr el casting del avatar de un cliente de alimentos, donde el arm de GPT se pedía image-to-image.
- 2026-11-01 — gpt-image-1 salió de la API (400 "does not exist"). Toda edición pasa a gpt-image-2
  sin `input_fidelity`; se retiran la lista fija de
  tamaños y el costo de gpt-image-1.
