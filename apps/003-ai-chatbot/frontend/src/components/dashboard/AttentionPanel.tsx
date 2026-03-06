"use client";

import { motion } from "framer-motion";
import { AlertCircle, Clock, ArrowRight } from "lucide-react";

interface Task {
  id: string;
  title: string;
  priority: string;
  status: string;
  updated_at: string;
}

interface AttentionPanelProps {
  highPriorityTasks: Task[];
  recentTasks: Task[];
  onViewAll?: () => void;
}

const priorityOrder = { high: 0, medium: 1, low: 2 };

export default function AttentionPanel({
  highPriorityTasks,
  recentTasks,
  onViewAll,
}: AttentionPanelProps) {
  const sortedHighPriority = [...highPriorityTasks]
    .sort(
      (a, b) =>
        priorityOrder[a.priority as keyof typeof priorityOrder] -
        priorityOrder[b.priority as keyof typeof priorityOrder],
    )
    .slice(0, 5);

  const sortedRecentTasks = [...recentTasks]
    .sort(
      (a, b) =>
        new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime(),
    )
    .slice(0, 3);

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${diffDays}d ago`;
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high":
        return "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400";
      case "medium":
        return "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400";
      case "low":
        return "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400";
      default:
        return "bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300";
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.4 }}
      className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden"
    >
      <div className="px-4 py-3 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-amber-500" />
          Needs Attention
        </h3>
        {onViewAll && (
          <button
            onClick={onViewAll}
            className="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 flex items-center gap-1"
          >
            View all
            <ArrowRight className="w-3 h-3" />
          </button>
        )}
      </div>

      <div className="divide-y divide-gray-100 dark:divide-gray-700">
        {sortedHighPriority.length > 0 ? (
          sortedHighPriority.map((task, index) => (
            <motion.div
              key={task.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors cursor-pointer"
            >
              <div className="flex items-start justify-between gap-2">
                <p className="text-sm font-medium text-gray-900 dark:text-white line-clamp-1">
                  {task.title}
                </p>
                <span
                  className={`flex-shrink-0 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${getPriorityColor(
                    task.priority,
                  )}`}
                >
                  {task.priority}
                </span>
              </div>
              <div className="mt-1 flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                <Clock className="w-3 h-3" />
                <span>{formatTime(task.updated_at)}</span>
              </div>
            </motion.div>
          ))
        ) : sortedRecentTasks.length > 0 ? (
          sortedRecentTasks.map((task, index) => (
            <motion.div
              key={task.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors cursor-pointer"
            >
              <div className="flex items-start justify-between gap-2">
                <p className="text-sm font-medium text-gray-900 dark:text-white line-clamp-1">
                  {task.title}
                </p>
                <span
                  className={`flex-shrink-0 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${getPriorityColor(
                    task.priority,
                  )}`}
                >
                  {task.priority}
                </span>
              </div>
              <div className="mt-1 flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                <Clock className="w-3 h-3" />
                <span>Updated {formatTime(task.updated_at)}</span>
              </div>
            </motion.div>
          ))
        ) : (
          <div className="px-4 py-8 text-center text-sm text-gray-500 dark:text-gray-400">
            No tasks need attention
          </div>
        )}
      </div>
    </motion.div>
  );
}
