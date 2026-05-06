import { useState } from 'react'
import useAppStore from '../store/useAppStore'

// Reproduit fidèlement le style Flux/Livewire de l'original
export default function Login({ onSwitchToRegister }) {
    const [email, setEmail]       = useState('')
    const [password, setPassword] = useState('')
    const [showPwd, setShowPwd]   = useState(false)
    const login   = useAppStore((s) => s.login)
    const loading = useAppStore((s) => s.loading)
    const error   = useAppStore((s) => s.error)

    const handleSubmit = async (e) => {
        e.preventDefault()
        await login(email, password)
    }

    return (
        // Layout identique à simple.blade.php
        <div className="min-h-screen bg-white dark:bg-gradient-to-b dark:from-neutral-950 dark:to-neutral-900 flex flex-col items-center justify-center gap-6 p-6 md:p-10">
            <div className="flex w-full max-w-sm flex-col gap-2">

                {/* Logo — identique à x-app-logo-icon */}
                <a href="#" className="flex flex-col items-center gap-2 font-medium mb-2">
                    <span className="flex h-9 w-9 items-center justify-center rounded-md">
                        <svg className="size-9 fill-current text-black dark:text-white" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
                            <path fillRule="evenodd" clipRule="evenodd" d="M20 2C10.059 2 2 10.059 2 20s8.059 18 18 18 18-8.059 18-18S29.941 2 20 2zm0 3c8.284 0 15 6.716 15 15 0 8.284-6.716 15-15 15-8.284 0-15-6.716-15-15 0-8.284 6.716-15 15-15zm-1 7v7h-7v2h7v7h2v-7h7v-2h-7v-7h-2z"/>
                        </svg>
                    </span>
                </a>

                {/* Card */}
                <div className="flex flex-col gap-6">

                    {/* Header — identique à x-auth-header */}
                    <div className="flex w-full flex-col text-center gap-1">
                        <h1 className="text-xl font-semibold text-zinc-900 dark:text-white">
                            Log in to your account
                        </h1>
                        <p className="text-sm text-zinc-500 dark:text-zinc-400">
                            Enter your email and password below to log in
                        </p>
                    </div>

                    {/* Error */}
                    {error && (
                        <div className="rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 px-4 py-3 text-sm text-red-600 dark:text-red-400 text-center">
                            {error}
                        </div>
                    )}

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="flex flex-col gap-6">

                        {/* Email */}
                        <div className="flex flex-col gap-2">
                            <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                                Email address
                            </label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="email@example.com"
                                required autoFocus
                                className="h-10 w-full rounded-lg border border-zinc-300 dark:border-zinc-600
                                           bg-white dark:bg-zinc-800 px-3 text-sm
                                           text-zinc-900 dark:text-zinc-100
                                           placeholder:text-zinc-400 dark:placeholder:text-zinc-500
                                           focus:outline-none focus:ring-2 focus:ring-zinc-800 dark:focus:ring-zinc-200
                                           transition"
                            />
                        </div>

                        {/* Password */}
                        <div className="flex flex-col gap-2">
                            <div className="flex items-center justify-between">
                                <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                                    Password
                                </label>
                                <button type="button" onClick={onSwitchToRegister}
                                    className="text-xs text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 transition">
                                    Forgot your password?
                                </button>
                            </div>
                            <div className="relative">
                                <input
                                    type={showPwd ? 'text' : 'password'}
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="Password"
                                    required
                                    className="h-10 w-full rounded-lg border border-zinc-300 dark:border-zinc-600
                                               bg-white dark:bg-zinc-800 px-3 pr-10 text-sm
                                               text-zinc-900 dark:text-zinc-100
                                               placeholder:text-zinc-400 dark:placeholder:text-zinc-500
                                               focus:outline-none focus:ring-2 focus:ring-zinc-800 dark:focus:ring-zinc-200
                                               transition"
                                />
                                <button type="button" onClick={() => setShowPwd(!showPwd)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300">
                                    {showPwd
                                        ? <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
                                        : <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                                    }
                                </button>
                            </div>
                        </div>

                        {/* Submit — flux:button variant="primary" */}
                        <button type="submit" disabled={loading}
                            className="h-10 w-full rounded-lg bg-zinc-900 dark:bg-zinc-100 text-sm font-medium
                                       text-white dark:text-zinc-900 hover:bg-zinc-700 dark:hover:bg-zinc-300
                                       disabled:opacity-50 transition cursor-pointer">
                            {loading ? 'Logging in...' : 'Log in'}
                        </button>
                    </form>

                    {/* Footer */}
                    <p className="text-center text-sm text-zinc-600 dark:text-zinc-400">
                        Don't have an account?{' '}
                        <button onClick={onSwitchToRegister}
                            className="text-zinc-900 dark:text-zinc-100 underline underline-offset-4 hover:no-underline transition">
                            Sign up
                        </button>
                    </p>
                </div>
            </div>
        </div>
    )
}
