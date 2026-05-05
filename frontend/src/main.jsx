/**
 * main.jsx — Point d'entrée React.
 * Monte <App /> dans le div#root de index.html.
 */
import React from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'

createRoot(document.getElementById('root')).render(<App />)
