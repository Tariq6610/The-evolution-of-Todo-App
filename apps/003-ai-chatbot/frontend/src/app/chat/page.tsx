"use client";

import { useState, useRef, useEffect } from "react";
import { useAuth } from "@/context/auth_context";
import { useRouter } from "next/navigation";

export default function ChatPage() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<
    { id: string; role: string; content: string; timestamp: Date }[]
  >([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Redirect if not authenticated
  useEffect(() => {
    if (!user && !loading) {
      router.push("/login");
    }
  }, [user, loading, router]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    // Add user message to UI immediately
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // Call backend chat API - use user ID from auth context
      const response = await fetch(`/api/v1/chat/${user?.id || user?.email}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // For this app, we might rely on cookies for auth instead of Bearer tokens
          // The backend should handle authentication based on session cookies
        },
        body: JSON.stringify({ message: input }),
        credentials: "include", // Include cookies in the request
      });

      if (!response.ok) {
        throw new Error(`Chat API error: ${response.status}`);
      }

      const data = await response.json();

      const assistantMessage = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: data.response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error sending message:", error);

      const errorMessage = {
        id: `error-${Date.now()}`,
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again.",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        Loading...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Todo AI Assistant
        </h1>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          {/* Messages container */}
          <div className="h-[60vh] overflow-y-auto p-4 space-y-4">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-gray-500">
                <p className="text-lg">Welcome to the Todo AI Assistant!</p>
                <p className="mt-2">Ask me to help you manage your tasks:</p>
                <ul className="mt-2 text-left list-disc pl-5 space-y-1">
                  <li>Create new tasks</li>
                  <li>Check your task list</li>
                  <li>Mark tasks as complete</li>
                  <li>Update or delete tasks</li>
                </ul>
              </div>
            ) : (
              messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-4 ${
                      msg.role === "user"
                        ? "bg-blue-500 text-white"
                        : "bg-gray-200 text-gray-800"
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{msg.content}</div>
                    <div
                      className={`text-xs mt-1 ${msg.role === "user" ? "text-blue-100" : "text-gray-500"}`}
                    >
                      {msg.timestamp.toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </div>
                  </div>
                </div>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input form */}
          <form onSubmit={handleSubmit} className="border-t p-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask me to help with your tasks..."
                className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="bg-blue-500 text-white rounded-lg px-6 py-2 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {isLoading ? "Sending..." : "Send"}
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2">
              Example: &quot;Add a task to buy groceries&quot; or &quot;Show me
              my tasks&quot;
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
