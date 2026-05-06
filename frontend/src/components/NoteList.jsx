/**
 * NoteList.jsx — Liste des notes avec suppression.
 * Charge les notes au montage via fetchNotes().
 */
import React, { useEffect } from 'react'
import useAppStore from '../store/useAppStore'

export default function NoteList() {
    const notes      = useAppStore((s) => s.notes)
    const loading    = useAppStore((s) => s.loading)
    const fetchNotes = useAppStore((s) => s.fetchNotes)
    const removeNote = useAppStore((s) => s.removeNote)

    useEffect(() => { fetchNotes() }, [])

    const error = useAppStore((s) => s.error)

    if (loading && notes.length === 0) return <p style={{ color: '#6b7280' }}>Chargement...</p>
    if (error) return <p style={{ color: '#ef4444' }}>{error}</p>
    if (notes.length === 0) return <p style={{ color: '#6b7280', fontStyle: 'italic' }}>Aucune note pour l'instant.</p>

    return (
        <div>
            <h2 style={{ margin: '0 0 1rem', color: '#1f2937' }}>Vos notes ({notes.length})</h2>
            {notes.map((note) => (
                <div key={note.id} style={styles.note}>
                    <div>
                        <p style={styles.text}>{note.text}</p>
                        <span style={styles.tag}>{note.tag?.name ?? 'Sans tag'}</span>
                    </div>
                    <button onClick={() => removeNote(note.id)} style={styles.del}>
                        Supprimer
                    </button>
                </div>
            ))}
        </div>
    )
}

const styles = {
    note: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', border: '1px solid #e5e7eb', borderRadius: '6px', padding: '0.75rem', marginBottom: '0.5rem', background: '#fff' },
    text: { margin: '0 0 0.25rem', color: '#1f2937', fontSize: '14px' },
    tag:  { fontSize: '12px', color: '#6b7280', background: '#f3f4f6', padding: '2px 8px', borderRadius: '4px' },
    del:  { background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', fontSize: '13px', whiteSpace: 'nowrap' },
}
