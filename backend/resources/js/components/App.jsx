/**
 * App.jsx — Composant racine de l'application React.
 *
 * C'est le seul composant qui connaît la structure globale de la page.
 * Il charge les tags au démarrage (fetchTags) pour que NoteForm
 * puisse afficher le select dès le premier rendu.
 *
 * Architecture client-driven :
 *   Blade (PHP) → fournit la coquille HTML + authentification
 *   React (App.jsx) → gère tout l'affichage interactif
 *   Zustand (useAppStore) → gère l'état global partagé entre composants
 *   api.js → communique avec le back-end Laravel via /api/*
 *
 * Flux des données :
 *   App monte → fetchTags() → store.tags mis à jour → NoteForm affiche le select
 *   NoteList monte → fetchNotes() → store.notes mis à jour → NoteList affiche les notes
 *   Utilisateur crée note → addNote() → store.notes mis à jour → NoteList re-render
 */
import React, { useEffect } from 'react';
import NoteForm from './NoteForm';
import NoteList from './NoteList';
import TagForm from './TagForm';
import useAppStore from '../store/useAppStore';

export default function App() {
    const fetchTags = useAppStore((s) => s.fetchTags);

    // Charge les tags une seule fois au montage de l'app
    // NoteForm a besoin des tags pour afficher le select de sélection
    useEffect(() => {
        fetchTags();
    }, []);

    return (
        <div className="space-y-6">
            {/* Section création de note */}
            <div className="p-4 border border-neutral-200 dark:border-neutral-700
                            rounded-xl bg-white dark:bg-neutral-900">
                <NoteForm />
            </div>

            {/* Section liste des notes */}
            <div className="p-4 border border-neutral-200 dark:border-neutral-700
                            rounded-xl bg-white dark:bg-neutral-900">
                <NoteList />
            </div>

            {/* Section création de tag */}
            <div className="p-4 border border-neutral-200 dark:border-neutral-700
                            rounded-xl bg-white dark:bg-neutral-900">
                <TagForm />
            </div>
        </div>
    );
}
