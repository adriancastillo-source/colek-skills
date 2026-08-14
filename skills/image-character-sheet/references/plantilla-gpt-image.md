# Plantilla GPT Image 2 (ChatGPT / API OpenAI) — bloques etiquetados

**Por qué esta forma:** la guía oficial de OpenAI acepta cualquier formato, pero para pedidos complejos recomienda **segmentos cortos etiquetados con saltos de línea**, y su patrón de iteración es "cambio único + re-pegar la preserve list". GPT Image 2 razona la composición (grid en un solo tiro funciona bien), pero el **texto pequeño es frágil** → pocas labels grandes. Tolera listas de exclusiones (CONSTRAINTS).

**Tamaño:** 1536x1024 (3:2 landscape) estándar; 2560x1440 si se necesita más detalle. Calidad `high` (el texto lo agradece).

## Plantilla (slots entre corchetes)

```
TASK: Professional character reference sheet, one single image, grid layout.

CHARACTER (identical in every view): [FICHA CANÓNICA COMPLETA — identidad, cara, ojos, pelo, cuerpo, wardrobe head-to-toe con material + color + un detalle por prenda. UNA sola vez, nunca reformular en otro bloque.]

VIEWS:
- Top row, three equal panels: full-body FRONT VIEW, SIDE VIEW, BACK VIEW — standing in a relaxed neutral pose, head to toe, both feet visible.
- Middle row, two panels: FRONT CLOSE-UP (chest-up portrait) and TOP-DOWN VIEW (seen from directly above).
- Bottom strip: DETAIL SWATCHES — [N] labeled close-up squares: [lista de swatches: telas, accesorios, props].

LAYOUT: clean light gray seamless background, equal margins, generous gutters, each figure fully isolated, flat even studio lighting.

LABELS: large clean dark sans-serif caption above each panel, verbatim: "FRONT VIEW", "SIDE VIEW", "BACK VIEW", "FRONT CLOSE-UP", "TOP-DOWN VIEW", "DETAIL SWATCHES".

STYLE: [MÓDULO DE ESTILO — de presets-estilo.md o custom: Render + Lighting + Quality tail.]

CONSTRAINTS: identical character in every view — same face, eye line, nose bridge, jaw length, body proportions, clothing seams, colors and accessories; the back view continues every front seam logically; single character only, no duplicate figures, no mannequin, no reflections, no extra people, no watermark, no extra text beyond the labels.
```

## Variantes de VIEWS (una sheet por propósito)

- **Turnaround:** `Four consistent full-body views in a row — front view, 3/4 view, side profile, back view — evenly spaced, A-pose, registration lines aligning eyes, chin, shoulders and waist across views.`
- **Expression sheet:** `One full-body reference on the left; right side a grid of head-and-shoulders portraits, all from the same frontal angle: neutral, smiling, serious, surprised, angry, laughing. Labels under each.`
- **Wardrobe variants:** `The same character shown full-body in [N] different outfits side by side, same pose and angle.`

## Ejemplo lleno (Ricky, estilo fotorreal)

```
TASK: Professional character reference sheet, one single image, grid layout.

CHARACTER (identical in every view): a cheerful young Latino waiter in his mid-twenties, warm brown skin, short curly black hair, thick expressive eyebrows, bright smile; wearing a vibrant purple button-front vest with a black "RICKY" name tag, crisp white dress shirt with sleeves rolled to the elbows, black bow tie, black belt with silver buckle, slim black dress pants, polished black cap-toe oxford shoes.

VIEWS:
- Top row, three equal panels: full-body FRONT VIEW, SIDE VIEW, BACK VIEW — standing in a relaxed neutral pose, head to toe, both feet visible.
- Middle row, two panels: FRONT CLOSE-UP (chest-up portrait) and TOP-DOWN VIEW (seen from directly above).
- Bottom strip: DETAIL SWATCHES — six labeled close-up squares: vest fabric, shirt fabric, bow tie, belt buckle, shoes, name tag.

LAYOUT: clean light gray seamless background, equal margins, generous gutters, each figure fully isolated, flat even studio lighting.

LABELS: large clean dark sans-serif caption above each panel, verbatim: "FRONT VIEW", "SIDE VIEW", "BACK VIEW", "FRONT CLOSE-UP", "TOP-DOWN VIEW", "DETAIL SWATCHES".

STYLE: ultra detailed photorealistic photography, visible fine skin texture with natural pores and subtle asymmetries, no digital smoothing, no beauty filter, cinematic quality, 35mm film grain, natural lighting.

CONSTRAINTS: identical character in every view — same face, eye line, nose bridge, jaw length, body proportions, clothing seams, colors and accessories; the back view continues every front seam logically; single character only, no duplicate figures, no mannequin, no reflections, no extra people, no watermark, no extra text beyond the labels.
```

## Fixes conocidos (error → cláusula)

| Síntoma | Fix |
|---|---|
| Cara cambia entre vistas | `same eye line, nose bridge, jaw length` (ya en CONSTRAINTS) |
| La espalda inventa detalles | `continue every front seam logically around` + wardrobe sin huecos |
| Grid amontonado | Menos paneles + `equal margins, generous gutters, isolated figures` |
| Labels ilegibles | Menos labels, más grandes; quality high; quitar micro-anotaciones |
| Identity drift al iterar | Cambio único por edición + re-pegar CHARACTER y CONSTRAINTS completos |
