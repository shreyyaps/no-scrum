"use client";

import { useEffect, useMemo, useRef } from "react";
import { useUIStore } from "@/stores/ui-store";
import { useMessages, useSendMessage } from "@/lib/hooks";
import { MessageBubble } from "@/components/chat/message-bubble";
import { ChatInput } from "@/components/chat/chat-input";
import type { SidebarSection } from "@/types/chat";

const SECTION_META: Record<
  SidebarSection,
  { title: string; description: string; placeholder: string }
> = {
  ask: {
    title: "Ask",
    description: "Anything about the workspace — work, people, blockers, decisions.",
    placeholder: "Ask anything…",
  },
  updates: {
    title: "Updates",
    description: "Recent activity and what changed since you last checked in.",
    placeholder: "Filter or ask about an update…",
  },
  work: {
    title: "Work",
    description: "Active work items — owners, blockers, urgency.",
    placeholder: "What's blocked? Who owns X?",
  },
  people: {
    title: "People",
    description: "Who is doing what — across teams.",
    placeholder: "Find someone or ask about a team…",
  },
  important: {
    title: "Important",
    description: "Surfaced items that need a decision or are at risk.",
    placeholder: "Ask about what's urgent…",
  },
};

export function ChatWindow() {
  const activeSection = useUIStore((s) => s.activeSection);
  const conversationId = activeSection;
  const meta = SECTION_META[activeSection];

  const { data: messages, isLoading } = useMessages(conversationId);
  const send = useSendMessage(conversationId);

  const scrollRef = useRef<HTMLDivElement>(null);
  const list = useMemo(() => messages ?? [], [messages]);

  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  }, [list.length]);

  return (
    <section className="flex h-full min-w-0 flex-1 flex-col bg-background">
      <header className="flex h-14 shrink-0 items-center border-b border-border px-6">
        <div className="flex flex-col leading-tight">
          <h1 className="text-sm font-medium text-foreground">{meta.title}</h1>
          <p className="text-xs text-muted-foreground">{meta.description}</p>
        </div>
      </header>

      <div ref={scrollRef} className="flex-1 overflow-y-auto">
        <div className="mx-auto flex w-full max-w-3xl flex-col gap-3 px-6 py-6">
          {isLoading && (
            <div className="text-xs text-muted-foreground">Loading…</div>
          )}
          {!isLoading && list.length === 0 && (
            <div className="text-xs text-muted-foreground">
              No messages yet. Start by asking a question below.
            </div>
          )}
          {list.map((m) => (
            <MessageBubble key={m.id} message={m} />
          ))}
        </div>
      </div>

      <div className="shrink-0 border-t border-border bg-background">
        <div className="mx-auto w-full max-w-3xl px-6 py-4">
          <ChatInput
            placeholder={meta.placeholder}
            disabled={send.isPending}
            onSubmit={(value) => send.mutate(value)}
          />
          <p className="mt-2 text-[11px] text-muted-foreground">
            Enter to send · Shift + Enter for newline
          </p>
        </div>
      </div>
    </section>
  );
}
