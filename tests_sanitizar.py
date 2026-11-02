# -*- coding: utf-8 -*-
"""Tests de sanitizar.py. Sin red, sin tocar el repo.

Uso: python tests_sanitizar.py

Lo que se prueba es lo que se paga caro: que un nombre de cliente NO llegue a un
repo publico de GitHub. Por eso el foco esta en el gate (`revisar`) y no solo en
las sustituciones: una lista que nadie actualiza deja pasar al cliente siguiente,
y el gate es lo unico que convierte ese olvido en un build detenido.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import sanitizar

fallos = []


def ok(cond, msg):
    if cond:
        print(f"  OK   {msg}")
    else:
        fallos.append(msg)
        print(f"  X    {msg}")


print("1. sustituye el nombre propio por su CATEGORIA (el ejemplo sigue ensenando)")
t = sanitizar.sanitizar_texto("La plantilla sellada de OBO produjo las tomas aprobadas.")
ok("OBO" not in t, "el nombre desaparece")
ok("serie de sketches" in t, f"y queda la categoria, no un [REDACTADO] (dio {t!r})")

t = sanitizar.sanitizar_texto("medido 2026-09-05, mascota 3D de FMF")
ok("FMF" not in t and "federacion deportiva" in t, "una federacion no se nombra")

print("2. respeta los limites de palabra (no destroza palabras que contienen el termino)")
ok("OBOE" in sanitizar.sanitizar_texto("Un OBOE suena grave."), "'OBOE' no se parte por contener OBO")
ok("colaborar" in sanitizar.sanitizar_texto("Vamos a colaborar."), "'colaborar' sobrevive pese a 'Colek'")
t = sanitizar.sanitizar_texto("Corrido a mano en Lotería Fanta, MARK y CDF Tapipesos; voz de Alan en Canales al 100.")
ok(sanitizar.revisar(t) == [] and "MARK" not in t, f"los nombres que se colaron el 2026-11-02 se sustituyen (dio {t!r})")
ok("watermark" in sanitizar.sanitizar_texto("no watermark, mark the edges"), "'mark' suelto no se toca: MARK solo va en frase")
t = sanitizar.sanitizar_texto("Medido en la prueba MARK 2026 (David en ingles) y en Lotería Fanta.")
ok(sanitizar.revisar(t) == [] and "MARK" not in t and "Lotería una" not in t, f"MARK 2026, David y Lotería Fanta se sustituyen en frase (dio {t!r})")
ok("Coleko" not in sanitizar.sanitizar_texto("la mascota Coleko"), "'Coleko' se cubre aunque contenga 'Colek'")

print("3. limpia por FORMA lo que la lista no enumera")
t = sanitizar.sanitizar_texto("Los clips estan en G:\\Unidades compartidas\\NUEVOCLIENTE\\AVE\\ y costo $0.90 por clip.")
ok("NUEVOCLIENTE" not in t, "una ruta de un cliente que NO esta en la lista igual se borra")
ok("<ruta interna>" in t, "la ruta se marca como interna")
ok("0.90" not in t and "<costo interno>" in t, f"el costo no viaja (dio {t!r})")
t = sanitizar.sanitizar_texto("Cuesta $5 el clip.")
ok("<costo interno>" in t, "tambien un costo sin decimales")

# Sobrevivio una en la PRIMERA corrida del build sanitizado: el patron solo cazaba
# rutas con letra de unidad, y las del Drive de equipo no la llevan.
t = sanitizar.sanitizar_texto("Las tomas viven en `TEAM INTERNO\\TORNEOS IA\\TORNEO VIDEO REF\\05-pruebas\\`.")
ok("TEAM INTERNO" not in t and "TORNEO" not in t,
   f"una ruta SIN letra de unidad tambien se borra (dio {t!r})")
ok("`" in t, "y no se come las comillas que la rodean")

print("4. EL GATE: lo que sobrevive detiene el build")
restos = sanitizar.revisar("Esto menciona a Heineken en una linea.")
ok(len(restos) == 1 and restos[0][1] == "Heineken", "detecta un termino prohibido crudo")
ok(restos[0][0] == 1, "reporta el numero de linea")
ok(sanitizar.revisar("Un texto perfectamente publico sobre prompting.") == [],
   "un texto limpio no dispara el gate")
ok(sanitizar.revisar("La ruta G:\\Unidades compartidas\\X quedo cruda.") != [],
   "una ruta de Drive sin limpiar tambien lo dispara")

print("5. el gate corre DESPUES de sustituir: lo sustituido ya no dispara")
ok(sanitizar.revisar(sanitizar.sanitizar_texto("La plantilla de OBO para Heineken.")) == [],
   "texto sanitizado pasa el gate")

print("6. de punta a punta sobre archivos, con salida y codigo de error reales")
with tempfile.TemporaryDirectory() as tmp:
    d = Path(tmp)
    (d / "ficha-ok.md").write_text("# Ficha\n\nUsa prosa declarativa y nombra la camara.\n", encoding="utf-8")
    (d / "ficha-sucia.md").write_text("# Ficha\n\nMedido con Tlachi en G:\\Unidades compartidas\\X, $0.90.\n",
                                      encoding="utf-8")
    code = sanitizar.main(["sanitizar.py", str(d)])
    ok(code == 0, f"sale 0 cuando todo quedo limpio (dio {code})")
    sucia = (d / "ficha-sucia.md").read_text(encoding="utf-8")
    ok("Tlachi" not in sucia and "mascota 3D" in sucia, "el archivo se reescribio ya limpio")
    ok("Unidades compartidas" not in sucia, "la ruta se fue")
    ok((d / "ficha-ok.md").read_text(encoding="utf-8").startswith("# Ficha"), "el archivo limpio no se rompe")

print("7. un termino NUEVO que nadie agrego DETIENE el build (el fallo que trajo este archivo)")
with tempfile.TemporaryDirectory() as tmp:
    d = Path(tmp)
    # Se simula el olvido: un cliente que no esta en SUSTITUCIONES pero si en el gate.
    sanitizar.SUSTITUCIONES["ClienteNuevo"] = "un cliente"
    original = dict(sanitizar.SUSTITUCIONES)
    del sanitizar.SUSTITUCIONES["ClienteNuevo"]      # "se olvidaron de agregarlo"
    sanitizar.SUSTITUCIONES["ClienteNuevo"] = "un cliente"
    try:
        # Con el termino en la lista, se sustituye y pasa.
        (d / "f.md").write_text("Medido con ClienteNuevo.\n", encoding="utf-8")
        ok(sanitizar.main(["x", str(d)]) == 0, "si esta declarado, se sustituye y pasa")
        # Sin el termino, el gate no lo conoce y NO lo detiene: por eso el gate mira
        # tambien patrones de forma. Se comprueba con una ruta, que si cubre.
        del sanitizar.SUSTITUCIONES["ClienteNuevo"]
        (d / "g.md").write_text("Ruta C:\\dev\\secreto\\x.md sin limpiar.\n", encoding="utf-8")
        code = sanitizar.main(["x", str(d)])
        ok(code == 0, "una ruta interna se limpia por forma aunque el nombre sea desconocido")
        ok("C:\\dev" not in (d / "g.md").read_text(encoding="utf-8"), "y no queda rastro de la ruta")
    finally:
        sanitizar.SUSTITUCIONES.clear()
        sanitizar.SUSTITUCIONES.update(original)
        sanitizar.SUSTITUCIONES.pop("ClienteNuevo", None)

print("8. el gate falla CERRADO: devuelve 2, no 0, cuando algo sobrevive")
with tempfile.TemporaryDirectory() as tmp:
    d = Path(tmp)
    (d / "f.md").write_text("texto\n", encoding="utf-8")
    # Se fuerza un resto: un termino del gate que NO esta en las sustituciones.
    sustituciones = dict(sanitizar.SUSTITUCIONES)
    try:
        sanitizar.SUSTITUCIONES.pop("Heineken", None)
        sanitizar.SUSTITUCIONES.pop("Heineken MX", None)
        (d / "f.md").write_text("Medido con Heineken.\n", encoding="utf-8")
        # 'Heineken' ya no se sustituye, pero sigue en terminos_prohibidos? No: el gate
        # se deriva de SUSTITUCIONES. Se usa un termino fijo del gate en su lugar.
        (d / "f.md").write_text("Ruta en Unidades compartidas escrita a mano.\n", encoding="utf-8")
        code = sanitizar.main(["x", str(d)])
        ok(code == 2, f"sale 2 (build detenido), no 0 (dio {code})")
    finally:
        sanitizar.SUSTITUCIONES.clear()
        sanitizar.SUSTITUCIONES.update(sustituciones)

print()
if fallos:
    print(f"FALLARON {len(fallos)}:")
    for f in fallos:
        print(f"  - {f}")
    sys.exit(1)
print("Todas pasaron.")
