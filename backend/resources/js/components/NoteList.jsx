/**
 * NoteList.jsx — Affiche la liste des notes de l'utilisateur.
 *
 * Responsabilité unique (S) : ce composant gère UNIQUEMENT l'affichage
 * de la liste et les suppressions. Il ne sait pas comment les notes
 * arrivent — il les lit dans le store Zustand.
 *
 * Au montage (useEffect), il déclenche fetchNotes() pour charger
 * les données depuis l'API. C'est le seul moment où il interagit
 * avec le cycle de vie des données.
 */
import React, { useEffect } from 'react';
import useAppStore from '../store/useAppStore';

export default function NoteList() {
    // Sélecteurs ciblés — évite les re-renders inutiles
    const notes      = useAppStore((s) => s.notes);
    const loading    = useAppStore((s) => s.loading);
    const fetchNotes = useAppStore((s) => s.fetchNotes);
    const removeNote = useAppStore((s) => s.removeNote);

    // Chargement initial des notes au montage du composant
    // [] en dépendance = s'exécute une seule fois (équivalent componentDidMount)
    useEffect(() => {
        fetchNotes();
    }, []);

    const handleDelete = async (id) => {
        // Délègue la suppression au store — pas de fetch ici
        await removeNote(id);
    };

    if (loading && notes.length === 0) {
        return (
            <div className="text-center text-gray-500 py-8">
                Chargement des notes...
            </div>
        );
    }

    if (notes.length === 0) {
        return (
            <div className="text-center text-gray-400 py-8 italic">
                Aucune note pour l'instant. Créez-en une !
            </div>
        );
    }

    return (
        <div className="space-y-3">
            <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100">
                Vos notes ({notes.length})
            </h2>

            {notes.map((note) => (
                <div
                    key={note.id}
                    className="flex justify-between items-start border border-gray-200
                               dark:border-gray-700 rounded-lg p-4 bg-white dark:bg-gray-800"
                >
                    <div className="flex-1 pr-4">
                        {/* Texte de la note */}
                        <p className="text-gray-900 dark:text-gray-100 whitespace-pre-wrap">
                            {note.text}
                        </p>

                        {/* Tag associé — note.tag peut être null si le tag a été supprimé */}
                        <span className="inline-block mt-2 text-xs text-gray-500
                                         dark:text-gray-400 bg-gray-100 dark:bg-gray-700
                                         rounded px-2 py-0.5">
                            {note.tag?.name ?? 'Sans tag'}
                        </span>
                    </div>

                    {/* Bouton suppression */}
                    <button
                        onClick={() => handleDelete(note.id)}
                        disabled={loading}
                        className="text-red-400 hover:text-red-600 disabled:opacity-40
                                   text-sm font-medium transition-colors shrink-0"
                    >
                        Supprimer
                    </button>
                </div>
            ))}
        </div>
    );
}
