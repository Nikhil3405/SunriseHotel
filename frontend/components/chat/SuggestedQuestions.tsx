type SuggestedQuestionsProps = {
  onSelect: (question: string) => void;
  disabled?: boolean;
};

const questions = [
  "What time is check-in?",
  "What amenities does the hotel have?",
  "Is breakfast included in the Deluxe Room?",
  "Do you have rooms for 3 guests?",
];

export default function SuggestedQuestions({
  onSelect,
  disabled = false,
}: SuggestedQuestionsProps) {
  return (
    <div className="grid gap-2 sm:grid-cols-2">
      {questions.map((question) => (
        <button
          key={question}
          type="button"
          disabled={disabled}
          onClick={() => onSelect(question)}
          className="rounded-xl border border-[#E7E5E4] bg-white px-4 py-3 text-left text-sm text-[#57534E] transition hover:border-[#FDBA74] hover:bg-[#FFF7ED] disabled:opacity-50"
        >
          {question}
        </button>
      ))}
    </div>
  );
}