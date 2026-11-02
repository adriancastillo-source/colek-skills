---
herramienta: Higgsfield Genjutsu (familia de flujos video-a-video, no un modelo único)
modelo-vigente: Genjutsu (lanzado 2026-09-01) — Motion Transfer `hf_mult_motion_control` · Object Swap `hf_mult_replace_object` · Genjutsu Styles (restyle) · galería de presets de movimiento
dominio: video
updated: 2026-10-15
status: vigente
---

# Ficha: Higgsfield Genjutsu

## Identidad

Genjutsu es la capa **video-a-video** de Higgsfield: parte de un video que YA existe (filmado o generado) y cambia solo lo que se le pide. **No es un modelo**: son cuatro puertas con el mismo nombre comercial, y la primera decisión es cuál:

| Puerta | Qué hace | Se conserva | Se cambia |
|---|---|---|---|
| **Motion Transfer** (`hf_mult_motion_control`) | Toma el movimiento de un video conductor y reconstruye la escena con tus referencias | movimiento, cámara, timing | elenco, locación, look |
| **Object Swap** (`hf_mult_replace_object`) | Reemplaza UN elemento señalado en un video real | todo el plano tal como se filmó | el personaje, prenda, producto, locación u objeto señalado |
| **Styles** (`genjutsu-style:<id>`) | Re-dibuja cada cuadro de tu video en un look con nombre | movimiento, cámara, encuadre | el estilo de render (cel, yarn, toy CGI, low-poly…) |
| **Presets** (galería) | Video conductor ya curado por Higgsfield o la comunidad; tú pones las referencias | el movimiento del preset | el sujeto |

Elegirlo cuando **el movimiento ya existe** (una toma de un actor, una coreografía, un plano de cámara) y lo que falta es el elenco o el look. No elegirlo para generar desde cero (eso es text/image-to-video: Seedance, Kling, Veo) ni para lipsync dirigido por audio (no consta que lo haga: ver huecos).

## Gramática oficial

Fuentes (consultadas 2026-10-15): página de producto **higgsfield.ai/genjutsu** · blog **higgsfield.ai/blog/higgsfield-genjutsu** (metadato de publicación 2026-08-31) · contrato del **MCP de Higgsfield** (`get_preset_instructions preset:"/genjutsu"`, `models_explore action:get` de ambos modelos, descripción de `generate_video` y de `manage_reference_elements`, leídos 2026-10-15). Esquema del API de terceros: **docs.comfy.org** (Comfy Router, modelo `higgsfield/higgsfield-genjutsu-motion-transfer-v1.0`, consultado 2026-10-15).

1. **El prompt es OPCIONAL.** "A full prompt is not required": un preset solo puede conducir todo el cambio, y la descripción corta sirve para afinar (blog). La página de producto da la única regla de redacción: decir **qué debe ser distinto** ("a person, a product, the text") y el resto del plano queda intacto. El esquema del API lo llama "Optional guidance for the recast" (Comfy Router).
2. **Las referencias mandan, no el texto.** Personajes, prendas, props y locaciones entran como **imágenes de referencia** y "show up in every result" (página de producto). El prompt dice qué hacer con ellas, no las describe.
3. **Medias (MCP):** imágenes de referencia + **exactamente UN video** fuente/conductor, en `params.medias`. El contrato de `generate_video` y de `/genjutsu` dice roles `image` y `video`; `models_explore` lista los roles como `image_references` / `video_references` ("server may auto-coerce when unambiguous"). Usar `image`/`video` como dice el contrato de la herramienta.
4. **Elegir el modelo por la intención del pedido, no por el preset de origen:** copiar/repetir movimiento, gestos, baile o cámara → `hf_mult_motion_control`; reemplazar un objeto, producto, prenda o personaje → `hf_mult_replace_object` (contrato MCP). **Nunca** pasar `genjutsu` como `model`.
5. **Video fuente:** 4 a 30 s (página de producto y blog; el esquema del API: "Minimum 4 seconds; a longer video is trimmed to 30 seconds"). Styles: 4 a 30 s (contrato MCP).
6. **Referencias:** hasta **30 imágenes** en la UI (página de producto y blog) · **1 a 8** en el API (Comfy Router: "URLs of 1 to 8 reference images for the cast, location and style") · Styles: hasta **5** opcionales (contrato MCP). El MCP no declara tope para los modelos directos.
7. **Salida:** 480p, 720p (por defecto) o 1080p (`models_explore`; blog "up to 1080p"). `aspect_ratios: []` en el MCP: no se elige ratio.
8. **Elements NO aplican:** `hf_mult_motion_control` y `hf_mult_replace_object` no están en la lista de modelos que honran `<<<element_id>>>` ("Other models ignore the placeholder", contrato de `manage_reference_elements`, 2026-10-15). Un personaje guardado como Element entra a Genjutsu **por su imagen fuente**, como referencia.
9. **Costo (blog, verificado por Higgsfield en sep-2026):** clip de 15 s = **40 cr a 480p · 104 cr a 720p · 144 cr a 1080p**; Motion Transfer y Object Swap cuestan lo mismo; "Credit costs may vary by generation settings". Styles: el precio sale de `get_presets` con `initial_inputs` (contrato MCP); no hay tabla pública.
10. **Uso comercial:** los resultados se publican en canales orgánicos y pagados "subject to Higgsfield's Terms of Use" (FAQ de la página de producto).

## Plantillas

**A — Motion Transfer (recast de una toma real)**
```
Keep the original motion, camera move and timing of the source video.
Recast [the person on screen / the person on the left] as the character in reference image [N]: [2-3 stable traits only — silhouette, fur/skin, signature prop].
[Optional] Set the scene in the location from reference image [M]. [Light/look in one clause].
```

**B — Object Swap (cambiar un elemento, todo lo demás intacto)**
```
Replace [the exact element as it appears in the source: e.g. the red can in her right hand] with [the item in reference image N].
Keep everything else in the shot unchanged: people, camera, lighting and background.
```

**C — Style (restyle de un video propio)**
```
[Optional — 1 line] Keep [what must survive the restyle: the logo on the shirt / the product label] recognizable.
```
(El look lo pone el `genjutsu-style:<id>`; el prompt solo afina. Referencias opcionales, máx. 5, para meter tus personajes, productos o ropa.)

## Parámetros

- `model`: `hf_mult_motion_control` | `hf_mult_replace_object` (vía `generate_video`). Styles y presets van por `get_presets` → `execute_preset`, no por `generate_video`.
- `resolution`: `480p` | `720p` (defecto) | `1080p`. Sin `duration` ni `aspect_ratio`: la duración la fija el video fuente.
- `get_cost: true` cotiza sin generar — siempre antes de disparar. Las generaciones gratis de Genjutsu (`use_free_gens`) **no están disponibles** por el conector MCP (contrato `/genjutsu`).
- Styles de la galería (2026-10-15, 20 en total): Hand-Painted Cel Animation, Knitted Yarn World, Expressive 2D Animation, Rounded Toy CGI, Felt Puppet Stop Motion, Grotesque Street CGI, Warm Painterly 3D Animation, Graphic Cel, Expressive Gouache Fashion, Sculptural 3D Fashion, Chunky Textured Low-Poly, Cel-Shaded CG Anime, Painterly Cinematic 3D, Outline-free Cel, Painterly Sculpted Animation, Neon Graphic Cinematic 3D, Textured Gouache Character Illustration, Comic 3D, Retro Game 3D, Nighttime Anime Pixel Art (`get_presets source:"genjutsu" category:"genjutsu-styles"`).

## Gotchas documentados

- **Los ejemplos del catálogo no son tus insumos:** el personaje de un preset es solo muestra; las referencias deben ser las del usuario (contrato MCP). Un preset no es permiso para generar.
- **Los límites de referencias cambian por puerta** (30 UI · 1-8 API · 5 Styles): una receta armada en la UI con 12 referencias no corre igual por API.
- **Elements ignorados** (ver gramática 8): escribir `<<<uuid>>>` en el prompt de Genjutsu no mete al personaje; hay que subir su imagen.
- **Ratio heredado:** al no haber `aspect_ratio`, grabar o reencuadrar el video fuente al ratio destino ANTES de pasarlo (inferencia del esquema; no hay doc que diga cómo trata un ratio raro).

## Folklore de comunidad

- **Lipsync y actuación facial se transfieren** — `anecdótico`. Creative AI News (Vannarot Roeung, 2026-09-01, nota de lanzamiento de 1 min) dice que "transfers the acting, lip sync, camera movement, and VFX"; el resumen de Digg de posts en X (sep-2026) cita "especially the lip sync". **Ninguna fuente oficial lo afirma ni lo niega**; ver hueco abajo.
- **Personajes no humanos funcionan en recast** — `anecdótico`. Pruebas con Pudgy Penguins insertados en clips existentes (posts en X recogidos por Digg, sep-2026). No dice nada de la boca.
- **Interacción física y oclusión rompen el resultado** — `reproducible` (consistente con cómo opera la transferencia por referencia). Kapwing (Emily Peng, 2026-10-04, competidor directo): abrazos, peleas, cruces de cuerpos, pases rápidos y oclusión frecuente causan deriva de identidad o movimiento asignado al sujeto equivocado; varias personas encimadas es lo más difícil.
- **Toma limpia = mejor resultado:** video bien iluminado, sujeto visible, blocking claro; filmar el movimiento una vez y reusarlo como plantilla para varias versiones — `anecdótico` (Creative AI News 2026-09-01; T—Zh, Даша Лейзаренко, 2026-09-25).
- **`@` para etiquetar las referencias subidas en el prompt de la UI** — `anecdótico` (T—Zh 2026-09-25). Por MCP no existe ese mecanismo documentado.
- **Precio por API ≈ <costo interno> a 720p** — `anecdótico` (agregador llm-stats.com, 2026-10-15; no confirmado por Higgsfield).
- **Lanzado 2026-09-01; la capacidad se parece a Seedance 2.5; Higgsfield no revela el modelo de fondo** — `anecdótico` (T—Zh 2026-09-25).

## Iteración

Fijar el video fuente y las referencias como invariantes; cambiar UNA cosa por corrida (una referencia, o la línea del prompt, o la resolución). Probar primero en **480p con un recorte de 4-5 s** del tramo más difícil (la boca, la mano con el producto) y subir a 720p/1080p solo cuando eso pase. Definir antes qué tiene que verse para aprobar (p. ej. "la boca abre y cierra en las sílabas fuertes").

## Huecos declarados

- 🔲 hueco: **¿Motion Transfer transfiere boca/lipsync o solo cuerpo y cámara?** La doc oficial solo promete "motion, camera and timing". Hay testimonios de que sí conserva el lipsync, pero ninguno oficial ni medido, y ninguno con un personaje de hocico (un personaje recurrente). Resolver con una prueba propia de 4-5 s a 480p antes de planear una escena hablada sobre esto.
- 🔲 hueco: **¿el audio del video fuente se conserva en la salida?** Ninguna fuente lo dice.
- 🔲 hueco: cómo referir una imagen concreta desde el prompt por MCP (¿"reference image 2" por orden de subida?). Las plantillas usan orden de subida como convención, sin confirmar.
- 🔲 hueco: tope de imágenes de referencia en el MCP para los modelos directos; precio de Styles; si el costo escala lineal con la duración (solo hay tabla de 15 s).
- 🔲 hueco: discrepancia de roles `image`/`video` (contrato) vs `image_references`/`video_references` (`models_explore`).

## Historial

- 2026-10-15 — alta de la ficha (Genjutsu a 6 semanas del lanzamiento; doc oficial escasa: página de producto + blog, sin artículo de help center).
