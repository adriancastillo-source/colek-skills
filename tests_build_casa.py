# -*- coding: utf-8 -*-
"""Prueba de casa de build.ps1 (escision fase 3, DISENO-RUTAS.md 4.2). Sin red.

Uso: python tests_build_casa.py

Lo que caza: una ruta fija olvidada. build.ps1 debe leer la fuente de
EXIO_CASA_ADRIAN\\skills y de ningun otro lado, y detenerse si la variable falta.
Corre build.ps1 con `powershell -File` (como una tarea agendada), desde una
carpeta fuera del repo, y escribe en una carpeta temporal (-Destino): los
skills\\ y zips\\ versionados del repo no se tocan, y se comprueba.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent
BUILD = REPO / "build.ps1"
SKILLS = ("media-prompting", "image-character-sheet")
MARCA = "JUGUETE-CASA-TEMPORAL"

fallos = []


def ok(cond, msg):
    if cond:
        print(f"  OK   {msg}")
    else:
        fallos.append(msg)
        print(f"  X    {msg}")


def huella_versionado() -> dict:
    """Hash de todo lo que build.ps1 reescribiria dentro del repo."""
    out = {}
    for sub in ("skills", "zips"):
        for f in sorted((REPO / sub).rglob("*")):
            if f.is_file():
                out[str(f.relative_to(REPO))] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out


def casa_de_juguete(raiz: Path) -> Path:
    for s in SKILLS:
        d = raiz / "skills" / s
        (d / "portable").mkdir(parents=True)
        (d / "references").mkdir(parents=True)
        (d / "portable" / "SKILL.md").write_text(
            f"---\nname: {s}\n---\n# {s} de juguete\n{MARCA}\n", encoding="utf-8")
        (d / "references" / "ficha-juguete.md").write_text(
            f"# Ficha de juguete\n{MARCA}\n", encoding="utf-8")
    return raiz


def correr(env_extra: dict, quitar: tuple, destino: Path, cwd: Path):
    env = {k: v for k, v in os.environ.items() if k not in quitar}
    env.update(env_extra)
    r = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(BUILD),
         "-Destino", str(destino)],
        cwd=str(cwd), env=env, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


antes = huella_versionado()

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    casa = casa_de_juguete(tmp / "casa")
    fuera = tmp / "cwd-fuera-del-repo"
    fuera.mkdir()

    print("1. con EXIO_CASA_ADRIAN en una casa temporal, lee AHI y no en G:")
    destino = tmp / "salida"
    rc, out = correr({"EXIO_CASA_ADRIAN": str(casa)}, (), destino, fuera)
    ok(rc == 0, f"build termina en 0 (rc={rc})")
    ok(str(casa / "skills") in out, "anuncia la fuente de la casa temporal")
    for s in SKILLS:
        skill = destino / "skills" / s / "SKILL.md"
        ok(skill.is_file() and MARCA in skill.read_text(encoding="utf-8"),
           f"{s}: SKILL.md viene de la casa de juguete")
        ficha = destino / "skills" / s / "references" / "ficha-juguete.md"
        ok(ficha.is_file(), f"{s}: la ficha de juguete viajo")
        z = destino / "zips" / f"{s}.zip"
        ok(z.is_file(), f"{s}: zip escrito en el destino temporal")
        if z.is_file():
            with zipfile.ZipFile(z) as zf:
                ok(f"{s}/SKILL.md" in zf.namelist(), f"{s}: zip con la carpeta en la raiz")
    if rc != 0:
        print(out)

    print("2. sin la variable, se detiene con el mensaje claro")
    rc, out = correr({}, ("EXIO_CASA_ADRIAN",), tmp / "salida-sin-var", fuera)
    ok(rc != 0, f"build sin variable falla (rc={rc})")
    ok("Falta EXIO_CASA_ADRIAN" in out, "el mensaje nombra la variable")
    ok(not (tmp / "salida-sin-var").exists(), "no escribio nada")

    print("3. con la variable apuntando a una carpeta que no existe, tambien se detiene")
    rc, out = correr({"EXIO_CASA_ADRIAN": str(tmp / "no-existe")}, (), tmp / "salida-mala", fuera)
    ok(rc != 0, f"build con casa inexistente falla (rc={rc})")
    ok("Falta EXIO_CASA_ADRIAN" in out, "el mensaje nombra la variable")

print("4. lo versionado del repo (skills\\, zips\\) quedo intacto")
ok(huella_versionado() == antes, "skills\\ y zips\\ del repo sin cambios")

if fallos:
    print(f"\n{len(fallos)} FALLO(S)")
    sys.exit(1)
print("\nTODO OK")
