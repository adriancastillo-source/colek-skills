---
herramienta: Higgsfield Soul Cinema (modelo de imagen propio de Higgsfield, familia Soul)
modelo-vigente: Soul Cinema — MCP `soul_cinematic` (preview 2026-03; vigente 2026-10-15); hermanos en el MCP sin doc pública `soul_cinema_studio` y `cinematic_studio_soul_location`
dominio: imagen
updated: 2026-10-15
status: vigente
---

# Ficha: Higgsfield Soul Cinema

## Identidad

Modelo de **imagen** de Higgsfield, hermano de Soul 2.0, afinado para **stills con cara de fotograma de película**: primeros planos con atmósfera, textura, grano natural, luz natural y looks de época. **El look viene fijo en el modelo**: no tiene presets ni Moodboards, así que el prompt carga toda la dirección. Elegirlo para keyframes de video (arranque para Kling o Seedance), concept art, storyboards con mood, planos de ambiente y **plates de locación**. No elegirlo cuando hay que meter un personaje propio no humano por referencia (no acepta Elements y la referencia apaga el prompt: ver gramática), ni para texto o tipografía legible en la imagen.

## Gramática oficial

Fuentes (consultadas 2026-10-15): help center **higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-soul-cinema** · página de producto **higgsfield.ai/soul-cinema** · blog **higgsfield.ai/blog/soul-cinema-preview** (fechado 2026-03-04) · help center de Soul ID **…/ai-models/how-do-i-create-and-use-a-soul-id-character** · contrato del **MCP de Higgsfield** (`models_explore action:get` de `soul_cinematic`, `soul_cinema_studio`, `cinematic_studio_soul_location`; descripción de `manage_reference_elements`; leídos 2026-10-15).

1. **Qué escribir:** "describe the scene, subject, and mood" (help center). Es la única regla de redacción oficial: no hay estructura, vocabulario de cámara ni negativos publicados.
2. **Prompt O referencia, no los dos (en la UI):** "When a reference image is attached, the prompt field becomes unavailable" (help center; Soul 2.0 se comporta igual). Una imagen de referencia **sustituye** al texto: no se puede pedir "este personaje, pero en tal lugar".
3. **Medias (MCP `soul_cinematic`):** máximo **1** imagen, rol `image`.
4. **Parámetros fuera del prompt:** relación de aspecto, calidad y tamaño de lote se fijan en la UI antes de generar; lote de hasta 4 imágenes (help center). En el MCP: `quality` `1.5k` | `2k` (defecto `2k`); ratios `1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9`; `soul_id` opcional.
5. **Soul HEX:** control de color por Color Transfer, con paleta sacada de una imagen de referencia o una paleta incluida (help center).
6. **Soul ID = identidad de UNA cara humana:** se entrena con **20 a 80 fotos** de la misma persona ("trains on a set of portraits of one face"); funciona en toda la familia Soul. Para un personaje inventado: generar primero sus retratos y entrenar sobre ellos, o usar AI Influencer Studio; para 2+ personajes consistentes, Elements (help center de Soul ID). En Soul Cinema se elige en el panel Character; un personaje de Soul 2.0 puede requerir "update" para estar disponible (help center).
7. **Elements NO aplican:** `soul_cinematic`, `soul_cinema_studio` y `cinematic_studio_soul_location` no están en la lista de modelos que honran `<<<element_id>>>` ("Other models ignore the placeholder", contrato de `manage_reference_elements`, 2026-10-15). Los que sí: `nano_banana_pro`, `nano_banana_2`, `gpt_image_2`, `seedream_v4_5`, `seedream_v5_lite`, `cinematic_studio_2_5` (imagen).
8. **Fortalezas declaradas:** primeros planos ("especially good at producing close-up shots", blog), texturas, grano, piel, materiales, luz natural, looks de época ("'70s, '90s, and today", página de producto), fotogramas que sirven de keyframe.
9. **Costo:** no publicado. El blog del preview solo dice que es "cheaper for user than other models". Cotizar con `get_cost: true`.

## Plantillas

**A — Still cinematográfico (personaje humano o sin personaje propio)**
```
[SHOT SIZE + ANGLE: e.g. medium close-up, eye level], [SUBJECT + ONE ACTION] in [LOCATION, specific and physical].
[COMPOSITION: subject on the left third, facing right; the right two-thirds stay clean and uncluttered for graphics].
[LIGHTING: source + direction + color temperature, e.g. cold overhead fluorescent tubes with a warm spill from the fridge door].
[ERA / PALETTE / TEXTURE: e.g. present day, desaturated teal-green palette, subtle natural film grain]. [MOOD in 2-3 words].
```

**B — Plate de locación vacía (para componer después al personaje)**
```
Wide [or medium-wide] establishing shot of [LOCATION: e.g. the interior of a small Mexican convenience store at night], empty, no people.
[Camera height and angle], [what occupies foreground / midground / background].
[COMPOSITION: leave a clear standing area at the left third, floor visible, for a character to be added later; right side calm for graphics].
[LIGHTING], [PALETTE + TEXTURE]. Photorealistic, natural lens perspective.
```
(La pared de producto con marcas reales sale distorsionada o inventada: pedir estantes genéricos y meter logos y señalética en post.)

## Parámetros

- `model: soul_cinematic` (vía `generate_image`) · `quality` `2k` por defecto · `aspect_ratio` uno de los 8 listados (ojo: **no hay `9:21`** aquí; `cinematic_studio_soul_location` sí lo lista) · `soul_id` solo para personaje humano entrenado · `count` 1-4.
- `soul_cinema_studio` (MCP, sin doc pública): `quality`, `style_id`, `custom_reference_id` ("e.g. a saved character or style reference"), `enhance_prompt` (defecto `false`); medias rol `image_references`, sin tope declarado; mismos ratios.
- `cinematic_studio_soul_location` (MCP, sin doc pública): sin parámetros ni medias declarados; ratios `1:1 … 21:9, 9:21`.

## Gotchas documentados

- **La referencia apaga el prompt** (gramática 2): en la UI, subir una imagen deja el texto sin efecto. Por MCP el campo `prompt` existe junto a `medias`, pero no hay doc de qué pesa cuando van los dos (hueco).
- **Personaje no humano (p. ej. un un personaje recurrente) en una locación fotorrealista: Soul Cinema solo no lo resuelve.** No acepta Elements, Soul ID exige cara humana, y la única imagen de referencia sustituye al prompt. Rutas que sí cierran con la doc actual: (a) **Soul Cinema hace el plate** de la locación (plantilla B) y un modelo que honra Elements (`nano_banana_pro`, `gpt_image_2`, `cinematic_studio_2_5`) mete al personaje usando el plate como referencia; o (b) generar todo directo en un modelo con Elements, sin la estética de Soul Cinema. `soul_cinema_studio` con `image_references` es una tercera vía posible, **sin probar**.
- **La composición se controla solo con palabras y con el ratio:** no hay máscara, pose ni control de layout documentados. Elegir el ratio final ANTES (reencuadrar después come el espacio negativo).
- Es modelo de imagen: para video, su salida va como `start_image` de otro modelo (help center).

## Folklore de comunidad

- **Vocabulario de los ejemplos publicados por Higgsfield** — `anecdótico`. El blog del preview (2026-03-04) muestra prompts redactados por Gemini, no guía oficial: "chiaroscuro", "shallow depth of field", "35mm film grain", "low-angle", "extreme close-up", "golden hour", "blue hour gradients", "teal and orange-pink highlights, desaturated shadows". Patrón: estética general → desglose de escena → nota de layout → paleta.
- **Prompt por capas y lo innegociable primero** (sujeto y acción → entorno → plano y cámara → luz → color y época → textura → restricciones de composición) — `reproducible` (Pippit, 2026-09-20; consistente con "describe the scene, subject, and mood"). Adjetivos de estilo sin sujeto ni acción = error listado.
- **Espacio para gráficos: decir dónde y cuánto** ("right two-thirds empty", "copy space top") y fijar el ratio antes de generar — `anecdótico` (Pippit, 2026-09-20).
- **No hay negativos**: escribir en positivo lo que debe quedar ("clean wall", "no people") en vez de listas "no X" — `anecdótico` (ninguna fuente documenta negativos; Pippit tampoco los cubre).
- **La misma receta no da el mismo resultado dos veces; una edición acotada (solo cambiar fondo) puede ir mejor en otro modelo** — `anecdótico` (Pippit, 2026-09-20).
- **Soul ID con un personaje no humano da "face not found"** — `anecdótico` (reseña en Trustpilot citada por terceros; consistente con "portraits of one face").

## Iteración

Fijar ratio, calidad y la frase de composición como invariantes; cambiar una capa por ronda (luz O paleta O plano). Guardar la primera salida como línea base y comparar contra ella. Si una sola zona falla (el fondo, un objeto), corregir esa zona en un modelo de edición en vez de regenerar todo el still.

## Huecos declarados

- 🔲 hueco: **costo en créditos** de `soul_cinematic` (y de sus hermanos). Resolver con `get_cost: true`.
- 🔲 hueco: por MCP, **¿qué hace `soul_cinematic` con `prompt` + 1 `image` juntos?** (la UI los hace excluyentes; el MCP no lo dice). ¿La imagen es referencia de estilo, de composición o de contenido?
- 🔲 hueco: **qué son `soul_cinema_studio` y `cinematic_studio_soul_location`**: no hay doc pública; solo su esquema en el MCP. En particular, si `image_references` de `soul_cinema_studio` sostiene a un personaje no humano en una locación (el caso un personaje recurrente en una tienda de conveniencia).
- 🔲 hueco: negativos, límite de caracteres del prompt y si existe control de composición más allá del texto.

## Historial

- 2026-10-15 — alta de la ficha (Soul Cinema; preview publicado 2026-03-04, sin guía de prompting oficial).
