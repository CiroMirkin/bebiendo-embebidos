"""Esquemáticos de la parte Electrónica (lecciones e-1 a e-4).

Uso: uv run --no-project --with schemdraw --with matplotlib python docs/electronica/diagramas.py
Escribe los SVG en public/images/.
"""
import os

import schemdraw
from schemdraw import elements as elm

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SALIDA = os.path.join(RAIZ, "public", "images")

schemdraw.config(fontsize=11, unit=2.5)
schemdraw.use("svg")


def ruta(nombre):
    return os.path.join(SALIDA, nombre)


def buzzer_npn():
    """e-1: NPN del lado bajo para un buzzer de 12 V desde el GPIO 2 del controlador."""
    with schemdraw.Drawing(file=ruta("buzzer-npn.svg"), show=False):
        elm.Dot(open=True).label("+12 V", "top")
        elm.Line().down(0.5)
        elm.RBox().down().label("buzzer\n12 V, 30 mA", loc="bot")
        elm.Line().down(0.5)
        q = elm.BjtNpn(circle=True).right().anchor("collector").label("Q1\nBC547", "right")
        elm.Line().at(q.emitter).down(0.5)
        elm.Ground()
        elm.Line().at(q.base).left(1.5)
        b = elm.Dot()
        elm.Resistor().left().label("R1\n680 Ω")
        elm.Dot(open=True).label("GPIO 2", "left")
        elm.Resistor().at(b.center).down().label("R2\n47 kΩ", loc="top")
        elm.Ground()


def llave_sensor_nodo():
    """e-2: P-MOSFET del lado alto manejado directo por el GPIO 25 del nodo."""
    with schemdraw.Drawing(file=ruta("llave-sensor-nodo.svg"), show=False):
        elm.Dot(open=True).label("3,3 V del\nregulador", "left")
        elm.Line().right(1)
        a = elm.Dot()
        elm.Line().down(1)
        q = elm.PFet().right().anchor("source").label("Q1\nAO3401", "left")
        elm.Line().at(a.center).right(3)
        elm.Resistor().down().toy(q.gate).label("R1\n100 kΩ", loc="top")
        g = elm.Dot()
        elm.Line().at(q.gate).to(g.center)
        elm.Line().at(g.center).right(0.5)
        elm.Resistor().right().label("R2\n10 kΩ", loc="bot")
        elm.Dot(open=True).label("GPIO 25\n(bajo = prendido)", "right")
        elm.Capacitor().at(g.center).down().label("C1\n47 nF", loc="bot")
        c = elm.Dot()
        elm.Line().at(q.drain).down().toy(c.center)
        s = elm.Dot()
        elm.Line().at(s.center).to(c.center)
        elm.Line().at(s.center).down(0.5)
        elm.RBox().down().label("sensor\nde suelo\n5 mA", loc="top")
        elm.Ground()


def llave_5v():
    """e-2 y e-4: P-MOSFET sobre 5 V con un NPN que invierte y adapta el nivel."""
    with schemdraw.Drawing(file=ruta("llave-5v.svg"), show=False):
        elm.Dot(open=True).label("5 V", "left")
        elm.Fuse().right().label("F1\n0,25 A")
        a = elm.Dot()
        elm.Line().down(1)
        q = elm.PFet().right().anchor("source").label("Q1\nAO3401", "left")
        elm.Line().at(a.center).right(3)
        elm.Resistor().down().toy(q.gate).label("R1\n10 kΩ", loc="top")
        g = elm.Dot()
        elm.Line().at(q.gate).to(g.center)
        elm.Line().at(g.center).down(0.75)
        n = elm.BjtNpn(circle=True).right().reverse().anchor("collector").label("Q2\nBC547", "left")
        elm.Line().at(n.emitter).down(0.5)
        elm.Ground()
        elm.Line().at(n.base).right(1)
        b = elm.Dot()
        elm.Resistor().right().label("R2\n4,7 kΩ")
        elm.Dot(open=True).label("GPIO\n(alto = prendido)", "right")
        elm.Resistor().at(b.center).down().label("R3\n47 kΩ", loc="bot")
        elm.Ground()
        elm.Line().at(q.drain).down(1.5)
        v = elm.Dot()
        elm.Line().down(2)
        elm.Dot(open=True).label("VBUS de\nla carga", "bottom")
        elm.Line().at(v.center).left(1.5)
        elm.Capacitor(polar=True).down().label("C1\n100 µF", loc="top")
        elm.Ground()


def alimentacion_controlador():
    """e-3: entrada de 12 V del controlador, con fusible, polaridad, desacople y regulador."""
    with schemdraw.Drawing(file=ruta("alimentacion-controlador.svg"), show=False):
        elm.Dot(open=True).label("+12 V\nfuente 5 A", "left")
        elm.Fuse().right().label("F1\n4 A lento")
        elm.Diode().right().label("D1 Schottky\n5 A")
        a = elm.Dot()
        elm.Line().right(2.5)
        b = elm.Dot()
        elm.Line().right(1.5)
        c = elm.Dot()
        elm.Line().right(1)
        reg = elm.Ic(pins=[elm.IcPin(name="", anchorname="IN", side="left"),
                           elm.IcPin(name="", anchorname="OUT", side="right"),
                           elm.IcPin(name="", anchorname="GND", side="bot")],
                     size=(2.5, 1.5), label="step-down\n12 V a 5 V").anchor("IN")
        elm.Line().at(reg.GND).down(0.5)
        elm.Ground()
        elm.Line().at(reg.OUT).right(1)
        o = elm.Dot()
        elm.Line().right(1)
        elm.Dot(open=True).label("5 V al\nESP32-S3", "right")
        elm.Capacitor(polar=True).at(a.center).down().label("470 µF", loc="top")
        elm.Ground()
        elm.Capacitor().at(b.center).down().label("100 nF", loc="top")
        elm.Ground()
        elm.Line().at(c.center).up(1.5)
        elm.Dot(open=True).label("12 V a bomba,\nventilador y cortina", "right")
        elm.Capacitor(polar=True).at(o.center).down().label("100 µF", loc="bot")
        elm.Ground()


def usb_host_taller():
    """e-4: conexionado del USB-A del control de acceso del taller."""
    with schemdraw.Drawing(file=ruta("usb-host-taller.svg"), show=False):
        esp = elm.Ic(pins=[elm.IcPin(name="GND", side="right", slot="1/4"),
                           elm.IcPin(name="GPIO 5", side="right", slot="2/4"),
                           elm.IcPin(name="GPIO 20 (D+)", side="right", slot="3/4"),
                           elm.IcPin(name="GPIO 19 (D-)", side="right", slot="4/4"),
                           elm.IcPin(name="GPIO 6", side="left", slot="2/4"),
                           elm.IcPin(name="5V", side="left", slot="3/4")],
                     size=(6, 5), label="ESP32-S3\nDevKitC-1", lblofst=0, lblloc="bot")
        usb = elm.Ic(pins=[elm.IcPin(name="GND", side="left", slot="1/4"),
                           elm.IcPin(name="VBUS", side="left", slot="2/4"),
                           elm.IcPin(name="D+", side="left", slot="3/4"),
                           elm.IcPin(name="D-", side="left", slot="4/4")],
                     size=(2.5, 5), label="USB-A\nhembra").at((esp["GND"][0] + 8, esp["GND"][1])).anchor("GND")
        elm.Wire("-").at(esp["GPIO 19 (D-)"]).to(usb["D-"])
        elm.Wire("-").at(esp["GPIO 20 (D+)"]).to(usb["D+"])
        elm.Wire("-").at(esp["GND"]).to(usb["GND"])
        elm.Line().at(esp["GPIO 5"]).right(2)
        llave = elm.Ic(pins=[elm.IcPin(name="", anchorname="ent", side="left"),
                             elm.IcPin(name="", anchorname="sal", side="right")],
                       size=(3, 1), label="llave de 5 V").anchor("ent")
        elm.Wire("-").at(llave.sal).to(usb["VBUS"])
        elm.Line().at(esp["GPIO 6"]).left(1.5)
        elm.Dot(open=True).label("relé de la\ncerradura", "left")
        elm.Line().at(esp["5V"]).left(1.5)
        elm.Dot(open=True).label("5 V de la\nfuente", "left")


if __name__ == "__main__":
    buzzer_npn()
    llave_sensor_nodo()
    llave_5v()
    alimentacion_controlador()
    usb_host_taller()
