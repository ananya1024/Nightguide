/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html", // <-- THIS LINE IS THE MOST IMPORTANT FIX
    "./src/**/*.{js,ts,jsx,tsx}", // This line scans your JavaScript/React files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}