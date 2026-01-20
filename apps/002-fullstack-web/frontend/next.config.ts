import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: false, // Temporarily disable React Compiler to avoid conflicts
  transpilePackages: [
    // Add any packages that need to be transpiled
  ],
};

export default nextConfig;
