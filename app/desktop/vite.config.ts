import { defineConfig } from "vite";

// Vite config tuned for Tauri: fixed dev port, no clearScreen so Rust logs
// stay visible, and a small/fast production bundle.
export default defineConfig({
  clearScreen: false,
  server: {
    port: 1420,
    strictPort: true,
    watch: {
      // Don't watch the Rust side; cargo handles that.
      ignored: ["**/src-tauri/**"],
    },
  },
  build: {
    target: "es2021",
    minify: "esbuild",
    sourcemap: false,
    // Inline tiny assets; we ship almost nothing besides JS+CSS.
    assetsInlineLimit: 4096,
  },
});
