# Plantilla Nano Banana (Gemini — NB Pro / NB2) — narrativa, sin negativos

**Por qué esta forma:** Google es explícito — **no listas de keywords, sino descripción narrativa** (`Sujeto + Acción + Contexto + Composición + Estilo`), empezando con un verbo fuerte. **No existe prompt negativo** (arquitectura autoregresiva): todo "sin X" se voltea a su positivo ("empty street" en vez de "no cars"). Única excepción: fronteras duras acompañadas del resultado positivo ("and only that text appears in the image"). Fortalezas a explotar: **el mejor texto-en-imagen del mercado** (labels y swatches anotados con fuente declarada) y **consistencia por imagen de referencia** (~93% en benchmarks de terceros, guías Nenobanana/Selfielab feb-2026; hasta 5 imágenes de referencia de personaje en NB Pro según la doc de la API de Gemini — ai.google.dev/gemini-api/docs/image-generation, consultada 2026-08-13).

**Ratio/resolución:** 3:2 o 16:9 de la lista fija; **2K** para sheets con anotaciones (el parámetro API lleva "K" mayúscula).

## Plantilla (slots entre corchetes)

```
Create a professional character reference sheet, as one single image arranged in a clean grid on a light gray seamless studio background. The character is [FICHA CANÓNICA COMPLETA en prosa — identidad, cara, ojos, pelo, cuerpo, wardrobe head-to-toe con material + color + un detalle por prenda. UNA sola vez.].

The top row shows three full-body views of the character standing in a relaxed neutral pose with both feet visible: front view, side view and back view. Below them sit a chest-up front close-up portrait and a top-down view seen from directly above. Along the bottom runs a strip of [N] detail swatches: close-ups of [lista de swatches]. Label every panel in large bold dark sans-serif capitals: "FRONT VIEW", "SIDE VIEW", "BACK VIEW", "FRONT CLOSE-UP", "TOP-DOWN VIEW", "DETAIL SWATCHES", and only that text appears in the image.

It is exactly the same character in every view, keeping the same face, eye line, proportions, hairstyle, outfit, seams and colors throughout; the back view continues the seams and details of the front logically. There is a single figure per panel and the background stays empty and seamless. [MÓDULO DE ESTILO en prosa — Render + Lighting + Quality tail.]
```

## Workflow ancla-primero (la jugada fuerte de NB)

Si el sheet en un solo tiro deriva — o para máxima consistencia desde el inicio:

1. Generar SOLO la vista frontal canónica full-body, alta calidad.
2. Guardarla como **ancla** del personaje.
3. Pedir el sheet completo (o cada vista extra) **adjuntando el ancla**:
   `Using the attached image as the exact character reference, keep the same face, proportions, hairstyle and outfit, and create [el sheet / la vista X]...`
4. Con varias referencias, **declarar el rol de cada una**: "Image A = the character, Image B = style reference only".
5. La edición es conversacional por turnos: cada refinamiento declara explícitamente qué se conserva. Tras ~5 ediciones, si aparecen derivas (manos, outfit reinterpretado), **regenerar el ancla**.

## Ejemplo lleno (Ricky, estilo fotorreal)

```
Create a professional character reference sheet, as one single image arranged in a clean grid on a light gray seamless studio background. The character is a cheerful young Latino waiter in his mid-twenties with warm brown skin, short curly black hair, thick expressive eyebrows and a bright smile, wearing a vibrant purple button-front vest with a black "RICKY" name tag, a crisp white dress shirt with sleeves rolled to the elbows, a black bow tie, a black belt with a silver buckle, slim black dress pants and polished black cap-toe oxford shoes.

The top row shows three full-body views of him standing in a relaxed neutral pose with both feet visible: front view, side view and back view. Below them sit a chest-up front close-up portrait and a top-down view seen from directly above. Along the bottom runs a strip of six detail swatches: close-ups of the vest fabric, shirt fabric, bow tie, belt buckle, shoes and name tag. Label every panel in large bold dark sans-serif capitals: "FRONT VIEW", "SIDE VIEW", "BACK VIEW", "FRONT CLOSE-UP", "TOP-DOWN VIEW", "DETAIL SWATCHES", and only that text appears in the image.

He is exactly the same character in every view, keeping the same face, eye line, proportions, hairstyle, outfit, seams and colors throughout; the back view continues the seams and details of the front logically. There is a single figure per panel and the background stays empty and seamless. Ultra detailed photorealistic photography, cinematic quality, subtle 35mm film grain, natural lighting.
```

## Conversión de negativos (chuleta)

| En GPT dirías… | En Nano Banana se vuelve… |
|---|---|
| no extra text | "and only that text appears in the image" |
| no duplicate figures | "there is a single figure per panel" |
| no background props | "the background stays empty and seamless" |
| no beauty filter / airbrushing | "visible natural skin texture with pores and subtle asymmetries" |
| no babyface (adultos) | "mature adult bone structure, defined jawline, adult proportions" |
