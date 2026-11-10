---
name: Bebiendo Embebidos
description: Sitio de lecciones largas sobre Arduino, ESP32 y backend, en papel crema con tinta casi negra y un acento naranja.
colors:
  canvas: "#fffcf0"
  surface: "#ffffff"
  code-bg: "#f2f0e5"
  ink: "#100f0f"
  accent: "#bc5215"
  accent-strong: "#9d4310"
  accent-2: "#ad8301"
  success: "#66800b"
  danger: "#af3029"
  muted: "#6f6e69"
  line: "#e6e4d9"
typography:
  display:
    fontFamily: "Inter Variable, Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: "2.25rem"
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Inter Variable, Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 650
    lineHeight: 1.25
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Inter Variable, Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.72
  label:
    fontFamily: "Inter Variable, Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 500
  code:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "0.875rem"
    lineHeight: 1.6
rounded:
  sm: "0.25rem"
  lg: "0.5rem"
  xl: "0.75rem"
  full: "999px"
spacing:
  gutter: "20px"
  gutter-sm: "24px"
  section: "3rem"
components:
  part-card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.xl}"
    padding: "20px"
  level-badge:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.accent-strong}"
    rounded: "{rounded.full}"
    padding: "2px 10px"
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.canvas}"
    rounded: "{rounded.lg}"
    padding: "10px 20px"
  code-block:
    backgroundColor: "{colors.code-bg}"
    rounded: "{rounded.xl}"
---

# Design System: Bebiendo Embebidos

## Overview

Papel crema, tinta casi negra y un único acento naranja. Es la paleta Flexoki (sin cambios, y con las fuentes de los diagramas, que no se rehacen). Hoy el sistema se lee como una plantilla de documentación en sans moderna: una sola familia (Inter), tarjetas redondeadas con borde fino, insignias en píldora y bloques de código en caja. Dirección buscada por el autor: cuaderno de estudio, cálido, tipo libro técnico, para leer lecciones largas. Esa dirección todavía no está en el código.

## Colors

Neutros cálidos (canvas, code-bg, line, muted) más un acento naranja. Amarillo, verde y rojo existen para el quiz y el resaltado de código, no para la interfaz. El acento sube a `accent-strong` cuando va como texto, por contraste. Los neutros de texto salen de `ink` con opacidad (`ink/80`, `ink/86`), lo que da grises tibios variables.

## Typography

Inter para todo (cargada desde Google Fonts), con `cv11` y `ss03`. Los números de lección (`0.1`) van en monoespaciada del sistema. Cuerpo de lección a 17px, interlínea 1.72, columna de 46rem. Títulos con tracking negativo y `text-wrap: balance`. No hay serif ni jerarquía de énfasis más allá del peso.

## Layout

Una columna de 4xl (56rem) centrada, gutter 20/24px. La lección ocupa 46rem a la izquierda de esa columna, así que a 1280px queda un hueco a la derecha. Inicio apila las 12 partes como tarjetas; la página de parte es una lista con filetes. Cabecera fija con nombre y un único enlace "Inicio".

## Elevation & Depth

Plano. Sin sombras: la jerarquía sale de bordes `line` y fondos `surface` sobre `canvas`. La cabecera usa `backdrop-blur`.

## Shapes

Radios de 0.75rem en tarjetas, bloques de código, detalles y diagramas; 0.5rem en botones y opciones del quiz; píldora completa en insignias.

## Components

- Tarjeta de parte: blanco, borde fino, título con prefijo mono ("Parte 0"), descripción en gris y la insignia de nivel arriba a la derecha. Hover cambia el borde.
- Insignia de nivel: píldora naranja tenue para ESTUDIAR, contorno gris para el resto. Se repite en inicio, parte, lección y cada fila de la lista.
- Bloque de código: caja con cabecera mono (lenguaje) y tema Flexoki de shiki sobre `code-bg`.
- Quiz: tarjeta sobre `code-bg`, etiqueta "Pregunta n de N" en píldora oscura, opciones como botones con borde; correcta en verde, incorrecta en rojo.
- Cita: caja con fondo naranja tenue y borde naranja.
- Enlaces de la lección: naranja fuerte subrayado.

## Do's and Don'ts

- Mantener Flexoki y las fuentes de los diagramas.
- Priorizar la lectura larga: medida, interlínea y ritmo vertical antes que ornamento.
- No inventar métricas, testimonios ni claims.
- Evitar rayas largas y estructuras de prosa de plantilla en los textos de la interfaz.
- No añadir más tarjetas con borde y radio: ya es el único gesto del sistema.
