"use client";

import Link from "next/link";
import { CheckCircle2 } from "lucide-react";
import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center space-y-8 py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex items-center space-x-3 text-indigo-600 dark:text-indigo-400"
      >
        <CheckCircle2 size={48} suppressHydrationWarning />
        <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
          Todo App
        </h1>
      </motion.div>

      <motion.p
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="max-w-2xl text-xl text-center text-gray-600 dark:text-gray-300"
      >
        A simple, clean, and powerful way to manage your tasks. Experience the
        evolution of task management from console to full-stack web.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="flex flex-col space-y-4 sm:flex-row sm:space-x-4 sm:space-y-0"
      >
        <Button
          asChild
          className="bg-indigo-600 hover:bg-indigo-700 text-white"
        >
          <Link href="/login">Sign In</Link>
        </Button>
        <Button variant="outline" asChild>
          <Link href="/register">Create Account</Link>
        </Button>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-3 w-full max-w-4xl"
      >
        <Card className="border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-shadow">
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white leading-6">
              Persistent
            </h3>
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              Powered by Neon DB for reliable, long-term storage of your tasks.
            </p>
          </CardContent>
        </Card>
        <Card className="border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-shadow">
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white leading-6">
              Secure
            </h3>
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              JWT-based authentication ensures your data remains private and
              safe.
            </p>
          </CardContent>
        </Card>
        <Card className="border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-shadow">
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white leading-6">
              Responsive
            </h3>
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              Access your tasks from anywhere - whether on your phone or your
              desktop.
            </p>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
