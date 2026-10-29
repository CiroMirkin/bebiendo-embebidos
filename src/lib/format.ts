export const toSentenceCase = (input: string): string => {
  const lower = input.toLowerCase();
  return lower.charAt(0).toUpperCase() + lower.slice(1);
};

// Títulos con Markdown inline, sin las comillas invertidas, para <title> y los metadatos.
export const textoPlano = (texto: string) => texto.replace(/`/g, '');
