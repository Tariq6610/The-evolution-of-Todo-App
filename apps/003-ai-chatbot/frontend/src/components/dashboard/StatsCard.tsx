"use client";

import { ReactNode } from "react";
import { motion } from "framer-motion";
import AnimatedCounter from "./AnimatedCounter";

interface StatsCardProps {
  title: string;
  value: number;
  icon: ReactNode;
  color: "blue" | "green" | "yellow" | "red" | "purple";
  suffix?: string;
  className?: string;
}

const colorVariants = {
  blue: {
    bg: "bg-blue-50 dark:bg-blue-900/20",
    icon: "bg-blue-100 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400",
    text: "text-blue-600 dark:text-blue-400",
  },
  green: {
    bg: "bg-green-50 dark:bg-green-900/20",
    icon: "bg-green-100 dark:bg-green-900/40 text-green-600 dark:text-green-400",
    text: "text-green-600 dark:text-green-400",
  },
  yellow: {
    bg: "bg-yellow-50 dark:bg-yellow-900/20",
    icon: "bg-yellow-100 dark:bg-yellow-900/40 text-yellow-600 dark:text-yellow-400",
    text: "text-yellow-600 dark:text-yellow-400",
  },
  red: {
    bg: "bg-red-50 dark:bg-red-900/20",
    icon: "bg-red-100 dark:bg-red-900/40 text-red-600 dark:text-red-400",
    text: "text-red-600 dark:text-red-400",
  },
  purple: {
    bg: "bg-purple-50 dark:bg-purple-900/20",
    icon: "bg-purple-100 dark:bg-purple-900/40 text-purple-600 dark:text-purple-400",
    text: "text-purple-600 dark:text-purple-400",
  },
};

interface StatsCardComponentProps extends StatsCardProps {
  delay?: number;
}

export default function StatsCard({
  title,
  value,
  icon,
  color,
  suffix = "",
  className = "",
  delay = 0,
}: StatsCardComponentProps) {
  const variants = colorVariants[color];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      whileHover={{ y: -4, boxShadow: "0 20px 25px -5px rgb(0 0 0 / 0.1)" }}
      className={`bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-100 dark:border-gray-700 transition-all ${className}`}
    >
      <div className="flex items-center gap-3">
        <div className={`p-2.5 rounded-lg ${variants.icon}`}>{icon}</div>
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
          <p className={`text-2xl font-bold ${variants.text}`}>
            <AnimatedCounter value={value} suffix={suffix} />
          </p>
        </div>
      </div>
    </motion.div>
  );
}

export { colorVariants };
