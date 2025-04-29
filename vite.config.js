import { defineConfig } from 'vite'
import { resolve } from 'path'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'frontend')
    }
  },
  build: {
    manifest: "manifest.json",
    outDir: "dist",
    rollupOptions: {
      input: "frontend/main.js",
    },
  },
})
