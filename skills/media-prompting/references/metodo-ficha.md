# Molde de ficha de prompting por herramienta

Toda ficha `ficha-<herramienta>.md` sigue esta estructura. El valor de la ficha es que un agente pueda redactar un prompt correcto **sin conocer la herramienta de antemano** y sin mezclar prácticas de otros modelos.

## Frontmatter obligatorio

```yaml
---
herramienta: <nombre comercial>
modelo-vigente: <versión exacta a la fecha>
dominio: imagen | video | voz | musica
updated: AAAA-MM-DD
status: vigente | stale   # stale lo marca el vigía cuando detecta modelo/guía nueva
---
```

## Secciones (en este orden)

1. **Identidad** (3-5 líneas): qué es, qué la distingue, cuándo elegirla y cuándo no.
2. **Gramática oficial** — la sintaxis documentada por el proveedor: estructura/fórmula del prompt, orden de slots, sintaxis literal (brackets, comillas, tags), límites (caracteres, duración, ratios, resoluciones). **Cada afirmación con URL + fecha de consulta.**
3. **Plantilla(s) con slots** — lista(s) para llenar, en inglés, con `[SLOTS]` entre corchetes. Una plantilla por caso de uso principal (no más de 3).
4. **Parámetros de generación** — ratios, duraciones, resoluciones, campos de API relevantes.
5. **Gotchas documentados** — qué NO funciona (negativos sí/no, texto, manos, físicas), con fuente.
6. **Folklore de comunidad** — trucos NO oficiales que parecen funcionar. Cada uno con procedencia (foro/autor/fecha) y nivel de confianza (`reproducible` si está anclado en la arquitectura del modelo / `anecdótico` si es correlación). **Nunca se promueve folklore a gramática sin fuente oficial.**
7. **Iteración** — cómo refinar sin romper lo logrado (cambio único, invariantes, anclas).
8. **Historial** — una línea por reescritura: fecha, qué versión del modelo la motivó.

## Reglas duras

- **Prohibido copiar cláusulas entre fichas** sin verificar que aplican al modelo destino: los quality tags son específicos de cada modelo y trasplantarlos es el error #1 documentado (cargo cult).
- **Autocontenida:** sin rutas del ecosistema (G:\, C:\dev) ni referencias a otros docs internos — la ficha viaja tal cual a la edición portable.
- **Toda cifra con procedencia** (límite de caracteres, precio, duración máxima): fuente + fecha.
- Los fragmentos de prompt van **en inglés**; la prosa explicativa en español.
