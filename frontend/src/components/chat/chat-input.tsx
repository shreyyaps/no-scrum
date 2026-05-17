"use client";

import { ArrowUp } from "lucide-react";
import { useEffect, useRef, useState, type FormEvent, type KeyboardEvent } from "react";
import { cn } from "@/lib/utils";

interface ChatInputProps {
  onSubmit: (value: string) => void;
  placeholder?: string;
  disabled?: boolean;
}

export function ChatInput({
  onSubmit,
  placeholder = "Ask anything…",
  disabled = false,
}: ChatInputProps) {
  const [value, setValue] = useState("");
  const ref = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = "0px";
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
  }, [value]);

  function submit() {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSubmit(trimmed);
    setValue("");
  }

  function onKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  function onFormSubmit(e: FormEvent) {
    e.preventDefault();
    submit();
  }

  const canSend = value.trim().length > 0 && !disabled;

  return (
    <form
      onSubmit={onFormSubmit}
      className={cn(
        "flex items-end gap-2 rounded-lg border border-border bg-background px-3 py-2",
        "focus-within:border-border-strong transition-colors",
      )}
    >
      <textarea
        ref={ref}
        rows={1}
        value={value}
        disabled={disabled}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
        className="flex-1 resize-none bg-transparent py-1.5 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={!canSend}
        aria-label="Send message"
        className={cn(
          "flex h-7 w-7 shrink-0 items-center justify-center rounded-md transition-colors",
          canSend
            ? "bg-foreground text-background hover:bg-foreground/90"
            : "bg-surface-muted text-muted-foreground",
        )}
      >
        <ArrowUp size={14} strokeWidth={2} />
      </button>
    </form>
  );
}
