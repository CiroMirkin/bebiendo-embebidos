# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Astro (sitio estático), Tailwind 4, React solo para el quiz, marked y shiki para el Markdown de las lecciones. Se despliega como archivos estáticos (`vercel.json`).

## Users

Personas que ya saben programar en algún lenguaje y no saben C++. Aprenden Arduino y ESP32 y después backend, leyendo lecciones largas con código, a su ritmo y en sesiones de estudio. Fuente: `CONTEXT.md` y `README.md`. Estado: inferido del repositorio, sin entrevista (no hubo canal de respuesta en esta sesión).

## Product Purpose

Roadmap de estudio, sitio "Bebiendo Embebidos", para aprender a construir un sistema de equipos conectados de punta a punta: C++ para firmware, Arduino y ESP32, electrónica, conectividad y un backend en Node, Express y PostgreSQL para varias organizaciones. Casi todas las lecciones usan un mismo ejemplo, el control de un invernadero. Éxito: que quien lee entienda la lección, haga el ejercicio y compruebe lo aprendido con el quiz.

## Positioning

Un único hilo de ejemplo (el invernadero) atraviesa firmware, electrónica y backend, con código de los ejemplos compilado contra el core ESP32 (`tools/verificar-ejemplos.py`). El ejemplo es ficticio: nunca se usa el proyecto real del autor.

## Operating Context

- 12 partes (Base de C++, Parte 0 a 9 y Electrónica) y 81 lecciones en `/conceptos/<slug>`, tres niveles: ESTUDIAR, CONOCER y PROFUNDIZAR.
- Cada lección tiene idea central, por qué importa, paso a paso, ejemplos, errores comunes, ejercicio con pista y solución, quiz y resumen.
- Hay diagramas propios en SVG (con paleta y fuentes ya definidas; no se rehacen) y bloques de código resaltados con un tema shiki basado en Flexoki.
- Idioma: español rioplatense (voseo). Solo el quiz carga JavaScript.

## Capabilities and Constraints

- Sitio estático, una página por URL, sin cuentas ni progreso guardado (no confirmado que se quiera agregar).
- Terminología fija en `CONTEXT.md`.
- Se mantiene la paleta Flexoki y las fuentes de los diagramas.
- Sin decidir: dominio de producción (hoy provisorio), modo oscuro, búsqueda, marcado de lecciones leídas.

## Brand Commitments

- Nombre: Bebiendo Embebidos.
- Dirección pedida por el autor: sensación de cuaderno de estudio, cálido, tipo libro técnico, pensado para leer lecciones largas.
- Prosa sin rastros de IA (reglas de humanizer): sin rayas largas, sin "no es X sino Y", títulos en minúscula inicial.

## Evidence on Hand

Contenido real: `src/content/conceptos/*.md`, `src/content/parts.ts`, diagramas en `public/images`. No hay testimonios, métricas de uso, clientes ni logo más allá del favicon (`/images/favicon.png`); no inventarlos.

## Product Principles

- La lección larga manda: todo lo demás se subordina a leerla cómoda de principio a fin.
- El código es contenido de primera clase, no decoración.
- Lo que está en la página es lo que se verificó: ni promesas ni cifras sin respaldo.
- Una sola voz cálida y directa, de autor a lector.

## Accessibility & Inclusion

Contraste AA en texto (ya hay tonos sólidos para `muted` y `accent-strong`), `prefers-reduced-motion` respetado, enlace "saltar al contenido", foco visible. Sin otro estándar declarado.
