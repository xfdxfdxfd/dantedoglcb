/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './public/index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        ink: '#120d0f',
        ember: '#ca5a2e',
        gold: '#f0c56f',
        mist: '#f6efe4',
        panel: 'rgba(18, 13, 15, 0.84)',
      },
      boxShadow: {
        glow: '0 24px 80px rgba(0, 0, 0, 0.45)',
      },
      fontFamily: {
        display: ['Trebuchet MS', 'Verdana', 'sans-serif'],
        body: ['Segoe UI', 'Tahoma', 'sans-serif'],
      },
    },
  },
  plugins: [],
};