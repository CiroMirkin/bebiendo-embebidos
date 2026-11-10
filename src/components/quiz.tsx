import { useState } from 'react';

// Isla de Astro: el texto llega ya convertido a HTML en el build (Markdown inline y bloques de codigo).
export type QuizRenderizado = {
  promptHtml: string;
  options: {
    textHtml: string;
    correct: boolean;
    explanationHtml: string;
  }[];
};

type QuizProps = {
  quiz: QuizRenderizado;
  numero: number;
  total: number;
};

const LETRAS = ['A', 'B', 'C', 'D', 'E', 'F'];

export const QuizCard = ({ quiz, numero, total }: QuizProps) => {
  const [selected, setSelected] = useState<number | null>(null);

  const answered = selected !== null;

  // Sin respuesta, todo neutro. El color aparece solo en la letra y la nota de la elegida y de la correcta.
  const letraClasses = (index: number, correct: boolean) => {
    if (!answered) return 'border-ink/30 text-ink/70';
    if (correct) return 'border-success bg-success text-canvas';
    if (index === selected) return 'border-danger bg-danger text-canvas';
    return 'border-ink/20 text-ink/40';
  };

  return (
    <section className="my-6 border border-ink/25 bg-surface">
      <div className="serif border-b border-line px-4 pb-3 pt-4 sm:px-5">
        <p className="mb-2 font-sans text-xs text-muted">
          {total > 1 ? `Pregunta ${numero} de ${total}` : 'Pregunta'}. Elegí una opción para ver si es correcta.
        </p>
        <div
          className="leccion quiz-prompt font-medium text-ink"
          dangerouslySetInnerHTML={{ __html: quiz.promptHtml }}
        />
      </div>

      <ul>
        {quiz.options.map((option, index) => (
          <li key={index} className={index > 0 ? 'border-t border-line' : ''}>
            <button
              type="button"
              onClick={() => setSelected(index)}
              disabled={answered}
              className={`serif flex w-full gap-3 px-4 py-3 text-left text-base leading-relaxed transition-colors sm:px-5 ${
                answered ? 'cursor-default' : 'cursor-pointer hover:bg-ink/[0.04]'
              } ${answered && !option.correct && index !== selected ? 'text-ink/60' : 'text-ink'}`}
            >
              <span
                aria-hidden="true"
                className={`mt-0.5 flex size-6 shrink-0 items-center justify-center rounded-full border font-sans text-xs font-medium ${letraClasses(
                  index,
                  option.correct,
                )}`}
              >
                {LETRAS[index] ?? index + 1}
              </span>
              <span className="leccion min-w-0">
                <span dangerouslySetInnerHTML={{ __html: option.textHtml }} />
                {answered && (index === selected || option.correct) && (
                  <span
                    className={`mt-1.5 block text-[0.95rem] ${option.correct ? 'text-success' : 'text-danger'}`}
                  >
                    {index !== selected ? 'Esta es la correcta. ' : option.correct ? 'Correcto. ' : 'No es correcto. '}
                    <span className="text-ink/80" dangerouslySetInnerHTML={{ __html: option.explanationHtml }} />
                  </span>
                )}
              </span>
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
};
