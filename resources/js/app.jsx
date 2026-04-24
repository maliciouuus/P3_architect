/**
 * app.jsx — Point d'entrée de l'application React.
 *
 * Ce fichier remplace app.js (qui était vide dans l'architecture Livewire).
 * Il monte le composant React <App /> dans le div#react-app injecté dans
 * le layout Blade. C'est la séparation front / back : Blade gère juste
 * la coquille HTML, React gère tout l'affichage interactif.
 */
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './components/App';

// On cherche le point de montage dans le DOM Blade
const container = document.getElementById('react-app');

if (container) {
    // createRoot est l'API React 18 — remplace ReactDOM.render()
    const root = createRoot(container);
    root.render(<App />);
}
