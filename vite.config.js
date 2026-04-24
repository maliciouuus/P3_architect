/**
 * vite.config.js — Configuration du bundler Vite.
 *
 * Modifications par rapport à la config initiale :
 *  1. Ajout du plugin @vitejs/plugin-react pour compiler le JSX React
 *  2. Remplacement de app.js par app.jsx comme point d'entrée JS
 *     (app.js était vide dans l'architecture Livewire)
 *  3. Le plugin laravel-vite-plugin s'occupe d'injecter les assets
 *     dans les templates Blade via @vite(...)
 */
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import tailwindcss from "@tailwindcss/vite";
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [
        // Plugin React — compile le JSX en JS standard
        react(),

        laravel({
            // app.jsx remplace app.js comme point d'entrée principal
            input: ['resources/css/app.css', 'resources/js/app.jsx'],
            refresh: true,
        }),
        tailwindcss(),
    ],
    server: {
        cors: true,
    },
});