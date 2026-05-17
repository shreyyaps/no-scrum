"use client";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import { fetchMessages, fetchUpdates, postMessage } from "@/lib/mock-api";
import type { Message } from "@/types/chat";

export function useMessages(conversationId: string) {
  return useQuery({
    queryKey: ["messages", conversationId],
    queryFn: () => fetchMessages(conversationId),
  });
}

export function useSendMessage(conversationId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (content: string) => postMessage(conversationId, content),
    onMutate: async (content) => {
      await qc.cancelQueries({ queryKey: ["messages", conversationId] });
      const previous = qc.getQueryData<Message[]>([
        "messages",
        conversationId,
      ]);
      const optimistic: Message = {
        id: `optimistic-${Date.now()}`,
        role: "user",
        content,
        createdAt: new Date().toISOString(),
      };
      qc.setQueryData<Message[]>(
        ["messages", conversationId],
        (old) => [...(old ?? []), optimistic],
      );
      return { previous };
    },
    onError: (_err, _content, ctx) => {
      if (ctx?.previous) {
        qc.setQueryData(["messages", conversationId], ctx.previous);
      }
    },
    onSettled: () => {
      qc.invalidateQueries({ queryKey: ["messages", conversationId] });
    },
  });
}

export function useUpdates() {
  return useQuery({
    queryKey: ["updates"],
    queryFn: fetchUpdates,
  });
}
