/**
 * store/useAppStore.js — Store global Zustand.
 *
 * Zustand est choisi pour sa simplicité par rapport à Redux :
 * pas de boilerplate actions/reducers/dispatch, juste un objet avec
 * des fonctions qui modifient l'état directement.
 *
 * Pattern appliqué : Flux simplifié
 *   Action (ex: addNote) → modifie le store → les composants
 *   qui lisent le store se re-rendent automatiquement.
 *
 * Principe S (Single Responsibility) :
 *   - Le store gère l'état global (notes, tags, loading, error)
 *   - Il délègue les appels réseau aux fonctions de api.js
 *   - Les composants React ne font que lire le store et appeler ses actions
 *
 * Principe D (Dependency Inversion) :
 *   - Le store dépend de l'abstraction api.js, pas directement de fetch
 *
 * Usage dans un composant :
 *   const { notes, fetchNotes } = useAppStore();
 */
import { create } from 'zustand';
import { getNotes, createNote, deleteNote, getTags, createTag } from '../services/api';

const useAppStore = create((set, get) => ({

    // ── État ──────────────────────────────────────────────────────────────────

    /** Liste des notes de l'utilisateur connecté */
    notes: [],

    /** Liste de tous les tags disponibles */
    tags: [],

    /** true pendant un appel API en cours — permet d'afficher un loader */
    loading: false,

    /** Message d'erreur à afficher si un appel API échoue */
    error: null,

    // ── Actions Notes ─────────────────────────────────────────────────────────

    /**
     * Charge toutes les notes depuis l'API et les stocke dans le store.
     * Appelé au montage du composant NoteList.
     */
    fetchNotes: async () => {
        set({ loading: true, error: null });
        try {
            const notes = await getNotes();
            set({ notes, loading: false });
        } catch (err) {
            // On stocke l'erreur dans le store — le composant l'affiche
            set({ error: 'Impossible de charger les notes.', loading: false });
        }
    },

    /**
     * Crée une note via l'API puis rafraîchit la liste localement.
     * On ajoute directement au store sans re-fetcher toute la liste
     * (optimistic update simplifié).
     *
     * @param {string} text    Texte de la note
     * @param {number} tag_id  ID du tag sélectionné
     */
    addNote: async (text, tag_id) => {
        set({ loading: true, error: null });
        try {
            const newNote = await createNote(text, tag_id);
            // On préfixe la nouvelle note en tête de liste (cohérent avec ->latest())
            set((state) => ({
                notes: [newNote, ...state.notes],
                loading: false,
            }));
        } catch (err) {
            const msg = err.response?.data?.message || 'Erreur lors de la création.';
            set({ error: msg, loading: false });
        }
    },

    /**
     * Supprime une note via l'API puis la retire du store local.
     * @param {number} id  ID de la note à supprimer
     */
    removeNote: async (id) => {
        set({ loading: true, error: null });
        try {
            await deleteNote(id);
            // On filtre la note supprimée sans re-fetcher
            set((state) => ({
                notes: state.notes.filter((n) => n.id !== id),
                loading: false,
            }));
        } catch (err) {
            set({ error: 'Impossible de supprimer la note.', loading: false });
        }
    },

    // ── Actions Tags ──────────────────────────────────────────────────────────

    /**
     * Charge tous les tags depuis l'API.
     * Appelé au montage du composant TagForm ou App.
     */
    fetchTags: async () => {
        set({ loading: true, error: null });
        try {
            const tags = await getTags();
            set({ tags, loading: false });
        } catch (err) {
            set({ error: 'Impossible de charger les tags.', loading: false });
        }
    },

    /**
     * Crée un tag via l'API puis l'ajoute au store.
     * @param {string} name  Nom du nouveau tag
     */
    addTag: async (name) => {
        set({ loading: true, error: null });
        try {
            const newTag = await createTag(name);
            set((state) => ({
                tags: [...state.tags, newTag],
                loading: false,
            }));
        } catch (err) {
            const msg = err.response?.data?.message || 'Erreur lors de la création du tag.';
            set({ error: msg, loading: false });
        }
    },
}));

export default useAppStore;
