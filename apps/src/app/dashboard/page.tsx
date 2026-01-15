'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '@/services/api_client';
import TaskForm, { TaskFormData } from '@/components/tasks/TaskForm';
import DeleteDialog from '@/components/tasks/DeleteDialog';

interface Task {
  id: string;
  title: string;
  description: string | null;
  status: string; // PENDING or COMPLETED
  priority: string; // LOW, MEDIUM, HIGH
  tags: string[];
  created_at: string;
  updated_at: string;
}

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deleteTaskId, setDeleteTaskId] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState<'ALL' | 'PENDING' | 'COMPLETED'>('ALL');
  const [filterPriority, setFilterPriority] = useState<'ALL' | 'LOW' | 'MEDIUM' | 'HIGH'>('ALL');
  const [sortBy, setSortBy] = useState<'created_at' | 'updated_at' | 'title' | 'priority'>('created_at');
  const router = useRouter();

  // Check if user is authenticated
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      router.push('/login');
      return;
    }
    fetchTasks();
  }, [searchQuery, filterStatus, filterPriority, sortBy]);

  const fetchTasks = async () => {
    try {
      const params: Record<string, string> = {};
      if (searchQuery) params.search = searchQuery;
      if (filterStatus !== 'ALL') params.status = filterStatus;
      if (filterPriority !== 'ALL') params.priority = filterPriority;
      if (sortBy !== 'created_at') params.sort_by = sortBy;

      const response = await apiClient.get('/tasks', params);
      setTasks(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskStatus = async (taskId: string) => {
    try {
      const response = await apiClient.patch(`/tasks/${taskId}/toggle-status`);
      setTasks(tasks.map(task =>
        task.id === taskId ? response.data : task
      ));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update task');
    }
  };

  const handleAddTask = async (data: TaskFormData) => {
    try {
      const response = await apiClient.post('/tasks', data);
      setTasks([...tasks, response.data]);
      setShowAddForm(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to add task');
      throw err;
    }
  };

  const handleEditTask = async (data: TaskFormData) => {
    if (!editingTask) return;
    try {
      const response = await apiClient.patch(`/tasks/${editingTask.id}`, data);
      setTasks(tasks.map(task =>
        task.id === editingTask.id ? response.data : task
      ));
      setEditingTask(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update task');
      throw err;
    }
  };

  const handleDeleteTask = async () => {
    if (!deleteTaskId) return;
    try {
      await apiClient.delete(`/tasks/${deleteTaskId}`);
      setTasks(tasks.filter(task => task.id !== deleteTaskId));
      setDeleteTaskId(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete task');
    }
  };

  const openEditDialog = (task: Task) => {
    setEditingTask(task);
  };

  const openDeleteDialog = (taskId: string) => {
    setDeleteTaskId(taskId);
  };

  const getTaskById = (taskId: string) => {
    return tasks.find(task => task.id === taskId);
  };

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    router.push('/login');
  };

  if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;

  const taskToDelete = deleteTaskId ? getTaskById(deleteTaskId) : null;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Todo Dashboard</h1>
          <button
            onClick={handleLogout}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Logout
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-700">{error}</div>
          </div>
        )}

        {showAddForm && (
          <div className="mb-8 bg-white shadow rounded-lg p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-800">Add New Task</h2>
              <button
                onClick={() => setShowAddForm(false)}
                className="text-gray-400 hover:text-gray-500"
              >
                ✕
              </button>
            </div>
            <TaskForm onSubmit={handleAddTask} onCancel={() => setShowAddForm(false)} />
          </div>
        )}

        {!showAddForm && (
          <div className="mb-4">
            <button
              onClick={() => setShowAddForm(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              + Add New Task
            </button>
          </div>
        )}

        {/* Filter Bar */}
        <div className="mb-8 bg-white shadow rounded-lg p-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
                Search
              </label>
              <input
                type="text"
                id="search"
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                id="status"
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value as 'ALL' | 'PENDING' | 'COMPLETED')}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value="ALL">All</option>
                <option value="PENDING">Pending</option>
                <option value="COMPLETED">Completed</option>
              </select>
            </div>

            <div>
              <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
                Priority
              </label>
              <select
                id="priority"
                value={filterPriority}
                onChange={(e) => setFilterPriority(e.target.value as 'ALL' | 'LOW' | 'MEDIUM' | 'HIGH')}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value="ALL">All</option>
                <option value="HIGH">High</option>
                <option value="MEDIUM">Medium</option>
                <option value="LOW">Low</option>
              </select>
            </div>

            <div>
              <label htmlFor="sort" className="block text-sm font-medium text-gray-700 mb-1">
                Sort By
              </label>
              <select
                id="sort"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as 'created_at' | 'updated_at' | 'title' | 'priority')}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value="created_at">Created Date</option>
                <option value="updated_at">Last Updated</option>
                <option value="title">Title</option>
                <option value="priority">Priority</option>
              </select>
            </div>
          </div>
        </div>

        {!showAddForm && (
          <div className="mb-4">
            <button
              onClick={() => setShowAddForm(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              + Add New Task
            </button>
          </div>
        )}

        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6">
            <h2 className="text-xl font-semibold text-gray-800">Your Tasks</h2>
          </div>
          <div className="border-t border-gray-200 px-4 py-5 sm:p-0">
            {tasks.length === 0 ? (
              <div className="p-6 text-center">
                <p className="text-gray-500">No tasks yet. Click &quot;Add New Task&quot; to create your first task!</p>
              </div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {tasks.map((task) => (
                  <li key={task.id} className="py-4 sm:py-5 sm:px-6">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start flex-1">
                        <input
                          type="checkbox"
                          checked={task.status === 'COMPLETED'}
                          onChange={() => toggleTaskStatus(task.id)}
                          className="mt-1 h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                        />
                        <div className="ml-3 flex-1">
                          <p className={`text-sm font-medium ${task.status === 'COMPLETED' ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                            {task.title}
                          </p>
                          {task.description && (
                            <p className="text-sm text-gray-500 mt-1">{task.description}</p>
                          )}
                          <div className="mt-1 flex items-center space-x-2">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                              task.priority === 'HIGH' ? 'bg-red-100 text-red-800' :
                              task.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-green-100 text-green-800'
                            }`}>
                              {task.priority}
                            </span>
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                              task.status === 'COMPLETED' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
                            }`}>
                              {task.status}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="flex space-x-2 ml-4">
                        <button
                          onClick={() => openEditDialog(task)}
                          className="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => openDeleteDialog(task.id)}
                          className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </main>

      {/* Edit Task Modal */}
      {editingTask && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div className="px-4 py-5 sm:p-6">
              <h2 className="text-lg leading-6 font-medium text-gray-900 mb-4">Edit Task</h2>
              <TaskForm
                initialData={{
                  title: editingTask.title,
                  description: editingTask.description || '',
                  priority: editingTask.priority as 'LOW' | 'MEDIUM' | 'HIGH',
                  tags: editingTask.tags?.join(', '),
                }}
                onSubmit={handleEditTask}
                onCancel={() => setEditingTask(null)}
                submitLabel="Save Changes"
              />
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Dialog */}
      <DeleteDialog
        isOpen={deleteTaskId !== null}
        taskTitle={taskToDelete?.title || ''}
        onConfirm={handleDeleteTask}
        onCancel={() => setDeleteTaskId(null)}
      />
    </div>
  );
}