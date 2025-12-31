import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/context/auth_context";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Todo App",
  description: "Evolution of Todo App - Phase 2: Full-Stack Web",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <main className="min-h-screen bg-gray-50 text-gray-900">
            <div className="max-w-4xl mx-auto px-4 py-8">
              {children}
            </div>
          </main>
        </AuthProvider>
      </body>
    </html>
  );
}
