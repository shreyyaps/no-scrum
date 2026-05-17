"use client";

import type { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface SidebarItemProps {
  icon: LucideIcon;
  label: string;
  active?: boolean;
  collapsed?: boolean;
  onClick?: () => void;
}

export function SidebarItem({
  icon: Icon,
  label,
  active = false,
  collapsed = false,
  onClick,
}: SidebarItemProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      title={collapsed ? label : undefined}
      className={cn(
        "group flex w-full items-center gap-2.5 rounded-md px-2 py-1.5 text-sm transition-colors",
        active
          ? "bg-sidebar-active text-sidebar-foreground"
          : "text-sidebar-muted hover:bg-sidebar-active/60 hover:text-sidebar-foreground",
        collapsed && "justify-center px-0",
      )}
    >
      <Icon
        size={16}
        strokeWidth={1.75}
        className={cn(
          "shrink-0",
          active ? "text-sidebar-foreground" : "text-sidebar-muted group-hover:text-sidebar-foreground",
        )}
      />
      {!collapsed && <span className="truncate">{label}</span>}
    </button>
  );
}
