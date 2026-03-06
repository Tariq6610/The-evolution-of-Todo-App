"use client";

import { motion } from "framer-motion";
import { Plus, Star, ListTodo, Calendar } from "lucide-react";

interface QuickActionsProps {
  onAddTask?: () => void;
  onAddHighPriority?: () => void;
  onNavigateToTasks?: () => void;
  onAddScheduled?: () => void;
}

interface ActionButton {
  icon: React.ReactNode;
  label: string;
  onClick: () => void;
  color: string;
  delay: number;
}

export default function QuickActions({
  onAddTask,
  onAddHighPriority,
  onNavigateToTasks,
  onAddScheduled,
}: QuickActionsProps) {
  const actions: ActionButton[] = [
    {
      icon: <Plus className="w-4 h-4" />,
      label: "Add Task",
      onClick: onAddTask || (() => {}),
      color: "bg-blue-500 hover:bg-blue-600",
      delay: 0,
    },
    {
      icon: <Star className="w-4 h-4" />,
      label: "High Priority",
      onClick: onAddHighPriority || (() => {}),
      color: "bg-red-500 hover:bg-red-600",
      delay: 0.1,
    },
    {
      icon: <Calendar className="w-4 h-4" />,
      label: "Scheduled",
      onClick: onAddScheduled || (() => {}),
      color: "bg-purple-500 hover:bg-purple-600",
      delay: 0.2,
    },
    {
      icon: <ListTodo className="w-4 h-4" />,
      label: "All Tasks",
      onClick: onNavigateToTasks || (() => {}),
      color: "bg-gray-500 hover:bg-gray-600",
      delay: 0.3,
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.5 }}
      className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-100 dark:border-gray-700"
    >
      <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-3">
        Quick Actions
      </h3>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
        {actions.map((action) => (
          <motion.button
            key={action.label}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3, delay: action.delay }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={action.onClick}
            className={`flex flex-col items-center gap-2 p-3 rounded-lg text-white ${action.color} transition-colors shadow-sm hover:shadow-md`}
          >
            {action.icon}
            <span className="text-xs font-medium">{action.label}</span>
          </motion.button>
        ))}
      </div>
    </motion.div>
  );
}
