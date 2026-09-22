import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { ConversationMessage } from "@/types/chat";
import RoomCard from "./RoomCard";

type MessageBubbleProps = {
  message: ConversationMessage;
};

function normalizeMarkdown(content: string) {
  // The LLM sometimes returns escaped Markdown such as \*\*text\*\*.
  return content.replace(/\\([\\`*_[\]{}()#+.!|>~-])/g, "$1");
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-[90%] rounded-2xl rounded-br-md bg-[#F97316] px-4 py-3 text-sm leading-6 text-white sm:max-w-[75%]">
          {message.content}
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start">
      <div className="max-w-[95%] sm:max-w-[85%]">
        <div className="rounded-2xl rounded-bl-md border border-[#E7E5E4] bg-white px-4 py-3 text-sm leading-6 text-[#292524] shadow-sm">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              p: ({ children }) => (
                <p className="mb-2 last:mb-0">{children}</p>
              ),

              strong: ({ children }) => (
                <strong className="font-semibold">{children}</strong>
              ),

              ul: ({ children }) => (
                <ul className="my-2 list-disc space-y-1 pl-5">
                  {children}
                </ul>
              ),

              ol: ({ children }) => (
                <ol className="my-2 list-decimal space-y-1 pl-5">
                  {children}
                </ol>
              ),

              li: ({ children }) => <li>{children}</li>,

              table: ({ children }) => (
                <div className="my-3 overflow-x-auto">
                  <table className="w-full min-w-125 border-collapse text-sm">
                    {children}
                  </table>
                </div>
              ),

              thead: ({ children }) => (
                <thead className="bg-[#FFF7ED]">{children}</thead>
              ),

              th: ({ children }) => (
                <th className="border border-[#E7E5E4] px-3 py-2 text-left font-semibold">
                  {children}
                </th>
              ),

              td: ({ children }) => (
                <td className="border border-[#E7E5E4] px-3 py-2">
                  {children}
                </td>
              ),

              code: ({ children }) => (
                <code className="rounded bg-[#F5F5F4] px-1.5 py-0.5 text-xs">
                  {children}
                </code>
              ),

              blockquote: ({ children }) => (
                <blockquote className="my-2 border-l-4 border-[#FDBA74] pl-3 text-[#57534E]">
                  {children}
                </blockquote>
              ),
            }}
          >
            {normalizeMarkdown(message.content)}
          </ReactMarkdown>
        </div>

        {message.type === "availability" &&
          message.data?.available &&
          message.data.rooms.length > 0 && (
            <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2">
              {message.data.rooms.map((room) => (
                <RoomCard key={room.room_id} room={room} />
              ))}
            </div>
          )}
      </div>
    </div>
  );
}