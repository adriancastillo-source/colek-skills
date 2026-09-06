---
herramienta: Wan (Alibaba)
modelo-vigente: Wan 3.0 (beta pública 2026-08-07, GA 2026-08-24); línea 2.2 vigente para animate/replace
dominio: video
updated: 2026-09-05
status: vigente
---

# Ficha: Wan 3.0

## Identidad

Modelo multimodal de video de Alibaba que junta en uno solo: texto-a-video, imagen-a-video con primer
y último frame, generación por referencias, edición localizada y extensión temporal. Acepta imagen,
video, audio, **documentos y páginas web** como entrada. Elegirlo para: tomas largas (hasta 30 s en
una pasada), trabajo por referencias, y cuando el precio por segundo manda. **No** elegirlo para
coreografía compleja o peleas — ver gotchas.

Comparte con Seedance el sistema de referencias `@` y el rango de duración, pero **su gramática es de
orden, no de brackets**: donde Seedance tipa canales con símbolos, Wan ordena categorías. No
trasplantar los brackets `{ }` `< >` `( )` de Seedance aquí.

## Gramática oficial

Fuentes: guía de prompting de Wan 3.0 publicada por **Runware** —proveedor que sirve el modelo, no
Alibaba directo— en runware.ai/docs/models/alibaba-wan3-0/guides/prompting, y el esquema de entrada
de fal en fal.ai/models/alibaba/wan-3.0/reference-to-video/api. Ambas consultadas **2026-09-01**.

### La regla que gobierna todo: el ORDEN es la sintaxis

Wan lee el prompt como **directivas por capas**, y el orden pesa más que la redacción:

> **`Sujeto → Acción → Entorno → Cámara → Audio`**
>
> *"Order matters more than sentence structure. A prompt that leads with the subject and setting,
> then moves to action, then camera, then audio, lands more predictably."*

Corolario que decide resultados: **el modelo prioriza lo que nombras explícitamente por encima de lo
que dejas abierto** — *"underspecified prompts get the model's defaults"*. Lo que no se nombra, lo
inventa el modelo.

### Cámara: nombrarla NO es opcional

Wan reconoce seis movimientos por nombre: **static/locked · dolly · pull-back · pan/tilt · orbit ·
handheld tracking**. Se pueden emparejar con óptica ("35mm lens, shallow depth of field").

> **La cita que más importa de toda esta ficha:** nombrar la cámara evita que *"the model animates
> the subject to compensate for a static camera"*. Es decir: **si quieres una toma quieta y no
> declaras la cámara como bloqueada, Wan mueve al personaje para compensar.** Para plano fijo, la
> forma documentada es `"Camera locked at eye level"` — no basta con escribir "static camera" al
> final como coletilla.

### Prosa declarativa, no listas de keywords

*"Write plain declarative prose"* y evitar listas de palabras clave. La densidad tiene techo: *"past
a few hundred well-chosen words, the model's attention narrows"*.

### Audio

El audio es directiva de primera clase, en la misma petición. El diálogo va **entre comillas** y el
modelo lo sincroniza con el hablante visible; conviene cerrar con `"no on-screen text"` para que no
lo queme como subtítulo. Los sonidos se piden con **verbos atados a un evento visible** ("the soft
haptic tick of the thumb tapping the screen"), no con adjetivos genéricos ("realistic phone sounds"),
y se ordenan por prominencia con marcas espaciales ("foreground", "distant", "off-camera").

Para suprimir audio del todo: parámetro `audio: false` (en fal), no una frase en el prompt.

### Negativos: NO documentados

La guía **no cubre prompts negativos** y el esquema de fal no expone un campo para ellos. Es una
diferencia dura con Seedance, cuya gramática **sí** documenta negativos literales. En Wan, lo que
funciona documentado es **decir qué SÍ ocurre**, no qué no debe ocurrir.

## Plantillas

### A — Animar un keyframe con movimiento mínimo (plate / beat sin diálogo)

```
[SUBJECT: who is in frame, 2-3 stable traits each, as shown in @Image1].
[ACTION: what moves, in plain prose, with adverbs that calibrate amplitude — "slowly",
 "barely", "once"]. [What stays put, stated positively: hands remain resting on X,
 the document stays in her hands, lips stay together].
[SETTING: location and props that must not change].
Camera locked at [eye level / the framing of @Image1], no camera movement.
[STYLE: visual register in one clause].
```

### B — Toma con diálogo

```
[SUBJECT]. [ACTION].
[SETTING].
Camera [named move] with [lens].
[SPEAKER, identified by visible traits] says, "[exact line]".
Audio: [foreground sound, verb-based], [distant sound]. No on-screen text.
```

### C — Toma larga (una sola pasada, 10-30 s)

Escribirla como **un movimiento que evoluciona**, con principio, giro y final — *"write the arc, not
the subject"*. ⚠️ El multi-shot por timestamps **NO dirige el momento del corte** — ver §D2.

### D — 🔒 SELLADA: toma de una serie de sketches (estilo plano con diálogo) *(el director, 2026-09-03)*

> **Wan 3.0 es la herramienta oficial para generar una serie de sketches.** Esta plantilla es la que produjo las tomas
> aprobadas; se usa tal cual, cambiando sólo lo que va en `<…>`.

**Insumos:** el keyframe del **set completo aprobado** como `@Image1` (no un personaje recortado) ·
la locución montada como `reference_audio_urls` → `@Audio1` · `--dur` = duración del audio **redondeada
hacia arriba** · 720p · el aspecto del proyecto.

**Los seis bloques, en este orden** — el orden ES la sintaxis en Wan:

1. **Estilo + referencia.** `"A flat-vector cartoon <escena> in a minimal stick-figure style with
   thick black outlines and flat colour fills, exactly as shown in @Image1."`
2. **Cada personaje por rasgos visibles**, no por nombre: *"a young man with a round white head, an
   orange t-shirt and thin black stick limbs, sitting in the visitor chair on the left"*. El modelo
   no sabe quién es un personaje recurrente; sabe qué es una playera naranja.
3. **El reparto de turnos por SEGUNDOS**, sin transcribir el diálogo: *"They speak the Mexican
   Spanish dialogue in @Audio1, taking turns. The woman speaks for the first six seconds while the
   young man listens; then, in the last two seconds, the young man asks a short question."* Más
   `"Each character's mouth moves only during their own line in @Audio1."`
   **Medido:** transcribir las líneas **no ayuda** (r 0.927 citando vs 0.954 sin citar).
4. **La expresión como GEOMETRÍA**, nunca como emoción — Wan no admite negativos. La cara `-.-'`:
   *"his eyebrows are straight flat lines angled slightly down toward the centre, his eyes are
   narrowed to thin half-lidded slits, and his mouth is one short straight horizontal line"*.
   **Repetirla íntegra en cada plano**: Wan conserva lo que se nombra y olvida lo que se nombra una
   sola vez.
5. **El set, objeto por objeto.** *"The desk, the laptop, the clipboard, the two blank white sheets,
   the framed poster, the potted plant and every colour and outline stay exactly as they are in
   @Image1."* Lo que no se nombra, se autoriza a reinventarlo.
6. **Cámara y cierre.** `"Camera locked in the wide framing of @Image1 at eye level, no camera
   movement. Crisp flat vector animation, clean uniform line art, flat colour fills. Audio: the
   voices in @Audio1 in the foreground, a quiet room tone behind them. No on-screen text."`

**Para un INSERT, se genera aparte y se monta** — no se pide dentro de la toma (ver §D2). Wan compone
un encuadre nuevo desde el mismo `@Image1`: se describe el encuadre (*"a tight overhead close-up
looking straight down at the desktop"*), se listan los objetos que deben aparecer, se declara la
cámara (*"Camera locked in a top-down overhead shot"*) y va **sin audio**. Salió a la primera, <costo interno>.

### D2 — ⛔ El límite duro: el multi-shot NO dirige el corte

**Medido con n=3.** Se pidió el corte a los 5.0 s, luego a los 4.0 y luego a los 2.5 — y **cayó en el
frame 171 (5.72 s de 8) las tres veces**, sin moverse un solo frame. El timestamp no entra en la
decisión, así que **no es un sesgo compensable**.

Wan sí obedece *cuántos* planos y *en qué orden*; nunca *cuándo*. En el intento de tres planos el
insert quedó en **0.77 s** y el wide de vuelta no coincidió con el de salida (diff 11.78 contra 0.28
de frames del mismo plano).

> **Regla:** el multi-shot sirve donde el punto de corte no cargue peso narrativo. **Para una serie de sketches, que es
> humor de timing, cada plano se genera por separado y el corte se monta.**

## Parámetros

- **Referencias:** `@Image1`, `@Video1`, `@Audio1`, numeradas por orden de subida. Campo de fal:
  `reference_image_urls` (**no** `image_urls`, que es de Seedance), hasta **10** imágenes.
- **Duración:** enteros de **2 a 30 s**, o `"auto"`. La guía sugiere 5-8 s por beat.
- **Resolución y ratio:** en llamadas con entrada (imágenes/video/audio) se usa `resolution`, y el
  ratio se hereda del input; en texto-a-video puro se usan `width`/`height`. **No mandar ambos.**
  Dimensiones fijas por combinación — 9:16 da 480×832 / **720×1280** / 1080×1920.
- **`audio`** por defecto **true** en el endpoint: apagarlo explícitamente para plates mudos.
- **`seed`** para reproducibilidad.
- La respuesta trae `actual_prompt`: el prompt **expandido** que el modelo aplicó de verdad. Leerlo
  cuando una toma salga rara — puede no ser el que se escribió.

## Gotchas documentados

- **Cámara sin declarar → el sujeto se mueve de más.** Es el modo de fallo #1 y está en la guía
  oficial (ver arriba). Fuente: guía de prompting, 2026-09-01.
- **Adherencia demasiado literal al frame.** Si el prompt omite un detalle, el modelo trata el
  primer/último frame como literal: una hélice que el frame muestra quieta se queda quieta. Lo que
  deba cambiar, hay que nombrarlo. — ghost.oxen.ai/wan-30-prompting-guide, leído 2026-09-01
  (secundaria).
- **Movimiento complejo no es su fuerte**: peleas o coreografía intrincada — *"Seedance 2.5 performs
  better"*. Misma fuente secundaria, y **es una comparación de un tercero, no una medición propia**.
  Desde el 2026-09-05 hay medición propia que lo acota mejor: no es que el movimiento complejo le
  cueste, es que **el gesto sin tarea física no lo hace en absoluto** — ver §Solo se mueve si hay
  una TAREA FÍSICA.
- **Voz robótica sin acento declarado**: especificar región ("southern American English, like from
  Texas"). Misma fuente.
- **El lipsync audio-a-video no es perfecto.** Fuente secundaria — y **es el criterio que decide
  cuándo NO usar Wan**: ver §Medido en el estudio.
- **Oclusión en animación plana**: si las relaciones espaciales no se describen, las capas se pierden.

## Medido en el estudio *(2026-09-02, torneo VIDEO REF R5-R7 — reemplaza las suposiciones de arriba)*

Todo lo de esta sección es **medición propia**, no folklore. Las tomas y la bitácora viven en
`<ruta interna>`.

### El audio de referencia se devuelve INTACTO (passthrough)

**El campo es `reference_audio_urls` y es DISTINTO del flag `audio`.** Confundirlos costó una ronda
entera: R4 mandó sólo `audio: true` creyendo que medía lipsync, el modelo inventó una línea en
inglés y se leyó como *"Wan ignora el audio"*. **Nunca lo había recibido.**

Con la pista pasada de verdad, **5 clips de 5 dieron passthrough** — un cliente de entretenimiento (personajes 3D, 3 refs,
9:16 y 16:9) y una serie de sketches (stick-man plano, 1 ref, 9:16):

| Clip | Envolvente | Forma de onda |
|---|---|---|
| un cliente de entretenimiento 2a / 2b / con back / clip de 10 s | 0.93 · 0.95 · 0.98 · 0.99 | **0.88 · 0.96 · 0.98 · 0.98** |
| una serie de sketches diálogo · una serie de sketches un personaje recurrente parco | 0.997 · 0.997 | **0.970 · 0.969** |

> **Wan devuelve tu grabación, no una imitación.** Y ahí le gana a Seedance 2.0 fast por fal, que con
> `audio_urls` re-actúa (envolvente 0.334, onda 0.047) y además corrompió el texto: *"estas dos
> hojitas"* salió como *"estas dos **fotos**"*.

**⚠️ Cómo se supo mal durante una hora.** El medidor alineaba la forma de onda con la resolución de
la envolvente (10 ms = 160 muestras a 16 kHz); a esa escala una señal idéntica correlaciona ~0.20.
Con eso se escribió aquí lo contrario —"Wan clona la voz"— y se construyó una hipótesis falsa sobre
la duración del clip. **El control de "una pista contra sí misma" daba 1.000 y por eso el
instrumento pasó por bueno; faltaba el control con la misma señal DESALINEADA.** Corregido el
2026-09-02: el desfase grueso acota la ventana y dentro se busca muestra a muestra.

**Lo que sigue decidiendo entre Wan y Seedance es el lipsync**, no la voz: si el plano exige que un
editor re-sincronice la boca contra la toma sellada, Seedance. Si no —cinemáticos, personajes de
fondo, estilo plano donde la boca es una línea— Wan, y se paga 2.4× menos.

#### Los dos campos se COMBINAN: sin `--audio`, el clip sale MUDO *(medido 2026-09-04)*

Saber que son campos distintos no basta. Medido con `wan.mjs --audio-ref voz.wav` **sin** `--audio`
sobre el avatar de una mascota 3D: el job corre, cobra (<costo interno>) y devuelve un mp4 **con un solo stream, el de
video**. El audio de referencia sí llegó y sí sincronizó la boca, pero la pista no se adjunta a la
salida. Con `--audio-ref` **y** `--audio`, el mismo prompt devolvió video + audio y la transcripción
del resultado es la locución nuestra, palabra por palabra.

- `--audio-ref` sin `--audio` → **clip mudo** (la boca sincroniza, pero no hay pista).
- `--audio` sin `--audio-ref` → el modelo **inventa** la voz.
- Los dos juntos → **passthrough con pista**. Es lo que se quiere para un avatar hablando.

*Recontar:* `ffprobe -v error -show_entries stream=codec_type -of csv=p=0 <clip.mp4>` — si no
aparece la línea `audio`, salió mudo.

⚠️ El texto de ayuda del CLI decía *"no son intercambiables"*, que es cierto y aun así induce a
elegir uno: se corrigió el 2026-09-04 para decir que **se combinan**.

#### Límite duro: el audio de referencia son 15 segundos *(medido 2026-09-04)*

`reference_audio_urls` rechaza pistas más largas, antes de generar y sin cobrar:

```
422 audio_duration_too_long: "Audio duration exceeds the maximum allowed. Maximum is 15 seconds."
```

Una locución de 18.76 s no entra. **Para un parlamento más largo hay que partirlo en tomas** y
montarlas — igual que el multi-shot (§D2), la costura se decide en montaje, no dentro del modelo.

### Solo se mueve si hay una TAREA FÍSICA *(medido 2026-09-05, mascota 3D de una federacion deportiva)*

**El criterio que decide si Wan sirve para un plano.** Sobre el mismo personaje, el mismo día y con
la misma locución:

| Plano | Qué se pidió | Qué hizo |
| :--- | :--- | :--- |
| Presentador a cámara | saludar con la palma, abrir las manos al presentarse, brazos sueltos entre frases | **Brazos colgando**, casi inmóviles |
| ídem, **sin declarar la cámara** | lo mismo | Brazos colgando otra vez |
| Jugando fútbol, sin diálogo | correr con el balón, jalear de rodilla, rematar | **Corre, conduce y remata bien** |
| Jugando fútbol **y hablando** | lo mismo, más la línea | Habla bien, pero **casi no juega**: el balón aparece en cuadro y apenas lo toca |

La lectura: **Wan anima acciones, no gestos.** Un gesto pedido en prosa —"saluda", "abre las
manos"— no lo ejecuta; una acción con objeto y objetivo —correr tras un balón, patearlo— sí. Y
cuando además tiene que hablar, la atención se le va a la boca y la acción se degrada.

Se probó con la cámara bloqueada y sin ella, así que **no es el gotcha de la cámara sin declarar**
que está más arriba: es una limitación distinta y aparte.

> **Por qué una serie de sketches no lo sufre:** ahí el personaje es un *stick-man* plano cuyo cuerpo casi no actúa, y
> la plantilla sellada D pide sobre todo boca y turnos. La limitación aparece cuando el personaje es
> una figura 3D que debe presentar con las manos.

**Consecuencia práctica:** para un plano de presentador con gesto, Wan no es el motor —lo fue Kling
por costo y InfiniteTalk por calidad, en ese casting—. Para acción sin diálogo, Wan gana y es el más
barato. *Recontar: los clips y sus prompts en `<ruta interna>`.*

### Evento temporal: dos métodos, los dos funcionan

Para un cambio que ocurre DENTRO de la toma (un semáforo de ámbar a rojo), medidos lado a lado con
todo lo demás idéntico:

- **ARCO** — el cambio escrito como un movimiento continuo que evoluciona, dentro de la plantilla C:
  *"the light glows amber, and while he is still approaching it turns red, its red lamp holding
  steady"*. **Escena más coherente.** Es el default.
- **TIMESTAMPS** — `Shot 1 [0-3s]: … Shot 2 [3-6s]: …`. **Cambio más marcado**, pero se le fue la
  mano: llenó los lados de semáforos rojos extra que nadie pidió.

**Regla:** arco por defecto; timestamps sólo cuando el momento exacto del cambio importe y se acepte
más ruido en el resto del cuadro.

### El back va como referencia, y aun así como capa

Pasar el fondo de marca como `@Image3` **funciona**: reprodujo una recepción de casino entera
—damascos, morado y dorado, mostrador con luz cálida, mármol, alfombra, tragamonedas al fondo— en vez
de inventar un casino genérico como cuando sólo recibió los personajes recortados sobre blanco.

**Pero los logos no sobreviven y además DERIVAN:** el letrero de marca se leía distinto en el
segundo 0.3 y en el 8.7 del mismo clip. Es la ley de capas del AVE confirmada por otra vía: **el
back se monta como capa**, aunque el modelo lo copie bien.

### Al describir el entorno, nombrar cada elemento

Corolario del gotcha de "adherencia literal": **el modelo conserva lo que se nombra.** El prompt que
funcionó lista el mostrador, el letrero, los paneles, el piso, la alfombra y las máquinas del fondo,
uno por uno, en afirmativo. Omitir uno es autorizarlo a reinventarlo.

## Folklore de comunidad

- *"The subject's movements remain unchanged"* como frase para aislar una edición y que el resto no
  derive — `anecdótico` (ghost.oxen.ai, 2026). Es coherente con la regla oficial de nombrar
  explícitamente lo que debe permanecer, pero no aparece en la guía del proveedor.
- Adverbios de intensidad ("slowly", "barely", "sharply") para calibrar amplitud de movimiento —
  `reproducible`: está anclado en la regla oficial de que lo no nombrado cae a defaults.
- Repetir requisitos de continuidad entre cortes para sostener estilo — `anecdótico`, misma fuente.

## Iteración

Un cambio por ronda, manteniendo fijos el bloque de sujeto y la línea de cámara. Si una toma deriva,
**la primera sospecha es la línea de cámara**, no el sujeto: en este modelo la cámara mal declarada
se paga con movimiento parásito del personaje. Segunda sospecha: algo que se dio por obvio y no se
nombró.

## Historial

- 2026-09-01 — alta de la ficha (Wan 3.0). La motivó un torneo que corrió **sin** ficha y quedó en
  cuarentena: se le dio a Wan un prompt escrito en la gramática de otro modelo —estilo primero,
  cámara como coletilla final, negativos— y el personaje soltó un objeto y abrió la boca con
  `mouths CLOSED` en el prompt. La guía oficial explica ese fallo exacto en su regla de cámara.

- 2026-09-04/05 — tres mediciones nuevas desde el casting de movimiento de una mascota 3D (una federacion deportiva): los dos
  campos de audio **se combinan** (`--audio-ref` sin `--audio` devuelve el clip mudo, y se cobra
  igual); el audio de referencia **topa en 15 segundos**; y **Wan solo se mueve si hay una tarea
  física** — con el mismo personaje y la misma locución, de presentador dejó los brazos colgando en
  dos prompts distintos, y en la cancha corrió y remató bien. Las tres en §Medido en el estudio.
