export type SidebarSection =
  | "ask"
  | "updates"
  | "work"
  | "people"
  | "important";

export type MessageRole = "user" | "system";

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  createdAt: string;
}

export interface Update {
  id: string;
  title: string;
  body: string;
  createdAt: string;
}

export interface WorkItem {
  id: string;
  title: string;
  owner: string;
  blockedBy: string | null;
  needsDecision: boolean;
  urgency: "low" | "medium" | "high";
  lastUpdated: string;
}
