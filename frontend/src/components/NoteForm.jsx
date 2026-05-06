/**
 * NoteForm.jsx — Formulaire création de note.
 * Lit les tags du store, appelle addNote() à la soumission.
 */
import React, { useState } from 'react'
import useAppStore from '../store/useAppStore'

export default function NoteForm() {
    const [text, setText]   = useState('')
    const [tagId, setTagId] = useState('')
    const tags    = useAppStore((s) => s.tags)
    const addNote = useAppStore((s) => s.addNote)
    const loading = useAppStore((s) => s.loading)
    const error   = useAppStore((s) => s.error)

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!text.trim() || !tagId) return
        await addNote(text, parseInt(tagId))
        setText('')
        setTagId('')
    }

    return (
        <form onSubmit={handleSubmit} style={styles.form}>
            <h2 style={styles.title}>Nouvelle note</h2>
            {error && <div style={styles.error}>{error}</div>}
            <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Écrivez votre note..."
                rows={3}
                required
                style={styles.textarea}
            />
            <select
                value={tagId}
                onChange={(e) => setTagId(e.target.value)}
                required
                style={styles.select}
            >
                <option value="">-- Sélectionner un tag --</option>
                {tags.map((tag) => (
                    <option key={tag.id} value={tag.id}>{tag.name}</option>
                ))}
            </select>
            <button type="submit" disabled={loading} style={styles.btn}>
                {loading ? 'Enregistrement...' : 'Ajouter la note'}
            </button>
        </form>
    )
}

const styles = {
    form:     { display: 'flex', flexDirection: 'column', gap: '0.75rem' },
    title:    { margin: 0, color: '#1f2937' },
    error:    { background: '#fee2e2', color: '#991b1b', padding: '0.5rem', borderRadius: '4px', fontSize: '13px' },
    textarea: { padding: '0.6rem', border: '1px solid #d1d5db', borderRadius: '4px', resize: 'none', fontSize: '14px' },
    select:   { padding: '0.6rem', border: '1px solid #d1d5db', borderRadius: '4px', fontSize: '14px' },
    btn:      { padding: '0.6rem', background: '#1a56db', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '14px' },
}
