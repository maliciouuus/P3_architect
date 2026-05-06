/**
 * store/useAppStore.js — Store Zustand global.
 *
 * Gère l'état de toute l'application :
 * - auth : token JWT + utilisateur connecté
 * - notes / tags : données métier
 * - loading / error : états UI
 *
 * Pattern Flux : action → store → UI
 */
import { create } from 'zustand'
import {
    login as apiLogin,
    register as apiRegister,
    logout as apiLogout,
    getNotes, createNote, deleteNote,
    getTags, createTag,
} from '../services/api'

const useAppStore = create((set) => ({

    // ── Auth ──────────────────────────────────────────────────────────────────

    /** Token stocké en mémoire et localStorage pour la persistance */
    token: localStorage.getItem('token') || null,
    user:  null,

    /**
     * Connecte l'utilisateur, stocke le JWT dans le store et localStorage.
     * @param {string} email
     * @param {string} password
     */
    login: async (email, password) => {
        set({ loading: true, error: null })
        try {
            const data = await apiLogin(email, password)
            localStorage.setItem('token', data.token)
            set({ token: data.token, user: data.user, loading: false })
        } catch (err) {
            const msg = err.response?.data?.message || 'Identifiants invalides.'
            set({ error: msg, loading: false })
        }
    },

    register: async (name, email, password) => {
        set({ loading: true, error: null })
        try {
            const data = await apiRegister(name, email, password)
            localStorage.setItem('token', data.token)
            set({ token: data.token, user: data.user, loading: false })
        } catch (err) {
            const msg = err.response?.data?.message || 'Erreur lors de l\'inscription.'
            set({ error: msg, loading: false })
        }
    },

    /**
     * Déconnecte l'utilisateur, supprime le token.
     */
    logout: async () => {
        try { await apiLogout() } catch (_) {}
        localStorage.removeItem('token')
        set({ token: null, user: null, notes: [], tags: [] })
    },

    // ── Notes ─────────────────────────────────────────────────────────────────

    notes: [],

    fetchNotes: async () => {
        set({ loading: true, error: null })
        try {
            const notes = await getNotes()
            set({ notes, loading: false })
        } catch {
            set({ error: 'Impossible de charger les notes.', loading: false })
        }
    },

    addNote: async (text, tag_id) => {
        set({ loading: true, error: null })
        try {
            const note = await createNote(text, tag_id)
            set((s) => ({ notes: [note, ...s.notes], loading: false }))
        } catch (err) {
            set({ error: err.response?.data?.message || 'Erreur.', loading: false })
        }
    },

    removeNote: async (id) => {
        set({ loading: true, error: null })
        try {
            await deleteNote(id)
            set((s) => ({ notes: s.notes.filter((n) => n.id !== id), loading: false }))
        } catch {
            set({ error: 'Impossible de supprimer.', loading: false })
        }
    },

    // ── Tags ──────────────────────────────────────────────────────────────────

    tags: [],

    fetchTags: async () => {
        set({ loading: true, error: null })
        try {
            const tags = await getTags()
            set({ tags, loading: false })
        } catch {
            set({ error: 'Impossible de charger les tags.', loading: false })
        }
    },

    addTag: async (name) => {
        set({ loading: true, error: null })
        try {
            const tag = await createTag(name)
            set((s) => ({ tags: [...s.tags, tag], loading: false }))
        } catch (err) {
            set({ error: err.response?.data?.message || 'Erreur.', loading: false })
        }
    },

    // ── UI ────────────────────────────────────────────────────────────────────
    loading: false,
    error:   null,
}))

export default useAppStore
