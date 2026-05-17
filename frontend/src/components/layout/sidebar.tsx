"use client";

import {
  MessageSquare,
  Bell,
  Briefcase,
  Users,
  Star,
  PanelLeftClose,
  PanelLeftOpen,
} from "lucide-react";
import { useUIStore } from "@/stores/ui-store";
import type { SidebarSection } from "@/types/chat";
import { SidebarItem } from "@/components/layout/sidebar-item";
import { cn } from "@/lib/utils";

const NAV: { id: SidebarSection; label: string; icon: typeof MessageSquare }[] = [
  { id: "ask", label: "Ask", icon: MessageSquare },
  { id: "updates", label: "Updates", icon: Bell },
  { id: "work", label: "Work", icon: Briefcase },
  { id: "people", label: "People", icon: Users },
  { id: "important", label: "Important", icon: Star },
];

export function Sidebar() {
  const activeSection = useUIStore((s) => s.activeSection);
  const setActiveSection = useUIStore((s) => s.setActiveSection);
  const collapsed = useUIStore((s) => s.sidebarCollapsed);
  const toggle = useUIStore((s) => s.toggleSidebar);

  return (
    <aside
      className={cn(
        "flex h-full shrink-0 flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground transition-[width] duration-150 ease-out",
        collapsed ? "w-14" : "w-60",
      )}
    >
      <div
        className={cn(
          "flex h-14 items-center border-b border-sidebar-border px-3",
          collapsed && "justify-center px-0",
        )}
      >
        <div className={cn("flex items-center gap-2", collapsed && "justify-center")}>
          <div className="flex h-6 w-6 items-center justify-center rounded-md bg-sidebar-foreground text-[11px] font-semibold text-sidebar">
            N
          </div>
          {!collapsed && (
            <div className="flex flex-col leading-tight">
              <span className="text-sm font-medium">no-scrum</span>
              <span className="text-[11px] text-sidebar-muted">Acme · Workspace</span>
            </div>
          )}
        </div>
      </div>

      <nav className={cn("flex-1 space-y-0.5 px-2 py-3", collapsed && "px-1.5")}>
        {NAV.map((item) => (
          <SidebarItem
            key={item.id}
            icon={item.icon}
            label={item.label}
            active={activeSection === item.id}
            collapsed={collapsed}
            onClick={() => setActiveSection(item.id)}
          />
        ))}
      </nav>

      <div className="border-t border-sidebar-border p-2">
        <button
          type="button"
          onClick={toggle}
          className={cn(
            "flex w-full items-center gap-2.5 rounded-md px-2 py-1.5 text-xs text-sidebar-muted transition-colors hover:bg-sidebar-active/60 hover:text-sidebar-foreground",
            collapsed && "justify-center px-0",
          )}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? (
            <PanelLeftOpen size={16} strokeWidth={1.75} />
          ) : (
            <>
              <PanelLeftClose size={16} strokeWidth={1.75} />
              <span>Collapse</span>
            </>
          )}
        </button>
      </div>
    </aside>
  );
}
