"use client";

import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle, Circle, Clock, Tag } from "lucide-react";

interface AnimatedTaskItemProps {
  task: {
    id: string;
    title: string;
    description: string | null;
    status: string;
    priority: string;
    tags: string[];
    created_at: string;
    updated_at: string;
  };
  index: number;
  onToggle: () => void;
  onEdit: () => void;
  onDelete: () => void;
}

const priorityConfig = {
  HIGH: {
    color: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
    icon: "🔴",
  },
  MEDIUM: {
    color:
      "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",
    icon: "🟡",
  },
  LOW: {
    color:
      "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
    icon: "🟢",
  },
};

export function AnimatedTaskItem({
  task,
  index,
  onToggle,
  onEdit,
  onDelete,
}: AnimatedTaskItemProps) {
  const priority = priorityConfig[task.priority as keyof typeof priorityConfig];

  return (
    <motion.li
      key={task.id}
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, x: -100, scale: 0.95 }}
      transition={{
        type: "spring",
        stiffness: 300,
        damping: 25,
        delay: index * 0.05,
      }}
      layout
      className="group"
    >
      <motion.div
        whileHover={{ scale: 1.005 }}
        className="p-4 sm:p-5 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-all rounded-xl"
      >
        <div className="flex items-start gap-3 sm:gap-4">
          {/* Animated Checkbox */}
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={onToggle}
            className={`mt-0.5 flex-shrink-0 w-5 h-5 sm:w-6 sm:h-6 rounded-full border-2 flex items-center justify-center transition-all ${
              task.status === "COMPLETED"
                ? "bg-green-500 border-green-500 dark:border-green-500"
                : "border-gray-300 dark:border-gray-600 hover:border-green-500"
            }`}
          >
            <AnimatePresence mode="wait">
              {task.status === "COMPLETED" && (
                <motion.svg
                  key="checkmark"
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  exit={{ scale: 0, opacity: 0 }}
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
            </AnimatePresence>
          </motion.button>

          {/* Task Content */}
          <div className="flex-1 min-w-0">
            <motion.p
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 + index * 0.05 }}
              className={`text-sm sm:text-base font-medium line-clamp-1 ${
                task.status === "COMPLETED"
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
                transition={{ delay: 0.15 + index * 0.05 }}
                className="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mt-1 line-clamp-2"
              >
                {task.description}
              </motion.p>
            )}

            {/* Tags and Priority */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 + index * 0.05 }}
              className="mt-2 sm:mt-3 flex items-center gap-2 flex-wrap"
            >
              {/* Priority Badge with Animation */}
              <motion.span
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 400, damping: 15 }}
                className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium ${priority.color}`}
              >
                {priority.icon}
                {task.priority}
              </motion.span>

              {/* Status Badge */}
              <motion.span
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{
                  type: "spring",
                  stiffness: 400,
                  damping: 15,
                  delay: 0.1,
                }}
                className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                  task.status === "COMPLETED"
                    ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
                    : "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
                }`}
              >
                {task.status === "COMPLETED" ? (
                  <CheckCircle className="w-3 h-3 mr-1" />
                ) : (
                  <Clock className="w-3 h-3 mr-1" />
                )}
                {task.status}
              </motion.span>

              {/* Tags */}
              {task.tags.map((tag, i) => (
                <motion.span
                  key={tag}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{
                    type: "spring",
                    stiffness: 400,
                    damping: 15,
                    delay: 0.15 + i * 0.05,
                  }}
                  className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400"
                >
                  <Tag className="w-3 h-3" />
                  {tag}
                </motion.span>
              ))}
            </motion.div>
          </div>

          {/* Action Buttons - Visible on Hover */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 0, x: 0 }}
            whileHover={{ opacity: 1, x: 0 }}
            className="flex items-center gap-1 sm:gap-2 opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onEdit}
              className="px-2 sm:px-3 py-1.5 text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
            >
              Edit
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onDelete}
              className="px-2 sm:px-3 py-1.5 text-xs sm:text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors"
            >
              Delete
            </motion.button>
          </motion.div>
        </div>
      </motion.div>
    </motion.li>
  );
}

// Re-export AnimatePresence for convenience
export { AnimatePresence } from "framer-motion";
