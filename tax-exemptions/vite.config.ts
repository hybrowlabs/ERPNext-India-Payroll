import path from 'path';
import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react'
import proxyOptions from './proxyOptions';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        port: 3000,
        proxy: proxyOptions,
        host: "0.0.0.0",
    },
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
    build: {
        outDir: '../cn_indian_payroll/public/tax-exemptions',
        emptyOutDir: true,
        target: 'es2015',
    },
});
