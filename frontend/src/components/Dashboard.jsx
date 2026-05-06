import { useEffect, useState } from 'react'
import useAppStore from '../store/useAppStore'
import NoteForm from './NoteForm'
import NoteList from './NoteList'
import TagForm  from './TagForm'

// Reproduit fidèlement le layout sidebar.blade.php de l'original
export default function Dashboard() {
    const user      = useAppStore((s) => s.user)
    const logout    = useAppStore((s) => s.logout)
    const fetchTags = useAppStore((s) => s.fetchTags)
    const [sidebarOpen, setSidebarOpen] = useState(false)

    useEffect(() => { fetchTags() }, [])

    const initials = user?.name
        ? user.name.split(' ').slice(0,2).map(w => w[0]).join('').toUpperCase()
        : '?'

    return (
        <div className="min-h-screen bg-white dark:bg-zinc-800 flex">

            {/* Sidebar overlay mobile */}
            {sidebarOpen && (
                <div className="fixed inset-0 z-20 bg-black/40 lg:hidden"
                     onClick={() => setSidebarOpen(false)} />
            )}

            {/* Sidebar */}
            <aside className={`
                fixed top-0 left-0 z-30 h-full w-64 flex flex-col
                border-r border-zinc-200 dark:border-zinc-700
                bg-zinc-50 dark:bg-zinc-900
                transform transition-transform duration-200
                ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
                lg:translate-x-0 lg:static lg:z-auto
            `}>
                {/* Close mobile */}
                <div className="flex items-center justify-between p-4 lg:hidden">
                    <span className="font-semibold text-zinc-900 dark:text-white">Renote</span>
                    <button onClick={() => setSidebarOpen(false)}
                        className="text-zinc-500 hover:text-zinc-900 dark:hover:text-white">
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                {/* Logo */}
                <div className="p-4 hidden lg:flex items-center gap-3">
                    <div className="w-8 h-8 bg-zinc-900 dark:bg-white rounded-md flex items-center justify-center">
                        <svg className="w-5 h-5 fill-current text-white dark:text-zinc-900" viewBox="0 0 24 24">
                            <path d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931z"/>
                        </svg>
                    </div>
                    <span className="font-semibold text-zinc-900 dark:text-white">Renote</span>
                </div>

                {/* Nav */}
                <nav className="flex-1 px-3 py-2">
                    <p className="px-2 py-1.5 text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-1">
                        Platform
                    </p>
                    <a href="#" className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium
                                          bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100
                                          border border-zinc-200 dark:border-zinc-700 shadow-sm">
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                        </svg>
                        Dashboard
                    </a>
                </nav>

                <div className="mt-auto px-3 py-4 border-t border-zinc-200 dark:border-zinc-700">
                    {/* User profile */}
                    <div className="flex items-center gap-3 px-2 py-2">
                        <span className="w-8 h-8 rounded-lg bg-neutral-200 dark:bg-neutral-700 flex items-center justify-center text-sm font-semibold text-black dark:text-white shrink-0">
                            {initials}
                        </span>
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-semibold text-zinc-900 dark:text-white truncate">{user?.name}</p>
                            <p className="text-xs text-zinc-500 dark:text-zinc-400 truncate">{user?.email}</p>
                        </div>
                        <button onClick={logout}
                            title="Log out"
                            className="text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition">
                            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                            </svg>
                        </button>
                    </div>
                </div>
            </aside>

            {/* Main */}
            <div className="flex-1 flex flex-col min-w-0">

                {/* Mobile header */}
                <header className="lg:hidden flex items-center justify-between px-4 py-3 border-b border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900">
                    <button onClick={() => setSidebarOpen(true)}
                        className="text-zinc-500 hover:text-zinc-900 dark:hover:text-white">
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                    <span className="font-semibold text-zinc-900 dark:text-white">Renote</span>
                    <button onClick={logout} className="text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300">
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                    </button>
                </header>

                {/* Content — identique dashboard.blade.php */}
                <main className="flex-1 p-6">
                    <div className="flex h-full w-full flex-1 flex-col gap-4 rounded-xl">

                        <div className="mt-2 p-4 border border-neutral-200 dark:border-neutral-700 rounded-xl bg-white dark:bg-neutral-900">
                            <NoteForm />
                        </div>

                        <div className="p-4 border border-neutral-200 dark:border-neutral-700 rounded-xl bg-white dark:bg-neutral-900">
                            <NoteList />
                        </div>

                        <div className="p-4 border border-neutral-200 dark:border-neutral-700 rounded-xl bg-white dark:bg-neutral-900">
                            <TagForm />
                        </div>

                    </div>
                </main>
            </div>
        </div>
    )
}
