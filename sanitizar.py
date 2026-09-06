# -*- coding: utf-8 -*-
"""Limpia las fichas antes de publicarlas en un repo PUBLICO de GitHub.

POR QUE EXISTE (2026-09-05). `build.ps1` copiaba `references/*.md` tal cual. En
agosto eso era inofensivo: las fichas eran tecnicas. Pero cada medicion nueva se
hizo sobre un proyecto real, y con ella entraron nombres de cliente, rutas del
Drive de Colek y costos por clip. Cuando se detecto, cuatro fichas YA PUBLICADAS
nombraban clientes, y la de Wan estaba a punto de publicar un personaje sin
lanzar. Nadie lo decidio: se fue colando ficha por ficha.

DOS CAPAS, y la segunda es la que importa:

  1. SUSTITUIR — los nombres propios se cambian por su categoria, no se borran:
     "la plantilla sellada de OBO" -> "la plantilla sellada de una serie de
     sketches". La ficha sigue ensenando; deja de decir para quien.

  2. BLOQUEAR — despues de sustituir, se busca CUALQUIER termino prohibido que
     haya sobrevivido. Si queda uno, el build ABORTA nombrando archivo y linea.
     Falla CERRADO, porque el error se paga publicando en internet: una lista de
     sustituciones que nadie actualiza deja pasar al cliente siguiente, y ese es
     exactamente el fallo que trajo este archivo.

Anadir un cliente: se agrega a SUSTITUCIONES. Si no esta, el build se detiene
antes de publicar en vez de filtrarlo en silencio.

Uso:  python sanitizar.py <carpeta_de_references>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Nombre propio -> como se llama en publico. La categoria se conserva porque es
# lo que hace util al ejemplo: "una serie de sketches" ensena; "[REDACTADO]" no.
SUSTITUCIONES = {
    # clientes y marcas
    "Heineken MX": "un cliente de bebidas",
    "Heineken": "un cliente de bebidas",
    "FMF": "una federacion deportiva",
    "Foliatti": "un cliente de entretenimiento",
    "OXXO": "una cadena de tiendas",
    "LALA": "un cliente de alimentos",
    "ALEN": "un cliente industrial",
    "Ragasa": "un cliente de alimentos",
    "Sigma": "un cliente de alimentos",
    "Colek Academy": "un curso interno",
    "Colek Studios": "el estudio",
    "Colek": "el estudio",
    # series y proyectos
    "Tlachi": "una mascota 3D",
    "OBO": "una serie de sketches",
    "Calculus Conquistadores": "un curso de ventas",
    "Conquistando al 100": "un teaser de curso",
    "Champs en Accion": "una serie de capacitacion",
    "Expertos del Frio": "una serie de capacitacion",
    "Presenta como un Pro": "un curso interno",
    # personajes
    "Melvin": "un personaje recurrente",
    "Dona Fortuna": "una personaje recurrente",
    "Doña Fortuna": "una personaje recurrente",
    "Ricky": "un personaje recurrente",
    "Julissa": "una conductora",
    "Alicia": "una conductora",
    "Yeti": "un personaje recurrente",
    "Juli Planta": "un avatar",
    # personas
    "Adrian": "el director",
    "Adrián": "el director",
}

# Patrones que se limpian por FORMA, no por nombre: cubren lo que la lista no
# alcanza a enumerar (una ruta de un cliente nuevo, un costo cualquiera).
PATRONES = [
    # Rutas de Windows. Los segmentos PUEDEN llevar espacios ("G:\Mi unidad\...",
    # "Unidades compartidas"), asi que no basta con cortar en el primer espacio:
    # se consumen segmentos mientras sigan terminando en '\', y el ultimo tramo ya
    # va sin espacios. Sin esto, "G:\Unidades compartidas\CLIENTE\" se limpiaba
    # solo hasta "G:\Unidades" y el nombre del cliente sobrevivia.
    (re.compile(r"[A-Z]:\\{1,2}(?:[^\\\n`'\"|)]*\\{1,2})*[^\\\n\s`'\"|)]*"), "<ruta interna>"),
    # Rutas SIN letra de unidad: `TEAM INTERNO\TORNEOS IA\...`, `skills\media-prompting\...`.
    # Se exigen al menos dos separadores para no confundirlas con un escape suelto de
    # codigo. Sobrevivio una en la primera corrida del build sanitizado (2026-09-05).
    (re.compile(r"(?<![\w:])[\w][\w .-]*\\{1,2}[\w][\w .-]*\\{1,2}(?:[\w .-]*\\{0,2})*"),
     "<ruta interna>"),
    (re.compile(r"\$\s?\d+[.,]\d+(\s*(USD|por segundo|/s))?"), "<costo interno>"),
    (re.compile(r"\$\d+(?![\d.,])"), "<costo interno>"),
]

# Lo que NUNCA puede aparecer en la salida, se haya sustituido o no.
# Es el gate: si sobrevive, el build no publica.
def terminos_prohibidos() -> list[str]:
    return sorted({t for t in SUSTITUCIONES} | {"Unidades compartidas", "Mi unidad", "colekstudios"},
                  key=len, reverse=True)


def sanitizar_texto(texto: str) -> str:
    for nombre, publico in sorted(SUSTITUCIONES.items(), key=lambda kv: -len(kv[0])):
        texto = re.sub(rf"\b{re.escape(nombre)}\b", publico, texto, flags=re.IGNORECASE)
    for patron, reemplazo in PATRONES:
        texto = patron.sub(reemplazo, texto)
    return texto


def revisar(texto: str) -> list[tuple[int, str, str]]:
    """Terminos prohibidos que sobrevivieron. (linea, termino, contexto)."""
    hallazgos = []
    for n, linea in enumerate(texto.split("\n"), 1):
        for t in terminos_prohibidos():
            if re.search(rf"\b{re.escape(t)}\b", linea, flags=re.IGNORECASE):
                hallazgos.append((n, t, linea.strip()[:100]))
                break
    return hallazgos


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip())
        return 1
    carpeta = Path(argv[1])
    if not carpeta.is_dir():
        print(f"ERROR: no existe la carpeta {carpeta}", file=sys.stderr)
        return 1

    problemas = []
    for f in sorted(carpeta.glob("*.md")):
        original = f.read_text(encoding="utf-8")
        limpio = sanitizar_texto(original)
        f.write_text(limpio, encoding="utf-8")
        cambios = sum(1 for a, b in zip(original.split("\n"), limpio.split("\n")) if a != b)
        restos = revisar(limpio)
        print(f"  {f.name:28} {cambios:3} lineas limpiadas" +
              (f"  <-- {len(restos)} RESTOS" if restos else ""))
        for n, termino, contexto in restos:
            problemas.append(f"{f.name}:{n}  '{termino}'  ->  {contexto}")

    if problemas:
        print("\nBUILD DETENIDO: quedaron terminos internos tras sanitizar.", file=sys.stderr)
        print("El repo destino es PUBLICO, asi que esto no se publica.\n", file=sys.stderr)
        for p in problemas:
            print(f"  {p}", file=sys.stderr)
        print("\nArreglo: agregar el termino a SUSTITUCIONES en sanitizar.py, o quitarlo de la fuente.",
              file=sys.stderr)
        return 2
    print("\nSanitizado limpio: ningun termino interno sobrevive.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
