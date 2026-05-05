/**
 * services/api.js — Couche d'accès à l'API REST.
 *
 * Différence majeure par rapport à l'ancienne version :
 * - Plus de cookies de session ni de CSRF token
 * - Authentification via JWT (Bearer token)
 * - Le token est stocké dans localStorage et envoyé dans chaque requête
 *
 * Principe S : ce fichier a une seule responsabilité — parler à l'API.
 * Principe D : les composants dépendent de ces fonctions, pas d'axios directement.
 */
import axios from 'axios'

const api = axios.create({
    baseURL: '/api',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
})

// Intercepteur — ajoute automatiquement le JWT à chaque requête si disponible
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// ─── AUTH ─────────────────────────────────────────────────────────────────────

/**
 * Inscrit un nouvel utilisateur.
 * POST /api/register
 * @returns {{ token: string, user: object }}
 */
export const register = async (name, email, password) => {
    const res = await api.post('/register', { name, email, password })
    return res.data
}

/**
 * Connecte un utilisateur et retourne un JWT.
 * POST /api/login
 * @returns {{ token: string, user: object }}
 */
export const login = async (email, password) => {
    const res = await api.post('/login', { email, password })
    return res.data
}

/**
 * Déconnecte l'utilisateur (invalide le token côté serveur).
 * POST /api/logout
 */
export const logout = async () => {
    await api.post('/logout')
}

// ─── NOTES ────────────────────────────────────────────────────────────────────

/** GET /api/notes */
export const getNotes = async () => {
    const res = await api.get('/notes')
    return res.data.data
}

/** POST /api/notes */
export const createNote = async (text, tag_id) => {
    const res = await api.post('/notes', { text, tag_id })
    return res.data.data
}

/** DELETE /api/notes/{id} */
export const deleteNote = async (id) => {
    await api.delete(`/notes/${id}`)
}

// ─── TAGS ─────────────────────────────────────────────────────────────────────

/** GET /api/tags */
export const getTags = async () => {
    const res = await api.get('/tags')
    return res.data.data
}

/** POST /api/tags */
export const createTag = async (name) => {
    const res = await api.post('/tags', { name })
    return res.data.data
}
