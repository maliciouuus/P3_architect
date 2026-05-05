/**
 * App.jsx — Composant racine.
 *
 * Gère le routing simple entre :
 * - Login / Register (si pas de token JWT)
 * - Dashboard (si token présent)
 *
 * Pas besoin de react-router-dom ici : on switche juste
 * entre les vues selon l'état d'authentification du store.
 */
import React, { useState } from 'react'
import useAppStore from './store/useAppStore'
import Login     from './components/Login'
import Register  from './components/Register'
import Dashboard from './components/Dashboard'

export default function App() {
    const token = useAppStore((s) => s.token)
    const [showRegister, setShowRegister] = useState(false)

    // Si l'utilisateur est connecté (token JWT présent) → Dashboard
    if (token) return <Dashboard />

    // Sinon → Login ou Register
    if (showRegister) {
        return <Register onSwitchToLogin={() => setShowRegister(false)} />
    }
    return <Login onSwitchToRegister={() => setShowRegister(true)} />
}
