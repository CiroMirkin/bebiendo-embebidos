"""Pruebas de verificar-diagramas.py: lo corren igual que el autor, sobre una copia del repo mínima.

Uso: python3 tools/test_verificar_diagramas.py
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verificar-diagramas.py")
SVG_BIEN = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50">
<title>Bus I2C</title>
<desc>El OLED y el SHT31 comparten SDA y SCL.</desc>
<rect width="10" height="10"/>
</svg>"""


class VerificarDiagramas(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.raiz = carpeta.name
        os.makedirs(os.path.join(self.raiz, "tools"))
        os.makedirs(os.path.join(self.raiz, "src", "content", "conceptos"))
        # El script ubica el repo a partir de su propia ruta, así que la copia revisa la carpeta temporal.
        shutil.copy(SCRIPT, os.path.join(self.raiz, "tools"))

    def correr(self, *prefijos):
        return subprocess.run(
            [sys.executable, os.path.join(self.raiz, "tools", "verificar-diagramas.py"), *prefijos],
            capture_output=True,
            text=True,
        )

    def leccion(self, slug, cuerpo="Texto de la lección."):
        ruta = os.path.join(self.raiz, "src", "content", "conceptos", f"{slug}.md")
        with open(ruta, "w", encoding="utf8") as archivo:
            archivo.write(f"---\ntitulo: Prueba\n---\n\n{cuerpo}\n")

    def diagrama(self, nombre, svg=SVG_BIEN, fuente=True):
        """Deja un SVG en la carpeta pública y, si corresponde, su HTML fuente."""
        svgs = os.path.join(self.raiz, "public", "images", "diagramas")
        fuentes = os.path.join(self.raiz, "docs", "diagramas")
        os.makedirs(svgs, exist_ok=True)
        os.makedirs(fuentes, exist_ok=True)
        with open(os.path.join(svgs, f"{nombre}.svg"), "w", encoding="utf8") as archivo:
            archivo.write(svg)
        if fuente:
            with open(os.path.join(fuentes, f"{nombre}.html"), "w", encoding="utf8") as archivo:
                archivo.write("<!doctype html>")

    def test_acepta_que_aun_no_haya_diagramas(self):
        self.leccion("0-1")
        resultado = self.correr()
        self.assertEqual(resultado.returncode, 0, resultado.stdout + resultado.stderr)

    def test_marca_la_imagen_cuyo_archivo_no_existe(self):
        self.leccion("0-7", "![Bus I2C](/images/diagramas/0-7-bus.svg)")
        resultado = self.correr()
        self.assertEqual(resultado.returncode, 1)
        self.assertIn("0-7", resultado.stdout)
        self.assertIn("0-7-bus.svg", resultado.stdout)

    def test_acepta_un_diagrama_completo(self):
        self.diagrama("0-7-bus")
        self.leccion("0-7", '![El OLED y el SHT31 comparten el bus](/images/diagramas/0-7-bus.svg "Bus I2C")')
        resultado = self.correr()
        self.assertEqual(resultado.returncode, 0, resultado.stdout)

    def test_marca_el_texto_alternativo_vacio(self):
        for alt in ("", "   "):
            with self.subTest(alt=alt):
                self.diagrama("0-7-bus")
                self.leccion("0-7", f"![{alt}](/images/diagramas/0-7-bus.svg)")
                resultado = self.correr()
                self.assertEqual(resultado.returncode, 1)
                self.assertIn("texto alternativo", resultado.stdout)

    def test_marca_el_svg_sin_titulo_descripcion_o_viewbox(self):
        casos = {
            "title": SVG_BIEN.replace("<title>Bus I2C</title>", ""),
            "desc": SVG_BIEN.replace("<desc>El OLED y el SHT31 comparten SDA y SCL.</desc>", ""),
            "viewBox": SVG_BIEN.replace(' viewBox="0 0 100 50"', ""),
            "title vacío": SVG_BIEN.replace("Bus I2C", ""),
        }
        self.leccion("0-7", "![Bus](/images/diagramas/0-7-bus.svg)")
        for caso, svg in casos.items():
            with self.subTest(caso=caso):
                self.diagrama("0-7-bus", svg)
                resultado = self.correr()
                self.assertEqual(resultado.returncode, 1)
                self.assertIn("0-7-bus.svg", resultado.stdout)
                self.assertIn(caso.split()[0], resultado.stdout)

    def test_marca_lo_que_se_carga_de_afuera(self):
        casos = {
            "@import": "<style>@import url('fuentes.css');</style>",
            "http": '<image href="http://ejemplo.com/a.png"/>',
            "https": "<style>text { src: url(https://ejemplo.com/a.woff2); }</style>",
            "sin protocolo": '<image href="//ejemplo.com/a.png"/>',
        }
        self.leccion("0-7", "![Bus](/images/diagramas/0-7-bus.svg)")
        for caso, agregado in casos.items():
            with self.subTest(caso=caso):
                self.diagrama("0-7-bus", SVG_BIEN.replace("<rect", agregado + "<rect"))
                resultado = self.correr()
                self.assertEqual(resultado.returncode, 1, caso)
                self.assertIn("0-7-bus.svg", resultado.stdout)

    def test_marca_el_svg_que_ninguna_leccion_usa(self):
        self.leccion("0-7")
        self.diagrama("0-7-bus")
        resultado = self.correr()
        self.assertEqual(resultado.returncode, 1)
        self.assertIn("0-7-bus.svg", resultado.stdout)
        self.assertIn("ninguna lección", resultado.stdout)

    def test_marca_el_svg_sin_html_fuente(self):
        self.leccion("0-7", "![Bus](/images/diagramas/0-7-bus.svg)")
        self.diagrama("0-7-bus", fuente=False)
        resultado = self.correr()
        self.assertEqual(resultado.returncode, 1)
        self.assertIn("0-7-bus.html", resultado.stdout)

    def test_los_prefijos_dejan_afuera_los_problemas_de_otras_lecciones(self):
        self.leccion("0-7", "![Bus](/images/diagramas/0-7-bus.svg)")
        self.diagrama("0-7-bus")
        self.leccion("2-2", "![](/images/diagramas/2-2-falta.svg)")
        self.diagrama("2-2-huerfano", "<svg/>", fuente=False)
        self.assertEqual(self.correr("0-").returncode, 0)
        self.assertEqual(self.correr("0-", "2-").returncode, 1)

    def test_con_prefijos_un_svg_compartido_no_queda_huerfano(self):
        self.leccion("4-1", "![Modelo](/images/diagramas/4-1-modelo-datos.svg)")
        self.leccion("5-1", "![Modelo](/images/diagramas/4-1-modelo-datos.svg)")
        self.diagrama("4-1-modelo-datos")
        for prefijo in ("4-", "5-"):
            with self.subTest(prefijo=prefijo):
                self.assertEqual(self.correr(prefijo).returncode, 0)

    def test_con_prefijos_revisa_el_svg_de_otra_leccion_que_se_usa_en_la_filtrada(self):
        self.leccion("5-1", "![Modelo](/images/diagramas/4-1-modelo-datos.svg)")
        self.diagrama("4-1-modelo-datos", "<svg/>")
        resultado = self.correr("5-")
        self.assertEqual(resultado.returncode, 1)
        self.assertIn("4-1-modelo-datos.svg", resultado.stdout)


if __name__ == "__main__":
    unittest.main()
