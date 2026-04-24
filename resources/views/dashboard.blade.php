{{--
    dashboard.blade.php — Vue principale de l'application.

    AVANT (architecture Livewire) :
        @livewireStyles / @livewireScripts
        <livewire:notes />       ← composant PHP server-driven
        <livewire:tag-form />    ← composant PHP server-driven

    APRÈS (architecture React) :
        <div id="react-app">    ← point de montage React
        React prend le relais, appelle l'API REST, gère l'affichage.
        Blade ne fait plus que fournir la coquille HTML + auth Laravel.
--}}
<x-layouts.app :title="__('Dashboard')">
    <div class="flex h-full w-full flex-1 flex-col gap-4 rounded-xl">

        {{--
            Point de montage React.
            app.jsx cherche getElementById('react-app') et monte <App /> ici.
            Tout ce qui était dans les composants Livewire est maintenant
            géré par React côté client.
        --}}
        <div id="react-app">
            {{-- Affiche un loader pendant que React se charge --}}
            <div class="flex items-center justify-center py-12 text-gray-400">
                Chargement...
            </div>
        </div>

    </div>
</x-layouts.app>
