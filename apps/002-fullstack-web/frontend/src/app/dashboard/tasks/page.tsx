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
  Edit2,
  Trash2,
  LogOut,
  ChevronDown,
} from "lucide-react";
import apiClient from "@/services/api_client";
import TaskForm, { TaskFormData } from "@/components/tasks/TaskForm";
import DeleteDialog from "@/components/tasks/DeleteDialog";
import { Sidebar } from "@/components/layout/Sidebar";
import { useAuth } from "@/context/auth_context";

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
  }, [user, authLoading, searchQuery, filterStatus, filterPriority, sortBy]);

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
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
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
                    className={`p-2 rounded-md transition-colors ${
                      viewMode === "list"
                        ? "bg-white dark:bg-gray-600 shadow-sm"
                        : "hover:bg-gray-200 dark:hover:bg-gray-600"
                    }`}
                    title="List view"
                  >
                    <List
                      size={16}
                      className={
                        viewMode === "list"
                          ? "text-blue-600 dark:text-blue-400"
                          : "text-gray-500"
                      }
                    />
                  </motion.button>
                  <motion.button
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setViewMode("grid")}
                    className={`p-2 rounded-md transition-colors ${
                      viewMode === "grid"
                        ? "bg-white dark:bg-gray-600 shadow-sm"
                        : "hover:bg-gray-200 dark:hover:bg-gray-600"
                    }`}
                    title="Grid view"
                  >
                    <Grid
                      size={16}
                      className={
                        viewMode === "grid"
                          ? "text-blue-600 dark:text-blue-400"
                          : "text-gray-500"
                      }
                    />
                  </motion.button>
                  <motion.button
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setViewMode("compact")}
                    className={`p-2 rounded-md transition-colors ${
                      viewMode === "compact"
                        ? "bg-white dark:bg-gray-600 shadow-sm"
                        : "hover:bg-gray-200 dark:hover:bg-gray-600"
                    }`}
                    title="Compact view"
                  >
                    <LayoutGrid
                      size={16}
                      className={
                        viewMode === "compact"
                          ? "text-blue-600 dark:text-blue-400"
                          : "text-gray-500"
                      }
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

// Task Card Component
function TaskCard({
  task,
  index,
  viewMode,
  onToggle,
  onEdit,
  onDelete,
  expandedTasks,
  toggleTaskExpanded,
}: {
  task: Task;
  index: number;
  viewMode: ViewMode;
  onToggle: () => void;
  onEdit: () => void;
  onDelete: () => void;
  expandedTasks: Set<string>;
  toggleTaskExpanded: (taskId: string) => void;
}) {
  const isCompact = viewMode === "compact";

  if (viewMode === "grid") {
    return (
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{
          opacity: 1,
          y: 0,
          scale: task.isCelebrating ? [1, 1.05, 1] : 1,
        }}
        transition={{
          scale: {
            duration: 0.3,
            times: [0, 0.5, 1],
          },
        }}
        className={`bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-4 hover:shadow-md transition-all group cursor-pointer`}
        onClick={() => toggleTaskExpanded(task.id)}
        style={{ contain: "layout" }}
      >
        <div className="flex items-start gap-3">
          {/* Status Indicator - prevent bubbling to avoid double toggle */}
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={(e) => {
              e.stopPropagation();
              onToggle();
            }}
            className={`mt-1 flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-full border-2 transition-all ${
              task.status === "completed"
                ? "bg-green-500 border-green-500 dark:border-green-500"
                : "border-gray-300 dark:border-gray-600 hover:border-green-500 hover:bg-gray-50 dark:hover:bg-gray-700"
            }`}
            aria-label={`Mark ${task.title} as ${task.status === "completed" ? "pending" : "completed"}`}
          >
            {task.status === "completed" && (
              <motion.svg
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.2 }}
                className="w-4 h-4 text-white"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth={3}
              >
                <motion.path
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: 0.3, ease: "easeInOut" }}
                  d="M5 13l4 4L19 7"
                />
              </motion.svg>
            )}
          </motion.button>

          <div className="flex-1 min-w-0">
            <div
              className={`text-sm font-medium ${
                task.status === "completed"
                  ? "line-through text-gray-500 dark:text-gray-500"
                  : "text-gray-900 dark:text-white"
              }`}
            >
              {task.title}
            </div>

            {/* Collapsed view - only tags */}
            <div className="mt-2 flex items-center gap-2 flex-wrap">
              {/* Priority Badge */}
              <span
                className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  task.priority === "high"
                    ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400"
                    : task.priority === "medium"
                      ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400"
                      : "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
                }`}
              >
                {task.priority.toUpperCase()}
              </span>

              {/* Tags */}
              {task.tags.slice(0, 2).map((tag) => (
                <span
                  key={tag}
                  className="inline-flex items-center px-2 py-0.5 rounded text-xs bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400"
                >
                  #{tag}
                </span>
              ))}
              {task.tags.length > 2 && (
                <span className="text-xs text-gray-400">
                  +{task.tags.length - 2}
                </span>
              )}
            </div>

            <AnimatePresence>
              {expandedTasks.has(task.id) && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3, ease: "easeInOut" }}
                  className="pt-3 mt-3 border-t border-gray-100 dark:border-gray-700 overflow-hidden"
                >
                  {task.description && (
                    <p
                      className={`text-sm mb-3 ${
                        task.status === "completed"
                          ? "text-gray-400 dark:text-gray-500"
                          : "text-gray-500 dark:text-gray-400"
                      }`}
                    >
                      {task.description}
                    </p>
                  )}

                  <div className="text-xs text-gray-500 dark:text-gray-400 space-y-1">
                    <div>
                      Created: {new Date(task.created_at).toLocaleDateString()}
                    </div>
                    {task.status === "completed" && task.updated_at && (
                      <div>
                        Completed:{" "}
                        {new Date(task.updated_at).toLocaleDateString()}
                      </div>
                    )}
                  </div>

                  <div className="flex items-center gap-2 mt-3">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onEdit();
                      }}
                      className="px-2 py-1 text-xs font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded transition-colors"
                    >
                      Edit
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDelete();
                      }}
                      className="px-2 py-1 text-xs font-medium text-white bg-red-600 hover:bg-red-700 rounded transition-colors"
                    >
                      Delete
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </motion.div>
    );
  }

  // List view (default)
  return (
    <motion.li
      key={task.id}
      initial={{ opacity: 0, y: 20 }}
      animate={{
        opacity: 1,
        y: 0,
        scale: task.isCelebrating ? [1, 1.05, 1] : 1,
      }}
      exit={{ opacity: 0, x: -100 }}
      transition={{
        delay: index * 0.05,
        scale: {
          duration: 0.3,
          times: [0, 0.5, 1],
        },
      }}
      className={`group ${task.status === "completed" ? "opacity-70" : ""}`}
    >
      <div
        className={`${isCompact ? "p-3" : "px-4 py-4 sm:px-6"} hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors border-l-4 cursor-pointer ${
          task.status === "completed"
            ? "border-green-500 bg-green-50/30 dark:bg-green-900/10"
            : task.priority === "high"
              ? "border-red-500"
              : task.priority === "medium"
                ? "border-yellow-500"
                : "border-gray-300 dark:border-gray-600"
        }`}
        onClick={() => toggleTaskExpanded(task.id)}
      >
        <div className="flex items-start gap-3 sm:gap-4">
          {/* Status Indicator - prevent bubbling to avoid double toggle */}
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={(e) => {
              e.stopPropagation();
              onToggle();
            }}
            className={`mt-1 flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-full border-2 transition-all ${
              task.status === "completed"
                ? "bg-green-500 border-green-500 dark:border-green-500"
                : "border-gray-300 dark:border-gray-600 hover:border-green-500 hover:bg-gray-50 dark:hover:bg-gray-700"
            }`}
            aria-label={`Mark ${task.title} as ${task.status === "completed" ? "pending" : "completed"}`}
          >
            {task.status === "completed" && (
              <motion.svg
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.2 }}
                className="w-4 h-4 text-white"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth={3}
              >
                <motion.path
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: 0.3, ease: "easeInOut" }}
                  d="M5 13l4 4L19 7"
                />
              </motion.svg>
            )}
          </motion.button>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <div
              className={`text-sm font-medium ${
                task.status === "completed"
                  ? "line-through text-gray-500 dark:text-gray-500"
                  : "text-gray-900 dark:text-white"
              }`}
            >
              {task.title}
            </div>

            {/* Collapsed view - only tags */}
            <div className="mt-2 flex items-center gap-2 flex-wrap">
              {/* Priority Badge */}
              <span
                className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  task.priority === "high"
                    ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400"
                    : task.priority === "medium"
                      ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400"
                      : "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
                }`}
              >
                {task.priority.toUpperCase()}
              </span>

              {/* Tags */}
              {task.tags.slice(0, 2).map((tag) => (
                <span
                  key={tag}
                  className="inline-flex items-center px-2 py-0.5 rounded text-xs bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400"
                >
                  #{tag}
                </span>
              ))}
              {task.tags.length > 2 && (
                <span className="text-xs text-gray-400">
                  +{task.tags.length - 2}
                </span>
              )}
            </div>

            <AnimatePresence>
              {expandedTasks.has(task.id) && !isCompact && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3, ease: "easeInOut" }}
                  className="pt-3 mt-3 border-t border-gray-100 dark:border-gray-700 overflow-hidden relative z-10"
                >
                  {task.description && (
                    <p
                      className={`text-sm mb-3 ${
                        task.status === "completed"
                          ? "text-gray-400 dark:text-gray-500"
                          : "text-gray-500 dark:text-gray-400"
                      }`}
                    >
                      {task.description}
                    </p>
                  )}

                  <div className="text-xs text-gray-500 dark:text-gray-400 space-y-1">
                    <div>
                      Created: {new Date(task.created_at).toLocaleDateString()}
                    </div>
                    {task.status === "completed" && task.updated_at && (
                      <div>
                        Completed:{" "}
                        {new Date(task.updated_at).toLocaleDateString()}
                      </div>
                    )}
                  </div>

                  <div className="flex items-center gap-2 mt-3">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onEdit();
                      }}
                      className="px-2 py-1 text-xs font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded transition-colors"
                    >
                      Edit
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDelete();
                      }}
                      className="px-2 py-1 text-xs font-medium text-white bg-red-600 hover:bg-red-700 rounded transition-colors"
                    >
                      Delete
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </motion.li>
  );
}
