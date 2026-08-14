---
herramienta: Nano Banana (Google Gemini imagen)
modelo-vigente: Nano Banana Pro (gemini-3-pro-image) / Nano Banana 2 (gemini-3.1-flash-image)
dominio: imagen
updated: 2026-08-13
status: vigente
---

# Ficha: Nano Banana (Gemini)

## Identidad

Familia de imagen de Google (autoregresiva, no difusión). Sus dos superpoderes: **el mejor texto-en-imagen del mercado** (labels, anotaciones, tipografía descrita) y **consistencia por imagen de referencia** (~93% en benchmarks de terceros — guías Nenobanana/Selfielab feb-2026). Elegirla para: piezas con texto, series consistentes de un personaje/producto, edición conversacional. No elegirla cuando el prompt necesita listas de exclusiones duras (no tiene negativos).

## Gramática oficial

Fuentes: blog.google "Prompting tips Nano Banana Pro" + Google Cloud "Ultimate prompting guide for Nano Banana" + ai.google.dev/gemini-api/docs/image-generation (consultadas 2026-08-13).

- **Narrativa obligada, no keywords:** descripción en prosa con estructura `[Sujeto] + [Acción] + [Contexto] + [Composición] + [Estilo]`, empezando con un **verbo fuerte** que declare la operación ("Create...", "Generate...").
- **Sin prompt negativo** (arquitectura autoregresiva): regla oficial de **positive framing** — "empty street" en vez de "no cars". Excepción: fronteras duras acompañadas del resultado positivo ("and only that text appears in the image").
- **Texto en imagen:** texto literal entre comillas + fuente descrita ("bold white sans-serif") o nombrada; multilingüe.
- **Referencias:** Pro admite hasta 5 imágenes de personaje + 6 de objeto + 3 de estilo; NB2 hasta 4 personajes + 10 objetos (docs API). Al mezclar, **declarar el rol de cada imagen** ("Image A = the character, Image B = style only").
- **Edición conversacional** por turnos, siendo explícito sobre qué se mantiene igual.

## Plantilla (narrativa)

```
Create [tipo de pieza] of [SUJETO — descripción canónica en prosa, una sola vez: rasgos, materiales, colores, un detalle por elemento]. [ACCIÓN/POSE]. [CONTEXTO/FONDO — descrito en positivo, incluido lo que debe estar vacío]. [COMPOSICIÓN — encuadre, layout, posición de elementos]. [TEXTO si aplica: The image includes the text "[TEXTO]" in [fuente/estilo], and only that text appears in the image.] [ESTILO — render, iluminación, acabado, en prosa].
```

Con referencia adjunta (el modo fuerte):

```
Using the attached image as the exact [character/product/style] reference, keep the same [invariantes: face, proportions, outfit, colors] and [OPERACIÓN: create/change/place...] [resto del requerimiento].
```

## Parámetros

- Aspect ratios (lista fija): 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 (NB2 añade 1:4/4:1/1:8/8:1).
- Resoluciones: 1K / 2K / 4K (el parámetro API exige la "K" mayúscula). 2K para piezas con texto/anotaciones.

## Gotchas documentados

- **Negativos no existen**: cada "sin X" se voltea a su positivo o el modelo lo ignora (o lo dibuja).
- Manos derivan tras ~5 ediciones consecutivas → regenerar el ancla.
- Outfits se reinterpretan en planos alejados; escenas grupales mezclan rasgos entre personajes (guías de consistencia 2026).
- Texto sobre props pequeños del sujeto sigue siendo el punto débil (mejorado en NB2).

## Folklore de comunidad

- **Workflow ancla-primero** (generar UNA vista/pieza canónica → adjuntarla como referencia para el resto) — `reproducible`: explota la arquitectura de referencias documentada; es el patrón canónico de comunidad (Selfielab, Chatsmith, 2026).
- Chuleta de conversión de negativos (no text → "and only that text appears"; no props → "the background stays empty and seamless") — `reproducible`: aplicación directa del positive framing oficial.
- Adjetivos de calidad tipo "8k, masterpiece" — `cargo cult`: sin efecto documentado; la calidad se pide con resolución y descripción de acabado.

## Iteración

Conversacional por turnos: cada refinamiento declara qué se conserva ("keep everything identical except..."). En API, `previous_interaction_id` mantiene el hilo. Tras ~5 ediciones con derivas: regenerar ancla y recomenzar desde ella.

## Historial

- 2026-08-13 — alta de la ficha (NB Pro / NB2).
