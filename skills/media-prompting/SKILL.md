---
name: media-prompting
description: Experto en prompting de contenido generativo (imagen + video) — dado un requerimiento, emite el prompt optimizado para la herramienta concreta que lo va a ejecutar, usando la ficha de sintaxis de ESA herramienta. Usar cuando el usuario pida "un prompt para [Higgsfield/Seedance/Kling/Veo/InfiniteTalk/GPT Image/Nano Banana/ChatGPT/Gemini]", "ayúdame a promptear este video/imagen", o pida generar un asset visual con IA y haga falta redactar el prompt. NO ejecuta la generación — entrega el prompt listo para pegar en la herramienta.
tags: [sop, imagen, video]
---

# media-prompting — prompts optimizados por herramienta (edición portable Colek)

> **Edición portable v2026-08-13 — distribuida por el repo `colek-skills`. NO editar estos archivos a mano: cualquier cambio se pierde en la siguiente actualización. Mejoras y correcciones → avisar a Adrian.**

Cada modelo de IA tiene gramática propia: un prompt escrito "en general" desperdicia (o rompe) las fortalezas del modelo que lo va a ejecutar. Esta skill produce **el prompt correcto para la herramienta concreta**, usando fichas de sintaxis por herramienta en `references\`.

## Flujo

1. **¿Qué herramienta va a ejecutar el prompt?** Si el usuario no la dijo, preguntarla (en Higgsfield, preguntar también QUÉ modelo eligió en la UI: Seedance, Kling, Veo…). Si el usuario pide recomendación: video multi-shot/ads → Seedance · personajes 4K → Kling · exteriores/atmósfera → Veo · imagen con texto/labels → Nano Banana · composición instruida compleja → GPT Image.
2. **Cargar SOLO la ficha de esa herramienta** (`references\ficha-<herramienta>.md`). En Higgsfield: la ficha de plataforma (`ficha-higgsfield.md`) + la ficha del modelo elegido.
3. **Ficha canónica del requerimiento** (una sola vez, en inglés): sujeto, acción, contexto, estilo, restricciones (duración, ratio, texto en pantalla). **La referencia visual manda**: si el estilo importa y no hay referencia, preguntarla.
4. **Llenar la plantilla de la ficha** respetando su gramática (orden de slots, sintaxis literal, negativos sí/no) y entregar: **prompt en bloque de código + parámetros** (ratio, duración, resolución) **+ los 2-3 gotchas relevantes** al caso.
5. **Iterar:** UN cambio por ronda, re-afirmando los invariantes, como indique la ficha. Nunca reescribir todo el prompt para corregir un detalle.

## Reglas duras

- **Prohibido trasplantar cláusulas entre modelos** sin verificar en la ficha destino: los "adjetivos mágicos" (masterpiece, 8k, score_9…) son específicos de cada modelo y copiarlos entre plataformas es el error #1 documentado.
- En cada ficha, la sección **Gramática oficial** es confiable (viene de docs del proveedor, con fuente y fecha); la sección **Folklore** trae su nivel de confianza — usar con criterio.
- Los prompts van **en inglés** salvo que la herramienta indique otra cosa; el texto literal que deba aparecer en pantalla, entre comillas y verbatim.

## Fichas disponibles

| Ficha | Herramienta | Dominio |
|---|---|---|
| `ficha-gpt-image.md` | GPT Image 2 (OpenAI / ChatGPT) | imagen |
| `ficha-nano-banana.md` | Nano Banana / Gemini (Google) | imagen |
| `ficha-higgsfield.md` | Higgsfield (plataforma) | video |
| `ficha-seedance.md` | Seedance 2.x (ByteDance) | video |
| `ficha-kling.md` | Kling 2.x/3 (Kuaishou) | video |
| `ficha-veo.md` | Veo 3.x (Google) | video |
| `ficha-infinitetalk.md` | InfiniteTalk (talking head / dubbing audio-driven) | video |

Para hojas de personaje multi-vista (character sheets), usar la skill hermana `image-character-sheet`.
