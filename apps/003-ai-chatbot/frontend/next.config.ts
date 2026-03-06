import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: "/api/v1",
  },
  /* config options here */
  reactCompiler: false, // Temporarily disable React Compiler to avoid conflicts
  transpilePackages: [
    // Add any packages that need to be transpiled
  ],
  // Specify the root directory to resolve the multiple lockfiles warning
  turbopack: {
    root: __dirname,
  },
  async rewrites() {
    // When running in Docker, we want to proxy requests to the backend service
    // When running locally, we want to proxy to localhost:7860
    const backendUrl = process.env.BACKEND_URL || "http://localhost:7860";
    console.log(`[Next.js] Rewriting /api/v1 to ${backendUrl}/api/v1`);
    return [
      {
        source: "/api/v1/:path*",
        destination: `${backendUrl}/api/v1/:path*`,
      },
    ];
  },
};

export default nextConfig;
