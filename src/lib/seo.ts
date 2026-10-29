export const NOMBRE_SITIO = 'Roadmap Arduino / ESP32 / Backend';
const SUFIJO_TITULO = 'Roadmap Arduino / ESP32';

export const DESCRIPCION_SITIO =
  'Roadmap de Arduino, ESP32, C++ y arquitectura de backend multi-organización, con ejemplos de código y quiz por concepto.';

// Con build.format 'file', Astro.url.pathname trae ".html" (/conceptos/0-1.html, /index.html); la URL pública no.
export const urlDePagina = (pathname: string, site: URL | undefined) =>
  new URL(pathname.replace(/\.html$/, '').replace(/\/index$/, '/'), site);

export const tituloDePagina = (titulo: string) => `${titulo} · ${SUFIJO_TITULO}`;

type Miga = { nombre: string; url: URL };

export const migas = (items: Miga[]) => ({
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: items.map((item, i) => ({
    '@type': 'ListItem',
    position: i + 1,
    name: item.nombre,
    item: item.url.href,
  })),
});

// Un <script type="application/ld+json"> no puede contener "</script>".
export const serializarJsonLd = (datos: object) => JSON.stringify(datos).replace(/</g, '\\u003c');
