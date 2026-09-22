"use client";

import { FormEvent, useState } from "react";
import { ArrowUp } from "lucide-react";

type ChatInputProps = {
  onSend: (message: string) => void;
  disabled?: boolean;
};

export default function ChatInput({
  onSend,
  disabled = false,
}: ChatInputProps) {
  const [message, setMessage] = useState("");

  function handleSubmit(event: FormEvent) {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || disabled) {
      return;
    }

    onSend(trimmedMessage);
    setMessage("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-center gap-2 rounded-2xl border border-[#E7E5E4] bg-white p-2 shadow-sm"
    >
      <input
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        disabled={disabled}
        placeholder="Ask about Sunrise Hotel..."
        className="min-w-0 flex-1 bg-transparent px-3 py-2 text-sm text-[#292524] outline-none placeholder:text-[#A8A29E]"
      />

      <button
        type="submit"
        disabled={disabled || !message.trim()}
        className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#F97316] text-white transition hover:bg-[#EA580C] disabled:cursor-not-allowed disabled:opacity-40"
        aria-label="Send message"
      >
        <ArrowUp size={18} />
      </button>
    </form>
  );
}