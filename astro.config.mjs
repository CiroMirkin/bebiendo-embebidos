import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'astro/config';

export default defineConfig({
  // Dominio provisorio: cambiarlo por el de producción antes de publicar (canónica, sitemap y Open Graph salen de acá).
  site: 'https://arduino-roadmap.example',
  trailingSlash: 'never',
  // /conceptos/0-1 se genera como conceptos/0-1.html, que los hostings estáticos sirven sin extensión.
  build: { format: 'file' },
  integrations: [react(), sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});
