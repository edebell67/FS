import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [],
  },
  // This epic has its own package-lock.json nested inside the monorepo-style
  // `eds` workspace, which otherwise makes Next guess the wrong root for
  // file tracing during build.
  outputFileTracingRoot: __dirname,
};

export default nextConfig;
