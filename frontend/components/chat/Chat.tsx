"use client";

import { useEffect, useRef, useState } from "react";

import SunriseLogo from "@/components/brand/SunriseLogo";
import { checkBackendHealth, sendMessage } from "@/lib/api";
import type { ConversationMessage } from "@/types/chat";

import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";
import SuggestedQuestions from "./SuggestedQuestions";

export default function Chat() {
  const [messages, setMessages] = useState<ConversationMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [backendReady, setBackendReady] = useState(false);
  const [checkingBackend, setCheckingBackend] = useState(true);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function connectToBackend() {
      setCheckingBackend(true);

      const isHealthy = await checkBackendHealth();

      setBackendReady(isHealthy);
      setCheckingBackend(false);
    }

    connectToBackend();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages, loading]);

  async function handleSend(message: string) {
    if (loading || !backendReady) {
      return;
    }

    setError(null);

    const userMessage: ConversationMessage = {
      role: "user",
      content: message,
    };

    setMessages((current) => [...current, userMessage]);
    setLoading(true);

    try {
      const conversation = messages.map(({ role, content }) => ({
        role,
        content,
      }));

      const response = await sendMessage(message, conversation);

      const assistantMessage: ConversationMessage = {
        role: "assistant",
        content: response.message,
        type: response.type,
        data: response.data,
      };

      setMessages((current) => [...current, assistantMessage]);
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  const isEmpty = messages.length === 0;

  return (
    <main className="flex h-dvh flex-col overflow-hidden bg-[#FFF7ED]">
      {/* Header */}
      <header className="z-20 shrink-0 border-b border-[#E7E5E4] bg-white">
        <div className="mx-auto flex h-16 w-full max-w-4xl items-center px-4 sm:px-6">
          <SunriseLogo size="md" showName />
        </div>
      </header>

      {/* Main content */}
      <div className="mx-auto flex min-h-0 w-full max-w-4xl flex-1 flex-col px-4 sm:px-6">
        {/* Scrollable chat area */}
        <div className="min-h-0 flex-1 overflow-y-auto overscroll-contain">
          {isEmpty ? (
            <div className="flex min-h-full items-center justify-center">
              <div className="w-full max-w-2xl py-10">
                <div className="mb-8 text-center">
                  <div className="mb-3 text-sm font-medium text-[#F97316]">
                    Sunrise Hotel Assistant
                  </div>

                  <h1 className="text-2xl font-semibold tracking-tight text-[#292524] sm:text-3xl">
                    How can we help?
                  </h1>

                  <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-[#78716C] sm:text-base">
                    Ask anything about rooms, amenities, policies, breakfast,
                    or availability.
                  </p>
                </div>

                <SuggestedQuestions
                  onSelect={handleSend}
                  disabled={
                    loading ||
                    checkingBackend ||
                    !backendReady
                  }
                />
              </div>
            </div>
          ) : (
            <div className="py-6 sm:py-8">
              <div className="space-y-5">
                {messages.map((message, index) => (
                  <MessageBubble
                    key={`${message.role}-${index}`}
                    message={message}
                  />
                ))}

                {loading && (
                  <div className="flex justify-start">
                    <div className="rounded-2xl rounded-bl-md border border-[#E7E5E4] bg-white px-4 py-3 shadow-sm">
                      <div className="flex items-center gap-1.5">
                        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-[#A8A29E]" />
                        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-[#A8A29E] [animation-delay:150ms]" />
                        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-[#A8A29E] [animation-delay:300ms]" />
                      </div>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="shrink-0 bg-[#FFF7ED] pb-3 pt-3 sm:pb-5">
          {error && (
            <div className="mb-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              {error}
            </div>
          )}

          {checkingBackend && (
            <div className="mb-3 rounded-xl border border-[#E7E5E4] bg-white px-4 py-3 text-center text-sm text-[#78716C]">
              Connecting to Sunrise Hotel Assistant...
            </div>
          )}

          {!checkingBackend && !backendReady && (
            <div className="mb-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-center text-sm text-red-700">
              Unable to connect to the hotel assistant. Please try again.
            </div>
          )}

          <ChatInput
            onSend={handleSend}
            disabled={
              loading ||
              checkingBackend ||
              !backendReady
            }
          />

          <p className="mt-2 px-2 text-center text-[11px] leading-4 text-[#A8A29E] sm:text-xs">
            Sunrise Hotel Assistant · Rooms · Amenities · Policies ·
            Availability
          </p>
        </div>
      </div>
    </main>
  );
}