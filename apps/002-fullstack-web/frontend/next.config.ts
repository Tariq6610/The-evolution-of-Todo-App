import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: false, // Temporarily disable React Compiler to avoid conflicts
  transpilePackages: [
    // Add any packages that need to be transpiled
  ],
  // Specify the root directory to resolve the multiple lockfiles warning
  turbopack: {
    root: __dirname,
  },
};

export default nextConfig;
