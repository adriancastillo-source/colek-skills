---
herramienta: sync. labs lipsync (sync-3 / lipsync-2-pro / lipsync-2), servido en fal como sync-lipsync y en la app de ElevenLabs como "Sync 3"
modelo-vigente: sync-3 (fal `fal-ai/sync-lipsync/v3`) · lipsync-2-pro (`fal-ai/sync-lipsync/v2/pro`) · lipsync-2 (`fal-ai/sync-lipsync/v2`)
dominio: video
updated: 2026-10-29
status: vigente
---

# Ficha de prompting — sync. labs lipsync (sync-3 y familia)

## ⚠️ Desambiguación — un modelo, tres puertas

| Puerta | Nombre que ve el usuario | ¿Es el mismo modelo? | API |
|---|---|---|---|
| **fal** | `fal-ai/sync-lipsync/v3` ("sync-3 Lipsync") | Sí. fal lo lista como modelo *Partner* y sus opciones remiten a Sync.so | Sí, con llave de fal |
| **sync.so** | `sync-3` en `POST /v2/generate` | Es el fabricante (sync. labs) | Sí, con cuenta propia de sync.so |
| **ElevenLabs Image & Video** | "Sync 3" y "Sync Lipsync 2 Pro" | Sí. La doc de ElevenLabs lo describe como *"The latest generation video lip-sync model from Sync"* | **No por API**: la API de Image & Video expone un subconjunto que no incluye Sync 3 (solo la app web) |

Fuentes: [fal.ai/models/fal-ai/sync-lipsync/v3/api](https://fal.ai/models/fal-ai/sync-lipsync/v3/api); [sync.so/docs/models/lipsync](https://sync.so/docs/models/lipsync); [elevenlabs.io/docs/eleven-creative/playground/image-video](https://elevenlabs.io/docs/eleven-creative/playground/image-video) §Lip-sync models; [elevenlabs.io/docs/eleven-api/guides/cookbooks/image-and-video](https://elevenlabs.io/docs/eleven-api/guides/cookbooks/image-and-video) §Available models. Todo leído el 2026-10-29.

**No traduce.** Los tres endpoints de fal reciben un video y un audio ya hecho y rehacen la boca para ese audio. La traducción con voz es otro paso: un doblaje (p. ej. ElevenLabs Dubbing) o un TTS propio. sync.so sí ofrece doblaje dentro de su API (`dubParams`, con ElevenLabs como proveedor), pero eso es su plataforma, no el endpoint de fal.

## 1. Identidad

Lipsync **video a video**: toma una toma ya generada o filmada y rehace solo la boca para un audio nuevo. No re-actúa el cuerpo ni genera desde imagen. Elegirlo para cambiar el idioma o corregir el diálogo de un clip que ya existe. No elegirlo para animar un retrato fijo (eso es un motor de avatar), ni cuando el personaje no es humanoide (§5).

## 2. Gramática oficial

**No hay prompt de texto.** Lo que se "redacta" son las entradas y las opciones.

### Entradas en fal (`fal-ai/sync-lipsync/v3`)
- `video_url` (requerido) y `audio_url` (requerido). Formatos aceptados según la página del modelo: video *"mp4, mov, webm, m4v, gif"*; audio *"mp3, ogg, wav, m4a, aac"* ([fal.ai/models/fal-ai/sync-lipsync/v3](https://fal.ai/models/fal-ai/sync-lipsync/v3), 2026-10-29).
- `sync_mode` (def. `cut_off`): `cut_off | loop | bounce | silence | remap`. Decide qué pasa cuando el audio y el video no duran lo mismo (tabla abajo).
- `enable_safety_checker` (def. `true`).
- `options` (objeto `Sync3GenerationOptions`): `options.sync_mode` pisa al de arriba; `active_speaker_detection` (`auto_detect`, `frame_number`, `coordinates`, `bounding_boxes`, `bounding_boxes_url`, `face_image`) para elegir la cara. **Ignorados por sync-3** según la misma página: `temperature` (*"ignored by sync-3"*), `occlusion_detection_enabled` (Sync.so *"handles this automatically for sync-3"*), y `model_mode` y `prompt` (emociones), que son *"primarily used by react-1"*.
- **No hay campo `model` ni `temperature`** en el nivel de arriba: el modelo lo fija el endpoint (`v3`, `v2/pro`, `v2`).
- Salida: `video` (`url`, `content_type`, `file_name`, `file_size`).

### `sync_mode` — qué hace cada uno ([sync.so/docs/developer-guides/sync-mode](https://sync.so/docs/developer-guides/sync-mode), 2026-10-29)

| Modo | Audio más largo que el video | Video más largo que el audio | Duración de salida |
|---|---|---|---|
| `cut_off` | **El audio se corta** al largo del video | El video se recorta | La más corta |
| `silence` | Se conserva todo el audio | El audio se rellena con silencio | La más larga |
| `remap` | El video se **alenta** | El video se **acelera** | La del audio |
| `loop` / `bounce` | El video se repite (o va y vuelve) | El video se recorta | La del audio |

*"For the most predictable result, make your video and audio durations close before submitting."*

### Los tres modelos ([sync.so/docs/models/lipsync](https://sync.so/docs/models/lipsync), 2026-10-29)

| | lipsync-2 | lipsync-2-pro | sync-3 |
|---|---|---|---|
| Para qué, según sync | *"best lipsync for majority of the videos"* | *"Seamlessly generates facial details with beards, wrinkles, and teeth"* | *"Handles close-ups, profile shots, obstructions, and complex scenes"* |
| Resolución de cara | 512×512 | 512×512 con detalle mejorado | *"4K native output with built-in super resolution"* |
| Obstrucciones | opción `occlusion_detection_enabled` (más lento) | igual | automáticas |
| Precio en sync.so @25 fps | <costo interno>–0.05/s | <costo interno>–0.083/s | <costo interno>–0.133/s |
| **Precio en fal** (API de precios de fal, 2026-10-29) | **<costo interno>/min** | **<costo interno>/min** | **<costo interno>/min** (= <costo interno>) |

### Límites
- **Personajes:** *"You can lipsync human-like faces, but our models don't currently support animals or non-humanoid characters"* (FAQ de [sync.so/docs/models/lipsync](https://sync.so/docs/models/lipsync)). La doc de ElevenLabs dice que Sync 3 está *"Optimized for all content types including live-action, 3D animation, and AI-generated video"*. Las dos cosas se cumplen a la vez: 3D sí, mientras la cara sea humanoide.
- **Calidad de entrada** ([sync.so/docs/product/troubleshooting](https://sync.so/docs/product/troubleshooting), 2026-10-29): cara de frente, bien iluminada, *"at a minimum of 480p"*; *"Avoid obstructions like hands, microphones, or hair covering the mouth area"*; *"Use clean audio without background music or overlapping speakers, as noise degrades lip-to-audio alignment."*
- **Duración máxima:** en sync.so depende del plan (1 min en Hobbyist hasta 30 min en Scale). **En fal no está publicada** (sin verificar).
- **Idioma:** sync dice que sus modelos son *"language-agnostic"* (tutorial de doblaje por API); ElevenLabs anuncia *"95+ languages"* para Sync 3. No hay lista de idiomas porque el modelo sigue el audio, no un texto.

## 3. Plantillas con slots

**A — Cambio de idioma con un audio ya doblado (caso principal):**
```json
{
  "video_url": "[CLIP ORIGINAL, sin re-encodear de más]",
  "audio_url": "[VOZ DOBLADA SOLA, sin música: el aislado de la pista doblada]",
  "sync_mode": "[cut_off si el doblaje ya respeta la duración | silence si el audio dura más y no se quiere cortar | remap solo si la diferencia es mínima]"
}
```
La pista final (voz más música) se pega después sobre el video que devuelve el modelo.

**B — Clip con más de una cara, o una cara difícil de detectar:**
```json
{
  "video_url": "[CLIP]", "audio_url": "[VOZ SOLA]",
  "options": { "active_speaker_detection": { "auto_detect": false, "frame_number": [N], "coordinates": [[X], [Y]] } }
}
```

**C — Variante barata de la misma familia (para comparar en un torneo):** misma forma que A contra `fal-ai/sync-lipsync/v2/pro` (sync recomienda esa versión para barbas) o `fal-ai/sync-lipsync/v2`.

## 4. Parámetros de generación

- Costo de un clip en fal = segundos de salida × tarifa: 27 s ≈ **<costo interno>** con sync-3, <costo interno> con v2-pro, <costo interno> con v2 (cálculo sobre los precios por minuto de fal; que cobre por segundo exacto y no por minuto redondeado **no está verificado**).
- La resolución de salida sigue al video de entrada; sync-3 aplica superresolución en la cara.
- Formato: mandar audio WAV o MP3 limpio, mono o estéreo.

## 5. Gotchas documentados

- **Caras no humanoides: no soportadas** (FAQ de sync, arriba). Una criatura con cara humanoide, nariz y boca en su lugar entra en zona gris: hay que probarla.
- **Pelo o barba sobre la boca degrada el resultado** (troubleshooting de sync). sync-3 maneja obstrucciones solo; lipsync-2-pro se anuncia para barbas.
- **La música en el audio de entrada empeora la sincronía.** Se manda la voz sola y la mezcla se pega después.
- **`cut_off` es el default y corta el audio si dura más que el video.** Una traducción al español o al francés suele durar más que el inglés. Revisar la duración antes de mandar, o usar `silence`.
- **Ignorados en sync-3:** `temperature`, `model_mode`, `prompt` de emoción y `occlusion_detection_enabled`. Mandarlos no cambia nada.
- **Videos largos:** sync procesa por tramos de 30 a 40 s; un corte de escena dentro de un tramo puede confundir el seguimiento de la cara (troubleshooting). Un clip de un solo plano no tiene ese problema.

## 6. Folklore de comunidad

Sin folklore incorporado. Lo medido en el estudio sobre sync-3 (en un retrato fotorrealista, 2026-08) se resume aquí, no como ley general:
- **Re-encodea todo el cuadro**: la boca mejora pero la nitidez del resto baja. Extraer solo el parche de la boca y pegarlo sobre la toma original recupera buena parte de la nitidez. `reproducible` (es un re-encode del cuadro completo).
- **Devuelve 25.075 fps**: forzar la tasa del proyecto al integrar. `reproducible` en esa corrida.
- lipsync-2 (v2) no encontró la cara en personajes de palito (2026-07). No se ha probado con personajes 3D humanoides.

## 7. Iteración

No hay prompt que ajustar: se itera la **entrada**. En este orden: (1) audio limpio, sin música ni reverb; (2) duraciones parecidas y el `sync_mode` correcto; (3) cara clara (encuadre, `active_speaker_detection`); (4) subir de modelo (v2 → v2-pro → sync-3). Una corrida es una toma: guardar la buena.

## 8. Historial

- 2026-10-29 — ficha creada desde la doc oficial de fal (endpoint v3 y API de precios), sync.so (modelos, sync_mode, troubleshooting, FAQ) y ElevenLabs (Image & Video), para el torneo de cambio de idioma de clips con lipsync. Resuelve que el "Sync 3" de ElevenLabs y el `sync-lipsync/v3` de fal son el mismo modelo de sync. labs.
