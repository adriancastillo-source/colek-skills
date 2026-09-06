---
herramienta: GPT Image (OpenAI / ChatGPT)
modelo-vigente: gpt-image-2
dominio: imagen
updated: 2026-08-13
status: vigente
---

# Ficha: GPT Image 2

## Identidad

Modelo de imagen de OpenAI con razonamiento O-series integrado: ejecuta bien **composiciones complejas en un solo tiro** (grids, layouts multi-panel, instrucciones largas). Elegirlo para: composiciones instruidas, edición dirigida, estilo fotográfico o ilustrado versátil. No elegirlo cuando el requisito dominante es texto-en-imagen denso o consistencia por imagen de referencia (ahí gana Nano Banana).

## Gramática oficial

Fuente: OpenAI Cookbook — Image Gen Models Prompting Guide (developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide, consultada 2026-08-13).

- **Formato libre, disciplina obligatoria:** "minimal prompts, descriptive paragraphs, JSON-like structures, instruction-style prompts, and tag-based prompts can all work well". Para pedidos complejos, recomienda **segmentos cortos etiquetados con saltos de línea** (contexto → sujeto → detalles → restricciones).
- **Patrón de iteración oficial:** "iterar en vez de sobrecargar" — base limpia + follow-ups de UN cambio, **repitiendo la preserve list** (invariantes) en cada iteración.
- **Texto literal:** entre **comillas o MAYÚSCULAS**; palabras difíciles deletreadas; exigir "verbatim, no extra characters"; `quality high` para texto pequeño.
- **Resolución:** `gpt-image-1`: 1024x1024 / 1536x1024 / 1024x1536. `gpt-image-2`: flexible — lados múltiplos de 16, ratio máx 3:1, confiable hasta 2560x1440 (4K experimental).

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
- ⚠️ **La edición con fidelidad de referencia sigue siendo de `gpt-image-1`.** `images.edit` con
  `input_fidelity="high"` **rechaza** gpt-image-2: `400 — "The model 'gpt-image-2' does not support
  the 'input_fidelity' parameter"` (verificado 2026-08-20). Para image-to-image con referencias hay
  que pedir `model="gpt-image-1"`, y ahí el tamaño vuelve a la lista fija (1024x1024 / 1536x1024 /
  1024x1536). Consecuencia de costo: high 1024x1536 = 6240 tokens de salida × <costo interno>/1M = **<costo interno>/imagen**
  (developers.openai.com/api/docs/pricing + su guía de image generation, leídas 2026-08-20).

## Gotchas documentados

- **Identity drift** si la descripción del sujeto se reformula en dos partes del prompt → descripción canónica única (Cookbook, patrón "preserve list").
- **Texto pequeño frágil** en layouts densos → pocas labels grandes; micro-anotaciones se rotulan después en diseño.
- **Sobrecargar un prompt** con múltiples propósitos (turnaround + expresiones + variantes) degrada todo → una imagen por propósito.
- Multi-panel: cara cambia entre paneles → añadir "same eye line, nose bridge, jaw length"; espalda inventa detalles → "continue every front seam logically".

## Folklore de comunidad

- Fórmula "Subject + Outfit + Pose + Views + Layout + Style" para model sheets (NanoPrompts, Dreamina, 2026) — `reproducible`: es aplicación directa del patrón oficial de bloques.
- "35mm film grain, cinematic quality" como acabado fotográfico (uso extendido, sin doc oficial) — `anecdótico pero inocuo`: describe estilo, no invoca magia.
- Quality tags heredados de difusión ("masterpiece, 8k") — `cargo cult`: sin efecto documentado en GPT Image; no usar.

## Iteración

Un cambio por edición; re-pegar SUBJECT y CONSTRAINTS completos en cada follow-up (la preserve list oficial). Para series consistentes: la primera imagen aprobada es el **ancla** y las siguientes la referencian en edición con restricciones explícitas ("same facial features, same outfit").

## Historial

- 2026-08-13 — alta de la ficha (modelo gpt-image-2).
- 2026-08-20 — precisión en §Parámetros: `input_fidelity` no existe en gpt-image-2, así que toda
  edición con referencia cae a gpt-image-1 (con su lista fija de tamaños y su costo real).
  Cazado al correr el casting del avatar de un cliente de alimentos, donde el arm de GPT se pedía image-to-image.
