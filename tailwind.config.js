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
        emberSoft: '#d98463',
        gold: '#f0c56f',
        brass: '#c79752',
        mist: '#f6efe4',
        pewter: '#a99a92',
        panel: 'rgba(18, 13, 15, 0.88)',
      },
      boxShadow: {
        glow: '0 0 18px rgba(240, 197, 111, 0.20)',
        frame: '0 0 0 1px rgba(240, 197, 111, 0.18), inset 0 0 0 1px rgba(240, 197, 111, 0.08)',
      },
      fontFamily: {
        display: ['Italiana', 'Marcellus', 'serif'],
        body: ['Josefin Sans', 'Segoe UI', 'sans-serif'],
        accent: ['Marcellus', 'serif'],
      },
    },
  },
  plugins: [],
};