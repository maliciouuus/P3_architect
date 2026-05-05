/**
 * services/api.js — Couche d'accès à l'API REST du back-end Laravel.
 *
 * Principe S (Single Responsibility) : ce fichier a une seule responsabilité,
 * communiquer avec l'API. Les composants React n'ont JAMAIS à connaître les URLs
 * ou les headers HTTP — ils appellent ces fonctions et reçoivent des données.
 *
 * Principe D (Dependency Inversion) : les composants dépendent de cette abstraction
 * (les fonctions), pas directement de fetch ou d'axios.
 *
 * axios est déjà installé dans le projet (package.json).
 * withCredentials: true permet d'envoyer le cookie de session Laravel
 * pour que le middleware 'auth' reconnaisse l'utilisateur connecté.
 */
import axios from 'axios';

// Instance axios partagée — baseURL + credentials cookie Laravel
const api = axios.create({
    baseURL: '/api',
    withCredentials: true,       // envoie le cookie de session Laravel
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        // CSRF token Laravel — obligatoire pour POST/DELETE
        'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]')?.content,
    },
});

// ─── NOTES ───────────────────────────────────────────────────────────────────

/**
 * Récupère toutes les notes de l'utilisateur connecté.
 * Correspond à : GET /api/notes
 * @returns {Promise<Array>} tableau de notes avec leur tag
 */
export const getNotes = async () => {
    const response = await api.get('/notes');
    return response.data.data; // { status, data: [...] }
};

/**
 * Crée une nouvelle note.
 * Correspond à : POST /api/notes
 * @param {string} text    Contenu de la note
 * @param {number} tag_id  ID du tag associé
 * @returns {Promise<Object>} la note créée
 */
export const createNote = async (text, tag_id) => {
    const response = await api.post('/notes', { text, tag_id });
    return response.data.data;
};

/**
 * Supprime une note par son ID.
 * Correspond à : DELETE /api/notes/{id}
 * @param {number} id  ID de la note à supprimer
 */
export const deleteNote = async (id) => {
    await api.delete(`/notes/${id}`);
};

// ─── TAGS ─────────────────────────────────────────────────────────────────────

/**
 * Récupère tous les tags disponibles.
 * Correspond à : GET /api/tags
 * @returns {Promise<Array>} tableau de tags
 */
export const getTags = async () => {
    const response = await api.get('/tags');
    return response.data.data;
};

/**
 * Crée un nouveau tag.
 * Correspond à : POST /api/tags
 * @param {string} name  Nom du tag
 * @returns {Promise<Object>} le tag créé
 */
export const createTag = async (name) => {
    const response = await api.post('/tags', { name });
    return response.data.data;
};
