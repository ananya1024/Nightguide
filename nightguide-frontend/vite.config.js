import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // This rule says:
      // "If the browser asks for a path starting with '/upload'..."
      '/upload': {
        // "...forward that request to the backend server at this address."
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
});
