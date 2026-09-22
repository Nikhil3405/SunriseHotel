import type { ChatResponse, ConversationMessage } from "@/types/chat";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function checkBackendHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/health`, {
      method: "GET",
      cache: "no-store",
    });

    return response.ok;
  } catch {
    return false;
  }
}

export async function sendMessage(
  message: string,
  conversation: ConversationMessage[]
): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      conversation,
    }),
  });

  if (!response.ok) {
    throw new Error("Unable to process your request.");
  }

  return response.json();
}