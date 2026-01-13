"use client";

import { motion } from "framer-motion";
import { Lightbulb } from "lucide-react";

interface SmartInsightProps {
  insight: string;
  subtitle?: string;
}

export default function SmartInsight({ insight, subtitle }: SmartInsightProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4, delay: 0.6 }}
      whileHover={{ y: -2 }}
      className="bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/10 rounded-xl p-4 shadow-sm border border-amber-100 dark:border-amber-900/30"
    >
      <div className="flex items-start gap-3">
        <div className="p-2 bg-amber-100 dark:bg-amber-900/40 rounded-lg">
          <Lightbulb className="w-4 h-4 text-amber-600 dark:text-amber-400" />
        </div>
        <div className="flex-1">
          <h3 className="text-sm font-semibold text-gray-900 dark:text-white">
            Smart Insight
          </h3>
          <p className="mt-1 text-sm text-gray-700 dark:text-gray-300">
            {insight}
          </p>
          {subtitle && (
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              {subtitle}
            </p>
          )}
        </div>
      </div>
    </motion.div>
  );
}

// Helper function to generate insights from task data
export function generateInsight(
  completedTasks: number,
  totalTasks: number,
  highPriorityPending: number,
  mediumPriority: number,
  lowPriority: number,
): { insight: string; subtitle?: string } {
  const completionRate =
    totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

  // Generate insights based on data patterns
  if (totalTasks === 0) {
    return {
      insight:
        "Start by adding your first task to begin tracking your productivity.",
      subtitle: "Tasks help you organize and prioritize your work",
    };
  }

  if (highPriorityPending > 0 && highPriorityPending <= 2) {
    return {
      insight: `You have ${highPriorityPending} high-priority task${highPriorityPending > 1 ? "s" : ""} waiting.`,
      subtitle: "Consider completing these first for maximum impact",
    };
  }

  if (completionRate >= 80 && completionRate < 100) {
    return {
      insight: "You're almost there! Just a few more tasks to complete.",
      subtitle: `Only ${totalTasks - completedTasks} tasks remaining`,
    };
  }

  if (completionRate === 100 && totalTasks > 0) {
    return {
      insight: "All tasks completed! Great work!",
      subtitle: "Time to add new goals or take on new challenges",
    };
  }

  if (lowPriority > mediumPriority && lowPriority > highPriorityPending) {
    return {
      insight: "Most of your tasks are low priority.",
      subtitle: "Consider raising some to medium or high for better focus",
    };
  }

  if (mediumPriority > highPriorityPending + lowPriority) {
    return {
      insight: "You're focusing on medium-priority work.",
      subtitle: "Good balance for steady progress",
    };
  }

  // Default insight
  return {
    insight: `You've completed ${completedTasks} out of ${totalTasks} tasks.`,
    subtitle: "Keep up the momentum!",
  };
}
