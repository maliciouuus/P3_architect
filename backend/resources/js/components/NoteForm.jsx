/**
 * NoteForm.jsx — Formulaire de création d'une note.
 *
 * Responsabilité unique (S) : ce composant gère UNIQUEMENT le formulaire
 * de création. Il ne sait pas comment les notes sont stockées, il délègue
 * au store Zustand via addNote().
 *
 * Il ne fait aucun appel API directement — c'est le store qui s'en charge.
 * Cela respecte le principe D : le composant dépend du store (abstraction),
 * pas de fetch/axios directement.
 */
import React, { useState } from 'react';
import useAppStore from '../store/useAppStore';

export default function NoteForm() {
    // État local du formulaire — reste dans le composant car non partagé
    const [text, setText] = useState('');
    const [tagId, setTagId] = useState('');

    // On récupère ce dont on a besoin dans le store (sélecteurs ciblés)
    // Zustand ne re-rend ce composant QUE si tags, addNote ou loading changent
    const tags    = useAppStore((s) => s.tags);
    const addNote = useAppStore((s) => s.addNote);
    const loading = useAppStore((s) => s.loading);
    const error   = useAppStore((s) => s.error);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!text.trim() || !tagId) return;

        // Délègue la création au store — pas de fetch ici
        await addNote(text, parseInt(tagId));

        // Réinitialise le formulaire local après succès
        setText('');
        setTagId('');
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-3 mb-6">
            <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100">
                Nouvelle note
            </h2>

            {/* Affichage de l'erreur venant du store */}
            {error && (
                <div className="text-red-500 text-sm bg-red-50 border border-red-200 rounded p-2">
                    {error}
                </div>
            )}

            <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Écrivez votre note..."
                rows={3}
                required
                className="w-full border border-gray-300 dark:border-gray-600 rounded-lg p-3
                           bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
                           focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            />

            <select
                value={tagId}
                onChange={(e) => setTagId(e.target.value)}
                required
                className="w-full border border-gray-300 dark:border-gray-600 rounded-lg p-2
                           bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
                           focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
                <option value="">-- Sélectionner un tag --</option>
                {tags.map((tag) => (
                    <option key={tag.id} value={tag.id}>
                        {tag.name}
                    </option>
                ))}
            </select>

            <button
                type="submit"
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300
                           text-white font-medium px-4 py-2 rounded-lg transition-colors"
            >
                {loading ? 'Enregistrement...' : 'Ajouter la note'}
            </button>
        </form>
    );
}
