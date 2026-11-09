"""Revisa que el sitio generado por `npm run build` tenga todas las páginas y su SEO.

Uso:
  npm run build && python3 tools/verificar-build.py
  npm run verificar                                  # lo mismo, en un paso

Lee las lecciones y las partes para saber qué páginas tienen que existir, y en
dist/ comprueba URLs, <title>, meta description, canónica, Open Graph, JSON-LD,
sitemap, robots.txt, quiz y bloques de código en el HTML, que las partes no
carguen JavaScript, y que los enlaces internos no estén rotos.
Sale con código 1 si algo falla. Necesita PyYAML (pip install pyyaml).
"""

import glob
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LECCIONES = os.path.join(RAIZ, "src", "content", "conceptos")
PARTES = os.path.join(RAIZ, "src", "content", "parts.ts")
CONFIG = os.path.join(RAIZ, "astro.config.mjs")
DIST = os.path.join(RAIZ, "dist")
LARGO_DESCRIPCION = 160
OG_OBLIGATORIOS = ["og:type", "og:site_name", "og:locale", "og:title", "og:description", "og:url", "og:image"]


class Pagina(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.titulo = ""
        self.meta = {}
        self.canonica = None
        self.json_ld = []
        self.enlaces = []
        self.scripts = []
        self.islas = 0
        self.texto = []
        self._en = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._en = "title"
        elif tag == "meta":
            clave = a.get("property") or a.get("name")
            if clave:
                self.meta[clave] = a.get("content") or ""
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonica = a.get("href")
        elif tag == "script":
            if a.get("type") == "application/ld+json":
                self._en = "json"
                self.json_ld.append("")
            elif a.get("src"):
                self.scripts.append(a["src"])
            else:
                self._en = "script"
        elif tag == "style":
            self._en = "style"
        elif tag == "a" and a.get("href"):
            self.enlaces.append(a["href"])
        elif tag == "astro-island":
            self.islas += 1

    def handle_endtag(self, tag):
        if tag in ("title", "script", "style"):
            self._en = None

    def handle_data(self, data):
        if self._en == "title":
            self.titulo += data
        elif self._en == "json":
            self.json_ld[-1] += data
        elif self._en is None:
            self.texto.append(data)


def normalizar(texto):
    return re.sub(r"\s+", " ", html.unescape(texto)).strip()


def leer_sitio():
    sitio = re.search(r"site:\s*'([^']+)'", open(CONFIG, encoding="utf8").read())
    return sitio.group(1).rstrip("/")


def leer_lecciones():
    lecciones = {}
    for ruta in sorted(glob.glob(os.path.join(LECCIONES, "*.md"))):
        frontmatter, cuerpo = open(ruta, encoding="utf8").read()[4:].split("\n---\n", 1)
        lecciones[os.path.basename(ruta)[:-3]] = (yaml.safe_load(frontmatter), cuerpo)
    return lecciones


def archivo_de(url):
    """La ruta en dist/ que sirve una URL interna, o None si no existe."""
    ruta = url.split("#")[0].split("?")[0]
    candidatos = ["index.html"] if ruta == "/" else [ruta.lstrip("/") + ".html", ruta.lstrip("/")]
    for c in candidatos:
        if os.path.isfile(os.path.join(DIST, c)):
            return c
    return None


def revisar():
    fallas = []
    sitio = leer_sitio()
    lecciones = leer_lecciones()
    partes = re.findall(r"^\s+slug: '([^']+)'", open(PARTES, encoding="utf8").read(), re.M)
    urls = ["/"] + [f"/partes/{p}" for p in partes] + [f"/conceptos/{s}" for s in lecciones]

    titulos, descripciones = {}, {}
    for url in urls + ["/404"]:
        archivo = archivo_de(url)
        if not archivo:
            fallas.append(f"{url}: no está en el build")
            continue
        p = Pagina()
        p.feed(open(os.path.join(DIST, archivo), encoding="utf8").read())
        titulo = normalizar(p.titulo)
        descripcion = p.meta.get("description", "")

        if p.lang != "es":
            fallas.append(f"{url}: <html lang> es {p.lang!r}")
        if not titulo or "`" in titulo:
            fallas.append(f"{url}: <title> vacío o con comillas invertidas: {titulo!r}")
        if not descripcion or len(descripcion) > LARGO_DESCRIPCION:
            fallas.append(f"{url}: meta description vacía o de más de {LARGO_DESCRIPCION} ({len(descripcion)})")
        for clave in OG_OBLIGATORIOS:
            if not p.meta.get(clave):
                fallas.append(f"{url}: falta {clave}")
        for href in p.enlaces:
            if href.startswith("/") and not href.startswith("//") and not archivo_de(href):
                fallas.append(f"{url}: enlace roto a {href}")
        datos = []
        for bloque in p.json_ld:
            try:
                datos.append(json.loads(bloque))
            except json.JSONDecodeError as e:
                fallas.append(f"{url}: JSON-LD inválido ({e})")
        tipos = {d.get("@type") for d in datos}

        if url == "/404":
            continue
        if p.canonica != sitio + url and not (url == "/" and p.canonica == sitio + "/"):
            fallas.append(f"{url}: canónica {p.canonica!r}")
        if p.meta.get("og:url") != p.canonica:
            fallas.append(f"{url}: og:url distinta de la canónica")
        titulos.setdefault(titulo, []).append(url)
        descripciones.setdefault(descripcion, []).append(url)

        if url.startswith("/partes/"):
            if "BreadcrumbList" not in tipos:
                fallas.append(f"{url}: falta el JSON-LD BreadcrumbList")
            if p.islas or p.scripts:
                fallas.append(f"{url}: carga JavaScript y no tiene quiz")
        if url.startswith("/conceptos/"):
            fm, cuerpo = lecciones[url.rsplit("/", 1)[1]]
            for tipo in ("LearningResource", "BreadcrumbList"):
                if tipo not in tipos:
                    fallas.append(f"{url}: falta el JSON-LD {tipo}")
            # Sin espacios: el HTML parte el texto en nodos (`codigo`, **negrita**) y los espacios no coinciden.
            texto = re.sub(r"\s+", "", html.unescape("".join(p.texto)))
            quiz = fm.get("quiz") or []
            if quiz:
                inicio = re.sub(r"\s+|`|\*", "", quiz[0]["prompt"].split("\n")[0])[:40]
                if inicio not in texto:
                    fallas.append(f"{url}: la primera pregunta del quiz no está en el HTML")
                if p.islas != len(quiz):
                    fallas.append(f"{url}: {p.islas} islas de quiz para {len(quiz)} preguntas")
            html_crudo = open(os.path.join(DIST, archivo), encoding="utf8").read()
            if "```" in cuerpo and ('class="bloque-codigo"' not in html_crudo or 'class="shiki' not in html_crudo):
                fallas.append(f"{url}: tiene código y falta el bloque resaltado")

    for valor, paginas in [*titulos.items(), *descripciones.items()]:
        if len(paginas) > 1:
            fallas.append(f"repetido en {', '.join(paginas)}: {valor[:60]!r}")

    sitemap = os.path.join(DIST, "sitemap-0.xml")
    listadas = set(re.findall(r"<loc>([^<]+)</loc>", open(sitemap, encoding="utf8").read())) if os.path.isfile(sitemap) else set()
    esperadas = {sitio + u if u != "/" else sitio + "/" for u in urls}
    for u in sorted(esperadas - listadas):
        fallas.append(f"sitemap: falta {u}")
    for u in sorted(listadas - esperadas):
        fallas.append(f"sitemap: sobra {u}")
    robots = open(os.path.join(DIST, "robots.txt"), encoding="utf8").read()
    if f"Sitemap: {sitio}/sitemap-index.xml" not in robots:
        fallas.append("robots.txt: no declara el sitemap con el dominio de astro.config.mjs")

    for f in fallas:
        print(f)
    print(f"{len(fallas)} problemas en {len(urls) + 1} páginas")
    return len(fallas)


if __name__ == "__main__":
    sys.exit(1 if revisar() else 0)
