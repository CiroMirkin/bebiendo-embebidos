"""Revisa los diagramas de las lecciones.

Uso:
  python3 tools/verificar-diagramas.py            # todas las lecciones
  python3 tools/verificar-diagramas.py b- 0-      # solo las que empiezan con b- o 0-

Para cada imagen de /images/diagramas/: que el archivo exista y que tenga texto
alternativo. Para cada SVG de la carpeta: que tenga <title>, <desc> y viewBox, que
no cargue nada de afuera, que alguna lección lo use y que tenga su HTML fuente en
docs/diagramas. Con prefijos entran los SVG con ese prefijo o usados en esas lecciones.
Sale con código 1 si encuentra algún problema.
"""

import glob
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LECCIONES = os.path.join(RAIZ, "src", "content", "conceptos")
DIAGRAMAS = os.path.join(RAIZ, "public", "images", "diagramas")
FUENTES = os.path.join(RAIZ, "docs", "diagramas")
IMAGEN = re.compile(r"!\[(.*?)\]\(\s*/images/diagramas/([^\s)]+)")
# Una URL absoluta o sin protocolo; los espacios de nombres de www.w3.org no se descargan.
URL_EXTERNA = re.compile(r"""(?:https?:|(?<=["'(]))//(?!www\.w3\.org/)[^\s"'<>)]+""", re.I)


def problemas_del_svg(texto):
    problemas = []
    for elemento in ("title", "desc"):
        if not re.search(rf"<{elemento}\b[^>]*>\s*[^<\s]", texto):
            problemas.append(f"no tiene <{elemento}> con texto")
    if not re.search(r"\bviewBox\s*=", texto):
        problemas.append("no tiene viewBox")
    if re.search(r"@import\b", texto, re.I):
        problemas.append("tiene @import")
    for url in URL_EXTERNA.findall(texto):
        problemas.append(f"carga algo de afuera: {url}")
    return problemas


def revisar(prefijos):
    entra = lambda nombre: not prefijos or nombre.startswith(tuple(prefijos))
    problemas = []
    usados = set()
    usados_en_filtradas = set()
    for ruta in sorted(glob.glob(os.path.join(LECCIONES, "*.md"))):
        slug = os.path.basename(ruta)[:-3]
        for alt, nombre in IMAGEN.findall(open(ruta, encoding="utf8").read()):
            usados.add(nombre)
            if not entra(slug):
                continue
            usados_en_filtradas.add(nombre)
            if not alt.strip():
                problemas.append(f"{slug}: {nombre} no tiene texto alternativo")
            if not os.path.isfile(os.path.join(DIAGRAMAS, nombre)):
                problemas.append(f"{slug}: no existe {nombre}")
    for ruta in sorted(glob.glob(os.path.join(DIAGRAMAS, "*.svg"))):
        nombre = os.path.basename(ruta)
        # El nombre empieza con el slug de su lección, pero otra lección lo puede compartir.
        if not entra(nombre) and nombre not in usados_en_filtradas:
            continue
        if nombre not in usados:
            problemas.append(f"{nombre}: ninguna lección lo usa")
        fuente = nombre[:-4] + ".html"
        if not os.path.isfile(os.path.join(FUENTES, fuente)):
            problemas.append(f"{nombre}: falta su fuente docs/diagramas/{fuente}")
        for problema in problemas_del_svg(open(ruta, encoding="utf8").read()):
            problemas.append(f"{nombre}: {problema}")
    for problema in problemas:
        print(problema)
    print(f"{len(problemas)} problemas")
    return len(problemas)


if __name__ == "__main__":
    sys.exit(1 if revisar(sys.argv[1:]) else 0)
