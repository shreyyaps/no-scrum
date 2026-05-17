import type { Message, Update } from "@/types/chat";

function delay<T>(value: T, ms = 350): Promise<T> {
  return new Promise((resolve) => setTimeout(() => resolve(value), ms));
}

const seedMessages: Record<string, Message[]> = {
  ask: [
    {
      id: "m-1",
      role: "system",
      content:
        "Welcome. Ask anything about the workspace — work, people, blockers, decisions.",
      createdAt: "2026-05-17T09:00:00Z",
    },
    {
      id: "m-2",
      role: "user",
      content: "What's blocked right now?",
      createdAt: "2026-05-17T09:01:00Z",
    },
    {
      id: "m-3",
      role: "system",
      content:
        "Two items: the billing migration is waiting on a decision from Priya, and the iOS release is blocked by App Review.",
      createdAt: "2026-05-17T09:01:08Z",
    },
  ],
};

const seedUpdates: Update[] = [
  {
    id: "u-1",
    title: "Billing migration",
    body: "Schema cutover landed in staging. Awaiting decision on rollout window.",
    createdAt: "2026-05-17T08:42:00Z",
  },
  {
    id: "u-2",
    title: "iOS 4.2 release",
    body: "Submitted to App Review. ETA 24–48h.",
    createdAt: "2026-05-17T07:10:00Z",
  },
  {
    id: "u-3",
    title: "Onboarding revamp",
    body: "Design review wrapped. Eng kickoff Monday.",
    createdAt: "2026-05-16T22:05:00Z",
  },
];

export async function fetchMessages(conversationId: string): Promise<Message[]> {
  return delay(seedMessages[conversationId] ?? seedMessages.ask);
}

export async function postMessage(
  conversationId: string,
  content: string,
): Promise<Message> {
  const message: Message = {
    id: `m-${Date.now()}`,
    role: "user",
    content,
    createdAt: new Date().toISOString(),
  };
  const list = seedMessages[conversationId] ?? (seedMessages[conversationId] = []);
  list.push(message);
  // Simulated system reply.
  const reply: Message = {
    id: `m-${Date.now() + 1}`,
    role: "system",
    content: "Got it — I'll dig into that.",
    createdAt: new Date().toISOString(),
  };
  list.push(reply);
  return delay(message, 250);
}

export async function fetchUpdates(): Promise<Update[]> {
  return delay(seedUpdates);
}
