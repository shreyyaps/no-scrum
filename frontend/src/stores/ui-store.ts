import { create } from "zustand";
import type { SidebarSection } from "@/types/chat";

interface UIState {
  activeSection: SidebarSection;
  sidebarCollapsed: boolean;
  selectedConversationId: string | null;
  setActiveSection: (section: SidebarSection) => void;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  setSelectedConversationId: (id: string | null) => void;
}

export const useUIStore = create<UIState>((set) => ({
  activeSection: "ask",
  sidebarCollapsed: false,
  selectedConversationId: null,
  setActiveSection: (section) => set({ activeSection: section }),
  toggleSidebar: () =>
    set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
  setSidebarCollapsed: (sidebarCollapsed) => set({ sidebarCollapsed }),
  setSelectedConversationId: (selectedConversationId) =>
    set({ selectedConversationId }),
}));
