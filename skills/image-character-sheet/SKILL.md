---
name: image-character-sheet
description: Generar CHARACTER SHEETS (hojas de referencia de personaje multi-vista) con IA — produce prompts optimizados por plataforma (ChatGPT/GPT Image y Nano Banana/Gemini) desde una ficha canónica de personaje. Usar cuando el usuario diga "character sheet", "hoja de personaje", "model sheet", "reference sheet", "turnaround", "expression sheet", "vistas del personaje", "personaje consistente", o pida un personaje en múltiples vistas (front/side/back, close-up, swatches). Entrega el prompt listo para pegar — no ejecuta la generación.
tags: [sop, imagen]
---

# image-character-sheet — hojas de referencia de personaje con IA (edición portable el estudio)

> **Edición portable v2026-08-13 — distribuida por el repo `el estudio-skills`. NO editar estos archivos a mano: cualquier cambio se pierde en la siguiente actualización. Mejoras y correcciones → avisar a el director.**

Convierte un brief de personaje en **prompts de character sheet listos por plataforma** — uno para **GPT Image 2** (ChatGPT) y uno para **Nano Banana** (Gemini) — desde **una misma ficha canónica**.

> **Por qué dos prompts y no uno:** GPT Image trabaja mejor con bloques cortos etiquetados y tolera listas de exclusiones; Nano Banana exige párrafo narrativo y NO tiene prompt negativo (todo "sin X" se voltea a positivo). Un prompt único desperdicia las fortalezas de ambos. Detalle por plataforma: `references\plantilla-gpt-image.md` y `references\plantilla-nano-banana.md`.

## Flujo

1. **Brief.** Extraer del pedido la identidad del personaje. Si el usuario pegó una descripción o imagen de referencia del personaje, **preservar cada detalle textual** — no parafrasear rasgos ya definidos.
2. **Estilo — la referencia visual manda.** Si el usuario adjuntó una referencia, el estilo se extrae de ella (y si el texto del pedido la contradice, gana la referencia). Si NO adjuntó referencia, **preguntarla siempre** ("¿tienes una imagen de referencia del estilo?"); solo si no existe, pedir descripción libre o preset. Presets listos en `references\presets-estilo.md` (fotorreal-anti-retoque, 3d-pixar, anime-2d, game-concept, editorial-polished). Con referencia/descripción libre, construir un módulo custom con la misma forma (Render + Lighting + Quality tail).
3. **Composición.** Default = **grid completo**: fila 1 full-body FRONT/SIDE/BACK, fila 2 FRONT CLOSE-UP + TOP-DOWN VIEW, franja inferior DETAIL SWATCHES con labels. Alternativas: turnaround simple (3-5 vistas en fila), expression sheet, wardrobe variants. **Una sheet por propósito** — turnaround y expresiones nunca en la misma imagen (figuras chicas + layout roto).
4. **Ficha canónica de slots** (escrita UNA sola vez, en inglés):
   `IDENTIDAD (edad + piel/etnia) → CARA (forma, mandíbula, pómulos, nariz, labios) → OJOS → CEJAS → PELO (color, largo, estilo, finish) → CUERPO → WARDROBE head-to-toe (top → capas → bottom → cinturón → zapatos → accesorios, con material + color + un detalle por prenda)`.
   Especificidad gana a adjetivos: "vibrant purple button-front vest with black un personaje recurrente name tag" ≫ "nice vest". Sin huecos en el wardrobe (la espalda inventa lo que no declaraste).
5. **Emitir los dos prompts** llenando las plantillas de `references\` (o solo el de la plataforma que el usuario va a usar). Entregar en bloques de código copy-paste, con tamaño/ratio recomendado al pie.

## Reglas anti-deriva (lo que más se rompe)

- **Consistencia = el producto.** La descripción del personaje vive en UN solo lugar del prompt; jamás reformularla en otra sección (causa #1 de identity drift).
- **Cláusula de invariantes siempre:** *"identical character in every view — same face, eye line, nose bridge, jaw length, body proportions, clothing seams, colors and accessories; the back view continues every front seam logically"*.
- **Anti-duplicados:** *"single character only, no duplicate figures"* (+ en GPT: no mannequin, no reflections, no extra people).
- **Labels:** pocas y grandes, entre comillas, verbatim ("FRONT VIEW", "SIDE VIEW"...) + "no extra text beyond the labels". En GPT el texto chico es frágil → nada de micro-anotaciones; Nano Banana sí aguanta swatches anotados.
- **Iterar, no sobrecargar:** cambios de a uno, re-pegando la lista de invariantes en cada iteración. En Nano Banana, si tras ~5 ediciones aparecen derivas (manos, outfit), regenerar el ancla.
- **Ancla-primero (Nano Banana):** si el sheet en un tiro deriva, generar SOLO la vista frontal canónica y adjuntarla: *"Using the attached image as the exact character reference, keep the same face, proportions and outfit…"*. Es la fortaleza estructural de NB.
- **IP:** personaje **original** siempre — nunca replicar la cara de una persona real ni un personaje con copyright; las referencias son inspiración de estilo, no reproducción.
- **Adultos maduros:** si el personaje es adulto, especificar estructura ósea adulta (mandíbula definida, proporciones maduras) — el sesgo babyface es corrección recurrente.
