import type { Message } from "@/types/chat";
import { cn } from "@/lib/utils";

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  return (
    <div className={cn("flex w-full", isUser ? "justify-end" : "justify-start")}>
      <div
        className={cn(
          "max-w-[680px] rounded-lg border px-3.5 py-2.5 text-sm leading-relaxed",
          isUser
            ? "border-border-strong bg-foreground text-background"
            : "border-border bg-surface text-foreground",
        )}
      >
        {message.content}
      </div>
    </div>
  );
}
