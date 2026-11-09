# Bebiendo Embebidos

Sitio estático hecho con [Astro](https://astro.build) para aprender a construir un sistema de equipos conectados de punta a punta: C++ para firmware, Arduino y ESP32, arquitectura de firmware, conectividad, y un backend en Node, Express y PostgreSQL para varias organizaciones.

Todas las lecciones usan el mismo ejemplo: el control de un invernadero, con nodos sensores a batería (BLE, deep sleep), un controlador ESP32-S3 que maneja el riego y la ventilación, y un backend donde cada productor tiene sus invernaderos, equipos y usuarios con roles.

## Contenido

- 11 partes: la Base (C++), la Parte 0 (Arduino y ESP32) y las Partes 1 a 9.
- 74 lecciones (`/conceptos/<slug>`), de dos tipos:
  - ESTUDIAR: idea central, por qué te importa, paso a paso, tres o más ejemplos, errores comunes, un ejercicio con pista y solución, un quiz de cuatro preguntas y un resumen.
  - CONOCER: una versión más liviana, con cómo funciona, uno o dos ejemplos, cuándo conviene y cuándo no, y un quiz de dos preguntas.

## Cómo correrlo

Requiere Node.js 22.23 o más nuevo.

```bash
npm install
npm run dev        # http://localhost:4321
```

## Sitio estático

```bash
npm run build      # genera dist/
npm run preview    # sirve dist/ para verlo antes de publicar
npm run verificar  # build + tools/verificar-build.py
```

`dist/` tiene una página `.html` por URL (`/conceptos/0-1` es `conceptos/0-1.html`), el sitemap y el `robots.txt`. Se puede servir con cualquier hosting de archivos estáticos que sirva `x.html` en `/x`. Solo el quiz carga JavaScript.

El dominio de producción está en `site` de `astro.config.mjs` y en la línea `Sitemap:` de `public/robots.txt`. De ahí salen la canónica, el sitemap y Open Graph; hoy es un dominio provisorio.

## Estructura

```text
src/
  content.config.ts         la colección de lecciones y el esquema del frontmatter
  content/
    conceptos/<slug>.md     una lección por concepto (frontmatter con id, parte, título, nivel, relacionado, descripción y quiz)
    concepts.ts             lee la colección y expone las lecciones ordenadas por parte
    parts.ts                las partes del roadmap
  lib/
    markdown.ts             marked + shiki: Markdown a HTML con resaltado de código, y el resumen en texto plano
    seo.ts                  títulos, URLs públicas y JSON-LD
  layouts/
    Base.astro              <head> con title, description, canónica, Open Graph y JSON-LD
  components/
    quiz.tsx                quiz interactivo (isla de React, client:visible)
    InlineMd.astro          títulos con `código` en listas y navegación
    LevelBadge.astro        ESTUDIAR / CONOCER
  pages/
    index.astro             listado de las partes
    partes/[part].astro     conceptos de una parte
    conceptos/[slug].astro  una lección
    404.astro
tools/
  verificar-build.py        revisa que el build tenga todas las páginas, el SEO y los enlaces internos
  verificar-ejemplos.py     compila los ejemplos de C++ completos contra el core esp32
  verificar-quiz.py         revisa que la respuesta correcta no se note por ser la más larga
```

## Escribir una lección

Cada archivo empieza con un frontmatter en YAML:

```markdown
---
id: '2.3'
parte: parte-2
titulo: 'Título con `código` si hace falta'
nivel: ESTUDIAR
relacionado: 0-1
descripcion: 'Opcional: el resumen que muestran los buscadores, de 160 caracteres como máximo.'
quiz:
  - prompt: '¿Pregunta?'
    options:
      - text: 'Opción'
        correct: false
        explanation: 'Por qué no.'
---
```

El build falla si falta `id`, `parte`, `titulo` o `nivel`, si `nivel` no es ESTUDIAR o CONOCER, o si `parte` o `relacionado` apuntan a algo que no existe. Sin `descripcion`, se usa el primer párrafo de la lección.

El cuerpo es Markdown. Los bloques de código llevan el lenguaje y una etiqueta opcional (` ```cpp sensor.ino `), los links internos son `/conceptos/<slug>`, y `<!-- quiz -->` marca dónde va el quiz.

En cada pregunta, la opción correcta no puede ser más larga que todas las incorrectas por más de 6 caracteres; `python tools/verificar-quiz.py` lo revisa.

## Verificar los ejemplos de C++

```bash
python tools/verificar-ejemplos.py b- 0- 1-
```

Usa el `arduino-cli` del Arduino IDE 2 con el core esp32 3.x. Solo compila los bloques que tienen `setup()` y `loop()`; los fragmentos que llaman funciones sin definir fallan con `was not declared`, y eso es esperable.
