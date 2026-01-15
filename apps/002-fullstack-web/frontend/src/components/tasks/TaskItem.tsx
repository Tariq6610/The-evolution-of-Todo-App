"use client";

import { motion } from "framer-motion";
import { CheckCircle, Clock, Tag, Edit2, Trash2 } from "lucide-react";

interface Task {
  id: string;
  title: string;
  description: string | null;
  status: string;
  priority: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

interface TaskItemProps {
  task: Task;
  onToggleStatus: (taskId: string) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

const priorityConfig = {
  high: {
    color: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
    bgLight: "hover:bg-red-50 dark:hover:bg-red-900/10",
  },
  medium: {
    color:
      "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",
    bgLight: "hover:bg-yellow-50 dark:hover:bg-yellow-900/10",
  },
  low: {
    color:
      "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
    bgLight: "hover:bg-green-50 dark:hover:bg-green-900/10",
  },
};

export default function TaskItem({
  task,
  onToggleStatus,
  onEdit,
  onDelete,
}: TaskItemProps) {
  const priority =
    priorityConfig[task.priority.toUpperCase() as keyof typeof priorityConfig];

  return (
    <motion.li
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ type: "spring", stiffness: 300, damping: 25 }}
      className={`py-4 sm:py-5 sm:px-6 ${priority.bgLight} transition-colors rounded-xl group`}
    >
      <div className="flex items-start gap-3 sm:gap-4">
        {/* Animated Checkbox */}
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => onToggleStatus(task.id)}
          className={`mt-0.5 flex-shrink-0 w-5 h-5 sm:w-6 sm:h-6 rounded-full border-2 flex items-center justify-center transition-all ${
            task.status === "completed"
              ? "bg-green-500 border-green-500 dark:border-green-500"
              : "border-gray-300 dark:border-gray-600 hover:border-green-500"
          }`}
          aria-label={`Mark ${task.title} as ${task.status === "completed" ? "pending" : "completed"}`}
        >
          {task.status === "completed" && (
            <motion.svg
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="w-3 h-3 sm:w-4 sm:h-4 text-white"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth={3}
            >
              <motion.path
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 0.2 }}
                d="M5 13l4 4L19 7"
              />
            </motion.svg>
          )}
        </motion.button>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <motion.p
            className={`text-sm sm:text-base font-medium line-clamp-1 ${
              task.status === "completed"
                ? "line-through text-gray-400 dark:text-gray-500"
                : "text-gray-900 dark:text-white"
            }`}
          >
            {task.title}
          </motion.p>
          {task.description && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mt-1 line-clamp-2"
            >
              {task.description}
            </motion.p>
          )}

          {/* Badges */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-2 sm:mt-3 flex items-center gap-2 flex-wrap"
          >
            {/* Priority */}
            <span
              className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium ${priority.color}`}
            >
              {task.priority === "high" && "🔴"}
              {task.priority === "medium" && "🟡"}
              {task.priority === "low" && "🟢"}
              {task.priority}
            </span>

            {/* Status */}
            <span
              className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium ${
                task.status === "completed"
                  ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
                  : "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
              }`}
            >
              {task.status === "completed" ? (
                <CheckCircle className="w-3 h-3" />
              ) : (
                <Clock className="w-3 h-3" />
              )}
              {task.status}
            </span>

            {/* Tags */}
            {task.tags.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {task.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400"
                  >
                    <Tag className="w-3 h-3" />
                    {tag}
                  </span>
                ))}
              </div>
            )}
          </motion.div>
        </div>

        {/* Action Buttons - Visible on Hover */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 0 }}
          whileHover={{ opacity: 1 }}
          className="flex items-center gap-1 sm:gap-2 opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onEdit(task)}
            className="inline-flex items-center gap-1 px-2 sm:px-3 py-1.5 text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
            aria-label={`Edit ${task.title}`}
          >
            <Edit2 className="w-3 h-3 sm:w-4 sm:h-4" />
            <span className="hidden sm:inline">Edit</span>
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onDelete(task.id)}
            className="inline-flex items-center gap-1 px-2 sm:px-3 py-1.5 text-xs sm:text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors"
            aria-label={`Delete ${task.title}`}
          >
            <Trash2 className="w-3 h-3 sm:w-4 sm:h-4" />
            <span className="hidden sm:inline">Delete</span>
          </motion.button>
        </motion.div>
      </div>
    </motion.li>
  );
}
