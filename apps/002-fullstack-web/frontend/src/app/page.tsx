import Link from "next/link";
import { CheckCircle2 } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center space-y-8 pt-20 text-center">
      <div className="flex items-center space-x-3 text-indigo-600">
        <CheckCircle2 size={48} />
        <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl">
          Todo App
        </h1>
      </div>

      <p className="max-w-2xl text-xl text-gray-600">
        A simple, clean, and powerful way to manage your tasks.
        Experience the evolution of task management from console to full-stack web.
      </p>

      <div className="flex flex-col space-y-4 sm:flex-row sm:space-x-4 sm:space-y-0">
        <Link
          href="/login"
          className="inline-flex items-center justify-center rounded-md bg-indigo-600 px-6 py-3 text-base font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
        >
          Sign In
        </Link>
        <Link
          href="/register"
          className="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-6 py-3 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
        >
          Create Account
        </Link>
      </div>

      <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-3">
        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 leading-6">Persistent</h3>
          <p className="mt-2 text-sm text-gray-500">
            Powered by Neon DB for reliable, long-term storage of your tasks.
          </p>
        </div>
        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 leading-6">Secure</h3>
          <p className="mt-2 text-sm text-gray-500">
            JWT-based authentication ensures your data remains private and safe.
          </p>
        </div>
        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 leading-6">Responsive</h3>
          <p className="mt-2 text-sm text-gray-500">
            Access your tasks from anywhere - whether on your phone or your desktop.
          </p>
        </div>
      </div>
    </div>
  );
}
