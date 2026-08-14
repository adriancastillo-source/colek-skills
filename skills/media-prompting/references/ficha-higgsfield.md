---
herramienta: Higgsfield (plataforma agregadora)
modelo-vigente: plataforma — envuelve Seedance 2.0, Kling 3.0, Veo 3.1, WAN 2.6, MiniMax (video) y Soul 2.0, Nano Banana Pro, Seedream 5.0, Flux 2, GPT Image 2 (imagen); Cinema Studio 3.5
dominio: video
updated: 2026-08-13
status: vigente
---

# Ficha: Higgsfield (plataforma)

## Identidad

Higgsfield NO es un modelo: es un **agregador multi-modelo** (15+ bajo una suscripción) con capa propia de producto (presets de cámara, Cinema Studio, Soul ID, Popcorn) y modelo propio solo en imagen (Soul 2.0). **Consecuencia rectora: la sintaxis del prompt es la del MODELO subyacente elegido** — usar la ficha de ese modelo (`ficha-seedance.md`, `ficha-kling.md`, `ficha-veo.md`) para redactar, y ESTA ficha para las reglas de la plataforma. Elegirlo cuando se trabaja en su UI (el caso de los editores); no aplica si se llama al modelo por API directa.

> **Versiones dentro del agregador ≠ versiones de API.** A 2026-08 Higgsfield ofrece **Seedance 2.0** (no 2.5): de `ficha-seedance.md` aplican los brackets `()<>{}【】` y las @refs (gramática 2.0), pero NO los timestamps ni las tomas de 30 s (eso es 2.5). Regla general: **verificar la versión visible en la UI de Higgsfield antes de usar rasgos exclusivos de una versión** — el agregador va detrás de las APIs.

## Gramática oficial (reglas de plataforma)

Fuentes: higgsfield.ai/sora-2-prompt-guide + higgsfield.ai/blog/cinema-studio-3.0 + help center Soul ID/Popcorn (consultadas 2026-08-13). Reglas de oficio adaptadas de la skill MIT `OSideMedia/higgsfield-ai-prompt-skill` (v3.31, ago-2026) — atribución abajo.

1. **Lo que se selecciona en la UI NO va en el prompt.** Duración, aspect ratio, resolución y modelo son settings de la app — escribirlos inline no hace nada. El campo de prompt es SOLO descripción de escena.
2. **Un movimiento de cámara por clip.** Los 50+ presets (crash zoom, dolly, whip pan, FPV drone…) **no se combinan**; apilar movimientos ensucia el render. Mejor práctica: elegir el preset en la UI **y repetir el movimiento en el texto** ("crash zoom in") — nombrarlo en ambos lados es lo más repetible.
3. **Personajes por identidad, no por descripción:** en Cinema Studio van con **@ tags / Elements**; el prompt describe acción y escena, no la cara del personaje. Presupuesto ~512 caracteres en Cinema Studio (los @ Elements consumen parte).
4. **Un cambio de estado por generación** (una acción, un beat): "tie one camera move to one character action per beat" (guía oficial Sora 2 de Higgsfield).
5. **Diálogo en bloque dedicado** ("Dialogue:") para lip-sync y entrega verbatim (misma guía).
6. **Consistencia — dos productos distintos:** **Soul ID** = identidad entrenada (20-80 fotos), persiste entre sesiones y modelos, ~90% facial (perfiles y ángulos extremos la rompen). **Popcorn** = memoria visual frame-a-frame DENTRO de una sesión (storyboards/secuencias de imagen). No confundirlos.

## Plantilla (esqueleto MCSLA, adaptado de OSideMedia, MIT)

Cinco capas, en orden — ≤200 palabras en short-form; la sintaxis fina la pone la ficha del modelo elegido:

```
[MODEL — se fija en la UI, no se escribe; decide qué ficha de sintaxis usar]
[CAMERA: one single move — named in UI preset AND restated in text]
[SUBJECT: @tag o Element si existe; si no, sujeto en una frase]
[LOOK: estilo, luz, atmósfera, paleta]
[ACTION: UN cambio de estado / beat, con foreground-midground-background anclados]
[Dialogue: "..." — bloque aparte, solo si hay habla]
```

## Guía de elección de modelo (la que publica el propio Higgsfield)

Seedance 2.0 = multi-shot/ads · Veo 3.1 = exteriores/atmósfera · Kling 3.0 = personajes en 4K · MiniMax = short-form rápido · WAN 2.6 = restyle de footage existente.

## Gotchas documentados

- **La pata Sora 2 tiene fecha de caducidad:** OpenAI descontinuó Sora en 2026 (anuncio de OpenAI; cierre de API reportado para sep-2026 — verificar antes de montar cualquier flujo sobre ella).
- Lip-sync imperfecto en habla rápida (heredado del modelo subyacente).
- Licenciamiento comercial **ambiguo** para likenesses humanos generados — precaución en trabajo de cliente.
- Sin Soul ID no hay identidad persistente de personaje entre sesiones.

## Folklore de comunidad

- "Preset en UI + movimiento repetido en texto" — `reproducible` (cheat sheet Memons + reviews 2026; consistente con la doc oficial).
- Créditos: expiran a 90 días sin rollover, 720p ≈ 1-1.5 créditos/seg, y el rendimiento real incluye 3-5 reintentos por pieza — `anecdótico` (reviews 2026, sin doc oficial de Higgsfield que lo confirme); presupuestar con margen.

## Iteración

Una variable por ciclo de iteración (criterio DISCIPLINE de OSideMedia, adoptado): cambiar cámara O acción O look, nunca dos a la vez. Definir el criterio de éxito falsificable ANTES de generar (¿qué tiene que verse para aprobar?). La iteración de identidad va por Soul ID/Popcorn, no por reescribir la descripción.

## Atribución

Reglas de oficio adaptadas de `github.com/OSideMedia/higgsfield-ai-prompt-skill` (MIT License, Copyright OSideMedia) — se adoptó criterio (MCSLA, UI-vs-prompt, un cambio de estado), no su estructura ni scripts.

## Historial

- 2026-08-13 — alta de la ficha (plataforma con Cinema Studio 3.5; Seedance 2.0/Kling 3.0/Veo 3.1 como motores de video).
