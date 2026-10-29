import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { getAllPartSlugs } from './content/parts';

const opcion = z.object({
  text: z.string(),
  correct: z.boolean(),
  explanation: z.string(),
});

// Una lección por concepto: un .md en content/conceptos, con el quiz en el frontmatter.
const conceptos = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/conceptos' }),
  schema: z.object({
    id: z.string(),
    parte: z.enum(getAllPartSlugs() as [string, ...string[]]),
    titulo: z.string(),
    nivel: z.enum(['ESTUDIAR', 'CONOCER']),
    relacionado: z.string().optional(),
    // Resumen para buscadores; si falta, se usa el primer párrafo de la lección.
    descripcion: z.string().optional(),
    quiz: z.array(z.object({ prompt: z.string(), options: z.array(opcion) })).default([]),
  }),
});

export const collections = { conceptos };
