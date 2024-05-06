/** @type {import('next').NextConfig} */
const nextConfig = {
//disaslbe eslint
eslint: {
  ignoreDuringBuilds: true,
},
  reactStrictMode: true,
  images: {
    domains: ['res.cloudinary.com'],
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: securityHeaders,
      },
    ];
  },


};
export default nextConfig;
