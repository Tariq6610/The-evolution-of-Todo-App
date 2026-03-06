"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { User, Mail, Calendar, Edit2, Save, X, Camera } from "lucide-react";
import { Sidebar } from "@/components/layout/Sidebar";
import { useAuth } from "@/context/auth_context";

export default function ProfilePage() {
  const router = useRouter();
  const { user, loading: authLoading, logout } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState("");

  // Form state
  const [name, setName] = useState("");
  const [bio, setBio] = useState("");
  const [originalName, setOriginalName] = useState("");
  const [originalBio, setOriginalBio] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    console.log(
      "[DEBUG] Profile - useEffect running, authLoading:",
      authLoading,
      "user:",
      user,
    );
    // Wait for auth context to finish loading and check if user is authenticated
    if (!authLoading) {
      console.log(
        "[DEBUG] Profile - auth finished loading, user is:",
        user ? "authenticated" : "not authenticated",
      );
      if (!user) {
        console.log("[DEBUG] Profile - No user, redirecting to login");
        // User is not authenticated, redirect to login
        router.push("/login");
        return;
      }
      console.log(
        "[DEBUG] Profile - User authenticated, initializing profile data:",
        user,
      );
      // User is authenticated, initialize profile data
      // Use setTimeout to avoid calling setState directly within an effect
      setTimeout(() => {
        setName(user.name || user.email?.split("@")[0] || "");
        setEmail(user.email || "");
        setOriginalName(user.name || user.email?.split("@")[0] || "");
        // Initialize bio if it exists in user object or from localStorage
        const bioFromUser = user.bio || "";
        setBio(bioFromUser);
        setOriginalBio(bioFromUser);
      }, 0);
    }
  }, [user, authLoading, router]);

  const handleCancel = () => {
    setName(originalName);
    setBio(originalBio);
    setIsEditing(false);
  };

  const handleSaveProfile = async () => {
    setIsSaving(true);
    setSaveMessage("");

    // Simulate saving - in real app, this would call API
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Save user data to localStorage
    const userData = { name, bio, email };
    localStorage.setItem("user_data", JSON.stringify(userData));

    setOriginalName(name);
    setOriginalBio(bio);
    setIsSaving(false);
    setIsEditing(false);
    setSaveMessage("Profile updated successfully!");
    setTimeout(() => setSaveMessage(""), 3000);
  };

  const handleLogout = async () => {
    await logout();
  };

  const memberSince = "January 2025";

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
              Profile
            </motion.h1>
            {!isEditing && (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setIsEditing(true)}
                className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
              >
                <Edit2 size={18} />
                Edit Profile
              </motion.button>
            )}
          </div>
        </header>

        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Save Message */}
            {saveMessage && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-6 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg"
              >
                <p className="text-sm text-green-600 dark:text-green-400">
                  {saveMessage}
                </p>
              </motion.div>
            )}

            {/* Profile Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden"
            >
              {/* Cover / Avatar Header */}
              <div className="h-32 bg-gradient-to-r from-blue-500 to-purple-600 relative">
                <div className="absolute -bottom-12 left-6">
                  <div className="relative">
                    <div className="w-24 h-24 rounded-full bg-white dark:bg-gray-800 p-1 shadow-lg">
                      <div className="w-full h-full rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                        <User className="w-12 h-12 text-white" />
                      </div>
                    </div>
                    {isEditing && (
                      <button className="absolute bottom-0 right-0 p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg transition-colors">
                        <Camera size={14} />
                      </button>
                    )}
                  </div>
                </div>
              </div>

              {/* Profile Info */}
              <div className="pt-16 px-6 pb-6">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    {isEditing ? (
                      <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className="px-4 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-xl font-bold"
                        placeholder="Your name"
                      />
                    ) : (
                      <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                        {name || "Your Name"}
                      </h2>
                    )}
                    <div className="flex items-center gap-2 mt-1 text-gray-500 dark:text-gray-400">
                      <Mail size={14} />
                      <span className="text-sm">{email}</span>
                    </div>
                  </div>

                  {isEditing && (
                    <div className="flex gap-2">
                      <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={handleCancel}
                        className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
                      >
                        <X size={18} />
                        Cancel
                      </motion.button>
                      <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={handleSaveProfile}
                        disabled={isSaving}
                        className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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
                    </div>
                  )}
                </div>

                {/* Bio Section */}
                <div className="border-t border-gray-100 dark:border-gray-700 pt-6">
                  <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-3">
                    About
                  </h3>
                  {isEditing ? (
                    <textarea
                      value={bio}
                      onChange={(e) => setBio(e.target.value)}
                      rows={4}
                      className="w-full px-4 py-3 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                      placeholder="Tell us about yourself..."
                    />
                  ) : (
                    <p className="text-gray-600 dark:text-gray-300">
                      {bio || "No bio added yet. Click Edit Profile to add one."}
                    </p>
                  )}
                </div>
              </div>
            </motion.div>

            {/* Account Info */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden"
            >
              <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex items-center gap-3">
                <User className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Account Information
                </h2>
              </div>

              <div className="divide-y divide-gray-100 dark:divide-gray-700">
                {/* Member Since */}
                <div className="px-6 py-4 flex items-center justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      Member Since
                    </p>
                  </div>
                  <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400">
                    <Calendar size={16} />
                    <span className="text-sm">{memberSince}</span>
                  </div>
                </div>

                {/* Account Status */}
                <div className="px-6 py-4 flex items-center justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      Account Status
                    </p>
                  </div>
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">
                    Active
                  </span>
                </div>
              </div>
            </motion.div>

            {/* Logout Button */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="flex justify-end"
            >
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleLogout}
                className="inline-flex items-center gap-2 px-6 py-3 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors"
              >
                Logout
              </motion.button>
            </motion.div>
          </div>
        </main>
      </div>
    </div>
  );
}
