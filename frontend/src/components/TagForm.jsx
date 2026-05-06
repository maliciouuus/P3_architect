/**
 * TagForm.jsx — Formulaire création de tag.
 * Appelle addTag() du store. Le nouveau tag apparaît automatiquement dans NoteForm.
 */
import React, { useState } from 'react'
import useAppStore from '../store/useAppStore'

export default function TagForm() {
    const [name, setName] = useState('')
    const addTag  = useAppStore((s) => s.addTag)
    const loading = useAppStore((s) => s.loading)
    const error   = useAppStore((s) => s.error)

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!name.trim()) return
        await addTag(name.trim())
        setName('')
    }

    return (
        <div>
            <h2 style={{ margin: '0 0 1rem', color: '#1f2937' }}>Nouveau tag</h2>
            {error && <div style={styles.error}>{error}</div>}
            <form onSubmit={handleSubmit} style={styles.form}>
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Nom du tag..."
                    maxLength={50}
                    required
                    style={styles.input}
                />
                <button type="submit" disabled={loading} style={styles.btn}>
                    {loading ? '...' : 'Ajouter'}
                </button>
            </form>
        </div>
    )
}

const styles = {
    form:  { display: 'flex', gap: '0.5rem' },
    input: { flex: 1, padding: '0.6rem', border: '1px solid #d1d5db', borderRadius: '4px', fontSize: '14px' },
    btn:   { padding: '0.6rem 1rem', background: '#065f46', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '14px' },
    error: { background: '#fee2e2', color: '#991b1b', padding: '0.5rem', borderRadius: '4px', fontSize: '13px', marginBottom: '0.5rem' },
}
