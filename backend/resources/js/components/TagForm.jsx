/**
 * TagForm.jsx — Formulaire de création d'un tag.
 *
 * Responsabilité unique (S) : gère uniquement la création d'un tag.
 * Découplé de TagForm.php (Livewire) qui est maintenant obsolète.
 *
 * Dans l'ancienne architecture Livewire, TagForm.php dispatçhait un
 * événement 'tagCreated' écouté par Notes.php pour rafraîchir les tags.
 * Ici, plus besoin d'événements : le store Zustand est partagé.
 * addTag() met à jour state.tags et NoteForm le voit automatiquement.
 */
import React, { useState } from 'react';
import useAppStore from '../store/useAppStore';

export default function TagForm() {
    // État local du formulaire
    const [name, setName] = useState('');

    const addTag  = useAppStore((s) => s.addTag);
    const loading = useAppStore((s) => s.loading);
    const error   = useAppStore((s) => s.error);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!name.trim()) return;

        await addTag(name.trim());
        setName('');
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-3">
            <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100">
                Nouveau tag
            </h2>

            {error && (
                <div className="text-red-500 text-sm bg-red-50 border border-red-200 rounded p-2">
                    {error}
                </div>
            )}

            <div className="flex gap-2">
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Nom du tag..."
                    maxLength={50}
                    required
                    className="flex-1 border border-gray-300 dark:border-gray-600 rounded-lg p-2
                               bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
                               focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                    type="submit"
                    disabled={loading}
                    className="bg-green-600 hover:bg-green-700 disabled:bg-green-300
                               text-white font-medium px-4 py-2 rounded-lg transition-colors"
                >
                    {loading ? '...' : 'Ajouter'}
                </button>
            </div>
        </form>
    );
}
