"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";

interface SidebarItemProps {
  href: string;
  label: string;
  icon: LucideIcon;
  isCollapsed: boolean;
  isActive: boolean;
  isLogout?: boolean;
}

export function SidebarItem({
  href,
  label,
  icon: Icon,
  isCollapsed,
  isActive,
  isLogout,
}: SidebarItemProps) {
  // For logout, we render a button instead of a link
  if (isLogout) {
    return (
      <button
        className={`w-full flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-200 ${
          isCollapsed ? "justify-center" : ""
        } ${
          isActive
            ? "bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400"
            : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white"
        }`}
        title={isCollapsed ? label : undefined}
        onClick={() => {
          // Handle logout logic here
          console.log("Logout clicked");
        }}
      >
        <Icon
          size={20}
          className={`flex-shrink-0 ${isActive ? "text-red-600 dark:text-red-400" : ""}`}
        />
        {!isCollapsed && (
          <span className="font-medium relative z-10">{label}</span>
        )}
        {isActive && !isCollapsed && (
          <div className="ml-auto w-2 h-2 rounded-full bg-blue-500" />
        )}
      </button>
    );
  }

  return (
    <Link
      href={href}
      className={`relative flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-200 ${
        isCollapsed ? "justify-center" : ""
      } ${
        isActive
          ? "bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400"
          : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white"
      }`}
      title={isCollapsed ? label : undefined}
    >
      {/* Active Indicator */}
      {isActive && (
        <motion.div
          className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 rounded-r-full bg-blue-500"
          initial={false}
          transition={{ type: "spring", stiffness: 500, damping: 30 }}
        />
      )}

      <Icon
        size={20}
        className={`flex-shrink-0 transition-transform group-hover:scale-110 ${
          isActive ? "text-blue-600 dark:text-blue-400" : ""
        }`}
      />

      {!isCollapsed && (
        <span className="font-medium relative z-10">{label}</span>
      )}
    </Link>
  );
}
