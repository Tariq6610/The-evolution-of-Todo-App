"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  Plus,
  Search,
  Filter,
  ArrowUpDown,
  LayoutGrid,
  List,
  Grid,
} from "lucide-react";
import apiClient from "@/services/api_client";
import TaskForm, { TaskFormData } from "@/components/tasks/TaskForm";
import DeleteDialog from "@/components/tasks/DeleteDialog";
import { Sidebar } from "@/components/layout/Sidebar";
import { useAuth } from "@/context/auth_context";
import AIAssistantFloatingButton from "@/components/AIAssistantFloatingButton";

interface Task {
  id: string;
  title: string;
  description: string | null;
  status: string;
  priority: string;
  tags: string[];
  created_at: string;
  updated_at: string;
  isCelebrating?: boolean;
}

type ViewMode = "list" | "grid" | "compact";

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deleteTaskId, setDeleteTaskId] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterStatus, setFilterStatus] = useState<
    "ALL" | "pending" | "completed"
  >("ALL");
  const [filterPriority, setFilterPriority] = useState<
    "ALL" | "low" | "medium" | "high"
  >("ALL");
  const [sortBy, setSortBy] = useState<
    "created_at" | "updated_at" | "title" | "priority"
  >("created_at");
  const [viewMode, setViewMode] = useState<ViewMode>("list");
  const [expandedTasks, setExpandedTasks] = useState<Set<string>>(new Set());
  const router = useRouter();

  const { user, loading: authLoading } = useAuth();

  useEffect(() => {
    console.log(
      "[DEBUG] Tasks - useEffect running, authLoading:",
      authLoading,
      "user:",
      user,
    );
    // Wait for auth context to finish loading and check if user is authenticated
    if (!authLoading) {
      console.log(
        "[DEBUG] Tasks - auth finished loading, user is:",
        user ? "authenticated" : "not authenticated",
      );
      if (!user) {
        console.log("[DEBUG] Tasks - No user, redirecting to login");
        // User is not authenticated, redirect to login
        router.push("/login");
        return;
      }
      console.log("[DEBUG] Tasks - User authenticated, fetching tasks");
      // User is authenticated, fetch tasks
      fetchTasks();
    }
  }, [user, authLoading, router, fetchTasks]);

  const fetchTasks = async () => {
    try {
      const params: Record<string, string> = {};
      if (searchQuery) params.search = searchQuery;
      if (filterStatus !== "ALL") params.status_param = filterStatus;
      if (filterPriority !== "ALL") params.priority = filterPriority;
      if (sortBy !== "created_at") params.sort_by = sortBy;

      const response = await apiClient.get("/tasks", { params });
      setTasks(response.data);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setError(error.response?.data?.detail || "Failed to fetch tasks");
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskStatus = async (taskId: string) => {
    try {
      const response = await apiClient.patch(`/tasks/${taskId}/toggle-status`);

      // Add a temporary celebration effect to the completed task
      setTasks((prevTasks) =>
        prevTasks.map((task) =>
          task.id === taskId
            ? { ...task, isCelebrating: response.data.status === "completed" }
            : task,
        ),
      );

      // Update the task status after a short delay to allow for animation
      setTimeout(() => {
        setTasks((prevTasks) =>
          prevTasks.map((task) =>
            task.id === taskId
              ? { ...response.data, isCelebrating: false }
              : task,
          ),
        );
      }, 300);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setError(error.response?.data?.detail || "Failed to update task");
    }
  };

  const handleAddTask = async (data: TaskFormData) => {
    try {
      const tagsArray = data.tags
        ? data.tags
            .split(",")
            .map((tag) => tag.trim())
            .filter((tag) => tag.length > 0)
        : [];

      const response = await apiClient.post("/tasks", {
        title: data.title,
        description: data.description || null,
        priority: data.priority,
        tags: tagsArray,
      });
      setTasks([response.data, ...tasks]);
      setShowAddForm(false);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setError(error.response?.data?.detail || "Failed to add task");
      throw err;
    }
  };

  const handleEditTask = async (data: TaskFormData) => {
    if (!editingTask) return;
    try {
      const tagsArray = data.tags
        ? data.tags
            .split(",")
            .map((tag) => tag.trim())
            .filter((tag) => tag.length > 0)
        : [];

      const response = await apiClient.put(`/tasks/${editingTask.id}`, {
        title: data.title,
        description: data.description || null,
        priority: data.priority,
        tags: tagsArray,
      });
      setTasks(
        tasks.map((task) =>
          task.id === editingTask.id ? response.data : task,
        ),
      );
      setEditingTask(null);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setError(error.response?.data?.detail || "Failed to update task");
      throw err;
    }
  };

  const handleDeleteTask = async () => {
    if (!deleteTaskId) return;
    try {
      await apiClient.delete(`/tasks/${deleteTaskId}`);
      setTasks(tasks.filter((task) => task.id !== deleteTaskId));
      setDeleteTaskId(null);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setError(error.response?.data?.detail || "Failed to delete task");
    }
  };

  const openEditDialog = (task: Task) => {
    setEditingTask(task);
  };

  const openDeleteDialog = (taskId: string) => {
    setDeleteTaskId(taskId);
  };

  const toggleTaskExpanded = (taskId: string) => {
    setExpandedTasks((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(taskId)) {
        newSet.delete(taskId);
      } else {
        newSet.add(taskId);
      }
      return newSet;
    });
  };

  if (authLoading || loading) {
    return (
      <div className="flex min-h-screen bg-gray-50 dark:bg-gray-900">
        <Sidebar />
        <div className="flex-1 lg:ml-20 lg:w-[calc(100%-5rem)] xl:ml-64 xl:w-[calc(100%-16rem)] flex items-center justify-center transition-all duration-300">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
            className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full"
          />
        </div>
      </div>
    );
  }

  const taskToDelete = deleteTaskId
    ? tasks.find((task) => task.id === deleteTaskId)
    : null;

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
                Tasks
              </motion.h1>
              <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                {tasks.length} {tasks.length === 1 ? "task" : "tasks"} total
              </p>
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowAddForm(true)}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors shadow-md"
            >
              <Plus size={20} />
              Add Task
            </motion.button>
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

          {/* Add Task Form */}
          <AnimatePresence>
            {showAddForm && (
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="mb-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
              >
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
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
                <TaskForm
                  onSubmit={handleAddTask}
                  onCancel={() => setShowAddForm(false)}
                  submitLabel="Add Task"
                />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Filter Bar */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4"
          >
            <div className="flex flex-col lg:flex-row gap-4">
              {/* Search - Full width on mobile */}
              <div className="relative flex-1">
                <Search
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                  size={18}
                />
                <input
                  type="text"
                  placeholder="Search tasks..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                />
              </div>

              {/* Filters Row */}
              <div className="flex flex-wrap gap-3 items-center">
                {/* Status Filter */}
                <div className="relative">
                  <Filter
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                    size={16}
                  />
                  <select
                    value={filterStatus}
                    onChange={(e) =>
                      setFilterStatus(
                        e.target.value as "ALL" | "pending" | "completed",
                      )
                    }
                    className="pl-9 pr-8 py-2.5 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm appearance-none cursor-pointer"
                  >
                    <option value="ALL">All Status</option>
                    <option value="pending">Pending</option>
                    <option value="completed">Completed</option>
                  </select>
                </div>

                {/* Priority Filter */}
                <div className="relative">
                  <select
                    value={filterPriority}
                    onChange={(e) =>
                      setFilterPriority(
                        e.target.value as "ALL" | "low" | "medium" | "high",
                      )
                    }
                    className="pl-4 pr-8 py-2.5 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm appearance-none cursor-pointer"
                  >
                    <option value="ALL">All Priority</option>
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>
                </div>

                {/* Sort */}
                <div className="relative">
                  <ArrowUpDown
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                    size={16}
                  />
                  <select
                    value={sortBy}
                    onChange={(e) =>
                      setSortBy(
                        e.target.value as
                          | "created_at"
                          | "updated_at"
                          | "title"
                          | "priority",
                      )
                    }
                    className="pl-9 pr-8 py-2.5 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm appearance-none cursor-pointer"
                  >
                    <option value="created_at">Created Date</option>
                    <option value="updated_at">Last Updated</option>
                    <option value="title">Title</option>
                    <option value="priority">Priority</option>
                  </select>
                </div>

                {/* View Mode Toggle */}
                <div className="flex items-center gap-1 p-1 bg-gray-100 dark:bg-gray-700 rounded-lg">
                  <motion.button
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setViewMode("list")}
                    className={`p-2 rounded-md transition-colors ${viewMode === "list" ? "bg-white dark:bg-gray-600 shadow-sm" : "hover:bg-gray-200 dark:hover:bg-gray-600"}`}
                    title="List view"
                  >
                    <List
                      size={16}
                      className={viewMode === "list" ? "text-blue-600 dark:text-blue-400" : "text-gray-500"}
                    />
                  </motion.button>
                  <motion.button
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setViewMode("grid")}
                    className={`p-2 rounded-md transition-colors ${viewMode === "grid" ? "bg-white dark:bg-gray-600 shadow-sm" : "hover:bg-gray-200 dark:hover:bg-gray-600"}`}
                    title="Grid view"
                  >
                    <Grid
                      size={16}
                      className={viewMode === "grid" ? "text-blue-600 dark:text-blue-400" : "text-gray-500"}
                    />
                  </motion.button>
                  <motion.button
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setViewMode("compact")}
                    className={`p-2 rounded-md transition-colors ${viewMode === "compact" ? "bg-white dark:bg-gray-600 shadow-sm" : "hover:bg-gray-200 dark:hover:bg-gray-600"}`}
                    title="Compact view"
                  >
                    <LayoutGrid
                      size={16}
                      className={viewMode === "compact" ? "text-blue-600 dark:text-blue-400" : "text-gray-500"}
                    />
                  </motion.button>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Tasks List */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden"
          >
            <div className="px-4 py-5 sm:px-6 border-b border-gray-100 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Your Tasks
              </h2>
              <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                {tasks.length} {tasks.length === 1 ? "task" : "tasks"} found
              </p>
            </div>

            <AnimatePresence mode="popLayout">
              {tasks.length === 0 ? (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="p-12 text-center"
                >
                  <p className="text-gray-500 dark:text-gray-400">
                    No tasks found. Create your first task!
                  </p>
                </motion.div>
              ) : viewMode === "grid" ? (
                <>
                  {/* Desktop view - 3 separate flex columns */}
                  <div className="hidden sm:flex sm:flex-row sm:gap-4 p-4">
                    {/* Column 1 */}
                    <div className="flex-1 flex flex-col gap-4 min-w-0">
                      {tasks
                        .filter((_, idx) => idx % 3 === 0)
                        .map((task, index) => (
                          <TaskCard
                            key={task.id}
                            task={task}
                            index={index}
                            viewMode={viewMode}
                            onToggle={() => toggleTaskStatus(task.id)}
                            onEdit={() => openEditDialog(task)}
                            onDelete={() => openDeleteDialog(task.id)}
                            expandedTasks={expandedTasks}
                            toggleTaskExpanded={toggleTaskExpanded}
                          />
                        ))}
                    </div>

                    {/* Column 2 */}
                    <div className="flex-1 flex flex-col gap-4 min-w-0">
                      {tasks
                        .filter((_, idx) => idx % 3 === 1)
                        .map((task, index) => (
                          <TaskCard
                            key={task.id}
                            task={task}
                            index={index}
                            viewMode={viewMode}
                            onToggle={() => toggleTaskStatus(task.id)}
                            onEdit={() => openEditDialog(task)}
                            onDelete={() => openDeleteDialog(task.id)}
                            expandedTasks={expandedTasks}
                            toggleTaskExpanded={toggleTaskExpanded}
                          />
                        ))}
                    </div>

                    {/* Column 3 */}
                    <div className="flex-1 flex flex-col gap-4 min-w-0">
                      {tasks
                        .filter((_, idx) => idx % 3 === 2)
                        .map((task, index) => (
                          <TaskCard
                            key={task.id}
                            task={task}
                            index={index}
                            viewMode={viewMode}
                            onToggle={() => toggleTaskStatus(task.id)}
                            onEdit={() => openEditDialog(task)}
                            onDelete={() => openDeleteDialog(task.id)}
                            expandedTasks={expandedTasks}
                            toggleTaskExpanded={toggleTaskExpanded}
                          />
                        ))}
                    </div>
                  </div>

                  {/* Mobile view for grid mode - stack all tasks vertically */}
                  <div className="sm:hidden flex flex-col gap-4 p-4">
                    {tasks.map((task, index) => (
                      <TaskCard
                        key={task.id}
                        task={task}
                        index={index}
                        viewMode={viewMode}
                        onToggle={() => toggleTaskStatus(task.id)}
                        onEdit={() => openEditDialog(task)}
                        onDelete={() => openDeleteDialog(task.id)}
                        expandedTasks={expandedTasks}
                        toggleTaskExpanded={toggleTaskExpanded}
                      />
                    ))}
                  </div>
                </>
              ) : (
                <div className="flex flex-col gap-4 p-4">
                  {tasks.map((task, index) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      index={index}
                      viewMode={viewMode}
                      onToggle={() => toggleTaskStatus(task.id)}
                      onEdit={() => openEditDialog(task)}
                      onDelete={() => openDeleteDialog(task.id)}
                      expandedTasks={expandedTasks}
                      toggleTaskExpanded={toggleTaskExpanded}
                    />
                  ))}
                </div>
              )}
            </AnimatePresence>
          </motion.div>
        </main>
      </div>

      {/* Edit Task Modal */}
      <AnimatePresence>
        {editingTask && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
            onClick={() => setEditingTask(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-xl max-w-md w-full overflow-hidden"
            >
              <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-700">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Edit Task
                </h2>
              </div>
              <div className="p-6">
                <TaskForm
                  initialData={{
                    title: editingTask.title,
                    description: editingTask.description || "",
                    priority: editingTask.priority as "low" | "medium" | "high",
                    tags: editingTask.tags?.join(", "),
                  }}
                  onSubmit={handleEditTask}
                  onCancel={() => setEditingTask(null)}
                  submitLabel="Save Changes"
                />
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Delete Confirmation Dialog */}
      <DeleteDialog
        isOpen={deleteTaskId !== null}
        taskTitle={taskToDelete?.title || ""}
        onConfirm={handleDeleteTask}
        onCancel={() => setDeleteTaskId(null)}
      />
    </div>
  );
}
