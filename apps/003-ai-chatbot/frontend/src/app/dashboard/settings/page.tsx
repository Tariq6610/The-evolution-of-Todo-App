"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  User,
  Bell,
  Moon,
  Shield,
  HelpCircle,
  LogOut,
  Save,
} from "lucide-react";
import { Sidebar } from "@/components/layout/Sidebar";
import { useAuth } from "@/context/auth_context";
import AIAssistantFloatingButton from "@/components/AIAssistantFloatingButton";

export default function SettingsPage() {
  const router = useRouter();
  const { user, loading: authLoading, logout } = useAuth();
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [notifications, setNotifications] = useState(true);
  const [emailUpdates, setEmailUpdates] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState("");

  // Form state
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    console.log(
      "[DEBUG] Settings - useEffect running, authLoading:",
      authLoading,
      "user:",
      user,
    );
    // Wait for auth context to finish loading and check if user is authenticated
    if (!authLoading) {
      console.log(
        "[DEBUG] Settings - auth finished loading, user is:",
        user ? "authenticated" : "not authenticated",
      );
      if (!user) {
        console.log("[DEBUG] Settings - No user, redirecting to login");
        // User is not authenticated, redirect to login
        router.push("/login");
        return;
      }
      console.log(
        "[DEBUG] Settings - User authenticated, initializing settings data:",
        user,
      );
      // User is authenticated, initialize settings data
      // Use setTimeout to avoid calling setState directly within an effect
      setTimeout(() => {
        setName(user.name || user.email?.split("@")[0] || "");
        setEmail(user.email || "");
      }, 0);
    }

    // Load theme preference
    const theme = localStorage.getItem("theme");
    // Use setTimeout to avoid calling setState directly within an effect
    setTimeout(() => {
      setIsDarkMode(theme === "dark");
    }, 0);
  }, [user, authLoading, router]);

  const toggleTheme = () => {
    const newTheme = !isDarkMode ? "dark" : "light";
    setIsDarkMode(!isDarkMode);
    localStorage.setItem("theme", newTheme);
    document.documentElement.classList.toggle("dark", newTheme === "dark");
  };

  const handleSaveProfile = async () => {
    setIsSaving(true);
    setSaveMessage("");

    // Simulate saving - in real app, this would call API
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Save user data to localStorage
    const userData = { name, email };
    localStorage.setItem("user_data", JSON.stringify(userData));

    setIsSaving(false);
    setSaveMessage("Profile saved successfully!");
    setTimeout(() => setSaveMessage(""), 3000);
  };

  const handleLogout = async () => {
    await logout();
  };

  const handlePasswordChange = () => {
    setSaveMessage("Password change feature coming soon!");
    setTimeout(() => setSaveMessage(""), 3000);
  };

  if (authLoading) {
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

  return (
    <div className="flex min-h-screen bg-gray-50 dark:bg-gray-900">
      <Sidebar />

      <div className="flex-1 lg:ml-20 lg:w-[calc(100%-5rem)] xl:ml-64 xl:w-[calc(100%-16rem)] flex flex-col min-h-screen transition-all duration-300">
        {/* Header */}
        <header className="bg-white dark:bg-gray-800 shadow-sm sticky top-0 z-30">
          <div className="px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
            <motion.h1
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-2xl font-bold text-gray-900 dark:text-white"
            >
              Settings
            </motion.h1>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleLogout}
              className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors"
            >
              <LogOut size={18} />
              Logout
            </motion.button>
          </div>
        </header>

        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Save Message */}
            {saveMessage && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg"
              >
                <p className="text-sm text-green-600 dark:text-green-400">
                  {saveMessage}
                </p>
              </motion.div>
            )}

            {/* Profile Section */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden"
            >
              <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <User className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Profile
                </h2>
              </div>

              <div className="divide-y divide-gray-100 dark:divide-gray-700">
                {/* Display Name */}
                <div className="px-6 py-4 flex items-center justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      Display Name
                    </p>
                  </div>
                  <div className="ml-4">
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="Enter your name"
                      className="px-4 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent w-64"
                    />
                  </div>
                </div>

                {/* Email */}
                <div className="px-6 py-4 flex items-center justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      Email Address
                    </p>
                  </div>
                  <div className="ml-4">
                    <input
                      type="email"
                      value={email}
                      placeholder="Enter your email"
                      disabled
                      className="px-4 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed w-64"
                    />
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Appearance Section */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden"
            >
              <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <Moon className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Appearance
                </h2>
              </div>

              <div className="divide-y divide-gray-100 dark:divide-gray-700">
                <div className="px-6 py-4 flex items-center justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      Dark Mode
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
                      Use dark theme for the interface
                    </p>
                  </div>
                  <div className="ml-4">
                    <button
                      onClick={toggleTheme}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                        isDarkMode
                          ? "bg-blue-600"
                          : "bg-gray-200 dark:bg-gray-700"
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          isDarkMode ? "translate-x-6" : "translate-x-1"
                        }`}
                      />
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Notifications Section */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden"
            >
              <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <Bell className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Notifications
                </h2>
              </div>

              <div className="divide-y divide-gray-100 dark:divide-gray-700">
                <div className="px-6 py-4 flex items-center justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      Push Notifications
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
                      Receive notifications for task updates
                    </p>
                  </div>
                  <div className="ml-4">
                    <button
                      onClick={() => setNotifications(!notifications)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                        notifications
                          ? "bg-blue-600"
                          : "bg-gray-200 dark:bg-gray-700"
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          notifications ? "translate-x-6" : "translate-x-1"
                        }`}
                      />
                    </button>
                  </div>
                </div>

                <div className="px-6 py-4 flex items-center justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      Email Updates
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
                      Receive weekly task summary emails
                    </p>
                  </div>
                  <div className="ml-4">
                    <button
                      onClick={() => setEmailUpdates(!emailUpdates)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                        emailUpdates
                          ? "bg-blue-600"
                          : "bg-gray-200 dark:bg-gray-700"
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          emailUpdates ? "translate-x-6" : "translate-x-1"
                        }`}
                      />
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Security Section */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden"
            >
              <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <Shield className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Security
                </h2>
              </div>

              <div className="divide-y divide-gray-100 dark:divide-gray-700">
                <div className="px-6 py-4 flex items-center justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      Change Password
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
                      Update your account password
                    </p>
                  </div>
                  <div className="ml-4">
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={handlePasswordChange}
                      className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
                    >
                      Update
                    </motion.button>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Save Button for Profile Section */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="flex justify-end"
            >
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleSaveProfile}
                disabled={isSaving}
                className="inline-flex items-center gap-2 px-6 py-3 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSaving ? (
                  <>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{
                        repeat: Infinity,
                        duration: 1,
                        ease: "linear",
                      }}
                      className="w-4 h-4 border-2 border-white border-t-transparent rounded-full"
                    />
                    Saving...
                  </>
                ) : (
                  <>
                    <Save size={18} />
                    Save Changes
                  </>
                )}
              </motion.button>
            </motion.div>

            {/* Help Section */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6"
            >
              <div className="flex items-center gap-3 mb-4">
                <HelpCircle className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Need Help?
                </h2>
              </div>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                If you have any questions or need assistance, please don&apos;t
                hesitate to reach out.
              </p>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="px-4 py-2 text-sm font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 hover:bg-blue-100 dark:hover:bg-blue-900/30 rounded-lg transition-colors"
              >
                Contact Support
              </motion.button>
            </motion.div>
          </div>
        </main>
      </div>
    </div>
  );
}
