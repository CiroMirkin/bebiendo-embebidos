export const NOMBRE_SITIO = 'Bebiendo Embebidos';
const SUFIJO_TITULO = 'Bebiendo Embebidos';

export const DESCRIPCION_SITIO =
  'Lecciones en español de C++ para firmware, Arduino y ESP32, y del backend que recibe sus datos, con código probado y un quiz en cada una.';

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
