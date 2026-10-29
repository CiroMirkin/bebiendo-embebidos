import { getCollection } from 'astro:content';

export type QuizOption = {
  text: string;
  correct: boolean;
  explanation: string;
};

export type Quiz = {
  prompt: string;
  options: QuizOption[];
};

type Level = 'ESTUDIAR' | 'CONOCER';

export type Concept = {
  id: string;
  slug: string;
  partSlug: string;
  title: string;
  level: Level;
  relacionado?: string;
  descripcion?: string;
  quizzes: Quiz[];
  cuerpo: string;
};

const cargar = async (): Promise<Concept[]> => {
  const entradas = await getCollection('conceptos');
  const concepts = entradas.map(({ id: slug, data, body }): Concept => ({
    id: data.id,
    slug,
    partSlug: data.parte,
    title: data.titulo,
    level: data.nivel,
    ...(data.relacionado ? { relacionado: data.relacionado } : {}),
    ...(data.descripcion ? { descripcion: data.descripcion } : {}),
    quizzes: data.quiz,
    cuerpo: body ?? '',
  }));
  const slugs = new Set(concepts.map((c) => c.slug));
  for (const c of concepts) {
    if (c.relacionado && !slugs.has(c.relacionado)) {
      throw new Error(`${c.slug}.md: "relacionado" apunta a "${c.relacionado}", que no existe`);
    }
  }
  return concepts;
};

let cache: Promise<Concept[]> | undefined;

export const getAllConcepts = (): Promise<Concept[]> => (cache ??= cargar());

export const getConceptBySlug = async (slug: string): Promise<Concept | undefined> =>
  (await getAllConcepts()).find((c) => c.slug === slug);

export const getConceptsByPart = async (partSlug: string): Promise<Concept[]> =>
  (await getAllConcepts())
    .filter((c) => c.partSlug === partSlug)
    .sort((a, b) => a.id.localeCompare(b.id, undefined, { numeric: true }));
