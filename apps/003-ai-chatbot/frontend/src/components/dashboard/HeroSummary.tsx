"use client";

import { useState, useEffect, useRef } from "react";
import { motion, useInView, useSpring } from "framer-motion";
import AnimatedCounter from "./AnimatedCounter";

interface HeroSummaryProps {
  userName?: string;
  completedTasks: number;
  totalTasks: number;
}

export default function HeroSummary({
  userName = "there",
  completedTasks,
  totalTasks,
}: HeroSummaryProps) {
  const greeting = (() => {
    const hour = new Date().getHours();
    if (hour < 12) return "Good morning";
    if (hour < 17) return "Good afternoon";
    return "Good evening";
  })();

  const progressPercentage =
    totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="relative overflow-hidden bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-600 rounded-2xl p-6 md:p-8 text-white shadow-xl"
    >
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <svg
          className="w-full h-full"
          viewBox="0 0 100 100"
          preserveAspectRatio="none"
        >
          <defs>
            <pattern
              id="grid"
              width="10"
              height="10"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M 10 0 L 0 0 0 10"
                fill="none"
                stroke="currentColor"
                strokeWidth="0.5"
              />
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#grid)" />
        </svg>
      </div>

      {/* Floating circles */}
      <motion.div
        className="absolute -top-10 -right-10 w-40 h-40 bg-white/10 rounded-full blur-2xl"
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.3, 0.5, 0.3],
        }}
        transition={{ duration: 4, repeat: Infinity }}
      />
      <motion.div
        className="absolute -bottom-10 -left-10 w-32 h-32 bg-purple-400/20 rounded-full blur-2xl"
        animate={{
          scale: [1, 1.3, 1],
          opacity: [0.2, 0.4, 0.2],
        }}
        transition={{ duration: 5, repeat: Infinity }}
      />

      <div className="relative z-10">
        <motion.h1
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="text-2xl md:text-3xl font-semibold mb-2"
        >
          {greeting}, {userName}!
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="text-blue-100 text-base md:text-lg mb-6"
        >
          {totalTasks === 0
            ? "Start by adding your first task"
            : `You've completed ${completedTasks} of ${totalTasks} tasks`}
        </motion.p>

        <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6">
          {/* Progress Circle */}
          <div className="relative w-24 h-24 flex-shrink-0">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="48"
                cy="48"
                r="42"
                stroke="rgba(255,255,255,0.2)"
                strokeWidth="8"
                fill="none"
              />
              <motion.circle
                cx="48"
                cy="48"
                r="42"
                stroke="white"
                strokeWidth="8"
                fill="none"
                strokeLinecap="round"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: progressPercentage / 100 }}
                transition={{ duration: 1.5, ease: "easeOut" }}
                style={{
                  strokeDasharray: "264",
                  strokeDashoffset: 264 - (264 * progressPercentage) / 100,
                }}
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-xl font-bold">
                <AnimatedCounter value={progressPercentage} suffix="%" />
              </span>
            </div>
          </div>

          {/* Progress Bar (mobile alternative) */}
          <div className="w-full sm:w-48 h-3 bg-white/20 rounded-full overflow-hidden sm:hidden">
            <motion.div
              className="h-full bg-white rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${progressPercentage}%` }}
              transition={{ duration: 1.5, ease: "easeOut" }}
            />
          </div>

          {/* Quick Stats */}
          <div className="flex gap-4 text-sm">
            <div className="text-center">
              <div className="text-xl font-bold">
                <AnimatedCounter value={totalTasks - completedTasks} />
              </div>
              <div className="text-blue-200 text-xs">Remaining</div>
            </div>
            <div className="w-px bg-white/30" />
            <div className="text-center">
              <div className="text-xl font-bold">
                <AnimatedCounter value={completedTasks} />
              </div>
              <div className="text-blue-200 text-xs">Done</div>
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}
