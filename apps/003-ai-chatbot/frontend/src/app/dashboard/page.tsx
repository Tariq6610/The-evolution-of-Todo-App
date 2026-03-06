"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  Plus,
  ListTodo,
  CheckCircle,
  Clock,
  AlertCircle,
  LogOut,
  ChevronRight,
  BarChart3,
} from "lucide-react";
import apiClient from "@/services/api_client";
import { Sidebar } from "@/components/layout/Sidebar";
import TaskForm from "@/components/tasks/TaskForm";
import { useAuth } from "@/context/auth_context";
import AIAssistantFloatingButton from "@/components/AIAssistantFloatingButton";

// Dashboard components
import HeroSummary from "@/components/dashboard/HeroSummary";
import StatsCard from "@/components/dashboard/StatsCard";
import TaskStatusChart from "@/components/dashboard/TaskStatusChart";
import PriorityChart from "@/components/dashboard/PriorityChart";
import AttentionPanel from "@/components/dashboard/AttentionPanel";
import QuickActions from "@/components/dashboard/QuickActions";
import SmartInsight, {
  generateInsight,
} from "@/components/dashboard/SmartInsight";

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

// Removed unused 'User' interface import

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showAddForm, setShowAddForm] = useState(false);
  const [formPriority, setFormPriority] = useState<
    "low" | "medium" | "high" | null
  >(null);
  const router = useRouter();
  const { user, loading: authLoading, logout } = useAuth();

  // Define fetchData here to include it in useEffect dependencies
  const fetchData = async () => {
    console.log("[DEBUG] fetchData - starting");
    try {
      // Fetch tasks
      console.log("[DEBUG] fetchData - calling /tasks");
      const tasksResponse = await apiClient.get("/tasks", {
        withCredentials: true,
        params: { sort_by: "created_at" },
      });
      console.log(
        "[DEBUG] fetchData - /tasks success, count:",
        tasksResponse.data.length,
      );
      setTasks(tasksResponse.data);
    } catch (err: unknown) {
      const error = err as {
        message?: string;
        response?: { status?: number; data?: { detail?: string } };
      };
      console.log(
        "[DEBUG] fetchData - error:",
        error.message,
        error.response?.status,
      );
      // If auth fails, redirect to login
      if (error.response?.status === 401) {
        console.log("[DEBUG] fetchData - 401 error, redirecting to login");
        router.push("/login");
        return;
      }
      setError(error.response?.data?.detail || "Failed to fetch data");
    } finally {
      console.log("[DEBUG] fetchData - setting loading to false");
      setLoading(false);
    }
  };

  useEffect(() => {
    console.log(
      "[DEBUG] Dashboard - useEffect running, authLoading:",
      authLoading,
      "user:",
      user,
    );
    // Wait for auth context to finish loading and check if user is authenticated
    if (!authLoading) {
      console.log(
        "[DEBUG] Dashboard - auth finished loading, user is:",
        user ? "authenticated" : "not authenticated",
      );
      if (!user) {
        console.log("[DEBUG] Dashboard - No user, redirecting to login");
        // User is not authenticated, redirect to login
        router.push("/login");
        return;
      }
      console.log("[DEBUG] Dashboard - User authenticated, fetching data");
      // User is authenticated, fetch dashboard data
      fetchData();
    }
    // Add fetchData to dependency array
  }, [user, authLoading, router, fetchData]);

  const handleAddTask = async (data: {
    title: string;
    description?: string;
    priority: "low" | "medium" | "high";
    tags?: string;
  }) => {
    try {
      const tagsArray = data.tags
        ? data.tags
            .split(",")
            .map((tag: string) => tag.trim())
            .filter((tag: string) => tag.length > 0)
        : [];

      const response = await apiClient.post("/tasks", {
        title: data.title,
        description: data.description || null,
        priority: data.priority,
        tags: tagsArray,
      });
      setTasks([response.data, ...tasks]);
      setShowAddForm(false);
      setFormPriority(null);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setError(error.response?.data?.detail || "Failed to add task");
      throw err;
    }
  };

  const handleLogout = () => {
    logout();
  };

  if (authLoading || loading) {
    return (
      <div className="flex min-h-screen bg-gray-50 dark:bg-gray-900">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
            className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full"
          />
        </div>
      </div>
    );
  }

  // Calculate statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter((t) => t.status === "completed").length;
  const pendingTasks = totalTasks - completedTasks;
  const highPriorityTasks = tasks.filter(
    (t) => t.priority === "high" && t.status !== "completed",
  ).length;
  const mediumPriorityTasks = tasks.filter(
    (t) => t.priority === "medium" && t.status !== "completed",
  ).length;
  const lowPriorityTasks = tasks.filter(
    (t) => t.priority === "low" && t.status !== "completed",
  ).length;

  // Get high priority and recent tasks for attention panel
  const highPriority = tasks.filter(
    (t) => t.priority === "high" && t.status !== "completed",
  );
  const recentTasks = tasks.slice(0, 5);

  // Generate smart insight\
  const insight = generateInsight(
    completedTasks,
    totalTasks,
    highPriorityTasks,
    mediumPriorityTasks,
    lowPriorityTasks,
  );

  const userName = user?.name || user?.email?.split("@")[0] || "there";

  return (
    <div className="flex min-h-screen bg-gray-50 dark:bg-gray-900">
      <Sidebar />
      <AIAssistantFloatingButton />

      <div className="flex-1 lg:ml-20 lg:w-[calc(100%-5rem)] xl:ml-64 xl:w-[calc(100%-16rem)] flex flex-col min-h-screen transition-all duration-300">
        {/* Header */}
        <header className="bg-white dark:bg-gray-800 shadow-sm sticky top-0 z-30">
          <div className="px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
            <div>
              <motion.h1
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-2xl font-bold text-gray-900 dark:text-white"
              >
                Dashboard
              </motion.h1>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Welcome back, {userName}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 transition-colors"
              >
                <LogOut size={18} />
                <span className="hidden sm:inline">Logout</span>
              </motion.button>
            </div>
          </div>
        </header>

        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
            >
              <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
            </motion.div>
          )}

          {/* Hero Summary */}
          <div className="mb-6">
            <HeroSummary
              userName={userName}
              completedTasks={completedTasks}
              totalTasks={totalTasks}
              onAddTask={() => {
                setFormPriority(null);
                setShowAddForm(true);
              }}
            />
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column - Stats and Charts */}
            <div className="lg:col-span-2 space-y-6">
              {/* Stats Cards Row */}
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <StatsCard
                  title="Total Tasks"
                  value={totalTasks}
                  icon={<ListTodo className="w-5 h-5" />}
                  color="blue"
                  delay={0}
                />
                <StatsCard
                  title="Completed"
                  value={completedTasks}
                  icon={<CheckCircle className="w-5 h-5" />}
                  color="green"
                  delay={0.1}
                />
                <StatsCard
                  title="Pending"
                  value={pendingTasks}
                  icon={<Clock className="w-5 h-5" />}
                  color="yellow"
                  delay={0.2}
                />
                <StatsCard
                  title="High Priority"
                  value={highPriorityTasks}
                  icon={<AlertCircle className="w-5 h-5" />}
                  color="red"
                  delay={0.3}
                />
              </div>

              {/* Charts Row */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <TaskStatusChart
                  completed={completedTasks}
                  pending={pendingTasks}
                />
                <PriorityChart
                  high={highPriorityTasks}
                  medium={mediumPriorityTasks}
                  low={lowPriorityTasks}
                />
              </div>

              {/* Quick Actions */}
              <QuickActions
                onAddTask={() => {
                  setFormPriority(null);
                  setShowAddForm(true);
                }}
                onAddHighPriority={() => {
                  setFormPriority("high");
                  setShowAddForm(true);
                }}
                onNavigateToTasks={() => router.push("/dashboard/tasks")}
                onAddScheduled={() => {
                  setFormPriority(null);
                  setShowAddForm(true);
                }}
              />
            </div>

            {/* Right Column - Attention Panel and Insights */}
            <div className="space-y-6">
              {/* Attention Panel */}
              <AttentionPanel
                highPriorityTasks={highPriority}
                recentTasks={recentTasks}
                onViewAll={() => router.push("/dashboard/tasks")}
              />

              {/* Smart Insight */}
              <SmartInsight
                insight={insight.insight}
                subtitle={insight.subtitle}
              />
            </div>
          </div>

          {/* View All Tasks Link */}
          {totalTasks > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 }}
              className="mt-8"
            >
              <motion.button
                whileHover={{ scale: 1.02, x: 5 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => router.push("/dashboard/tasks")}
                className="w-full flex items-center justify-between p-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-all"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                    <BarChart3 className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div className="text-left">
                    <p className="font-medium text-gray-900 dark:text-white">
                      View All Tasks
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {totalTasks} {totalTasks === 1 ? "task" : "tasks"} in your
                      list
                    </p>
                  </div>
                </div>
                <ChevronRight className="w-5 h-5 text-gray-400" />
              </motion.button>
            </motion.div>
          )}

          {/* Empty State */}
          {totalTasks === 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="mt-8 p-8 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 text-center"
            >
              <div className="max-w-md mx-auto">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full mb-4">
                  <Plus className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Start Your Productivity Journey
                </h3>
                <p className="text-gray-500 dark:text-gray-400 mb-6">
                  Create your first task and start tracking your progress. Your
                  dashboard will fill up with insights as you add more tasks.
                </p>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => {
                    setFormPriority(null);
                    setShowAddForm(true);
                  }}
                  className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
                >
                  <Plus size={20} />
                  Create Your First Task
                </motion.button>
              </div>
            </motion.div>
          )}
        </main>
      </div>

      {/* Add Task Modal */}
      {showAddForm && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          onClick={() => setShowAddForm(false)}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            onClick={(e) => e.stopPropagation()}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-xl max-w-md w-full overflow-hidden"
          >
            <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Add New Task
              </h2>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setShowAddForm(false)}
                className="text-gray-400 hover:text-gray-500 dark:text-gray-500 dark:hover:text-gray-400"
              >
                ✕
              </motion.button>
            </div>
            <div className="p-6">
              <TaskForm
                initialData={
                  formPriority ? { priority: formPriority } : undefined
                }
                onSubmit={handleAddTask}
                onCancel={() => {
                  setShowAddForm(false);
                  setFormPriority(null);
                }}
              />
            </div>
          </motion.div>
        </motion.div>
      )}
    </div>
  );
}
