export type MessageRole = "user" | "assistant";

export type ResponseType = "answer" | "availability" | "error";

export interface ConversationMessage {
  role: MessageRole;
  content: string;
  type?: ResponseType;
  data?: AvailabilityData | null;
}

export interface AvailableRoom {
  room_id: string;
  name: string;
  description: string;
  max_guests: number;
  price_per_night: number;
  currency: string;
  breakfast_included: boolean;
  beds: string;
}

export interface AvailabilityData {
  available: boolean;
  check_in: string;
  check_out: string;
  guests: number;
  rooms: AvailableRoom[];
}

export interface ChatResponse {
  message: string;
  type: ResponseType;
  data: AvailabilityData | null;
}