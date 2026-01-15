import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
    async redirects() {
    return [
      {
        source: '/dashboard',
        destination: '/dashboard/review',
        permanent: true, // This creates a 308 permanent redirect
      },
    ];
  },
};

export default nextConfig;
