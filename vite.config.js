import { defineConfig } from 'vite'
import { resolve } from 'path'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
    plugins: [tailwindcss()],
    root: resolve(import.meta.dirname, 'app/'),
    base: '/static/',
    build: {
        manifest: 'manifest.json',
        outDir: resolve(import.meta.dirname, 'app/static/dist/'),
        emptyOutDir: true,
        rollupOptions: {
            input: {
                app: resolve(import.meta.dirname, 'app/src/entries/app.js'),
                // dashboard: resolve(import.meta.dirname, 'app/src/entries/dashboard.js'),
                // saleEntry: resolve(import.meta.dirname, 'app/src/entries/sale-entry.js'),
                // receipt: resolve(import.meta.dirname, 'app/src/entries/receipt.js'),
            },
            output: {
                entryFileNames: 'js/[name].[hash].js',
                chunkFileNames: 'js/[name].[hash].js',
                assetFileNames: (assetInfo) => {
                    const name = assetInfo.name || '';

                    if (name.endsWith('.css')) {
                        return 'css/[name].[hash][extname]';
                    }
                    // Automatically match common font file extensions
                    if (/\.(woff2?|eot|ttf|otf)$/i.test(name)) {
                        return 'fonts/[name].[hash][extname]';
                    }

                    return 'assets/[name].[hash][extname]';
                },
            },
        },
    },
    server: { origin: 'http://localhost:5173' },
})
