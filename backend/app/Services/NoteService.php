<?php

namespace App\Services;

use App\Models\Note;
use Illuminate\Support\Facades\Auth;

/**
 * NoteService — contient toute la logique métier liée aux notes.
 * Respecte le principe S de SOLID : une seule responsabilité (gérer les notes).
 * Injecté dans NoteController via l'injection de dépendances Laravel (principe D).
 */
class NoteService
{
    /**
     * Récupère toutes les notes de l'utilisateur connecté,
     * avec leur tag associé (eager loading pour éviter le N+1).
     */
    public function getAllForUser(): \Illuminate\Database\Eloquent\Collection
    {
        return Note::with('tag')
            ->where('user_id', Auth::id())
            ->latest()
            ->get();
    }

    /**
     * Crée une nouvelle note pour l'utilisateur connecté.
     * L'user_id est injecté ici (pas dans le contrôleur) : la logique reste dans le service.
     *
     * @param array $data  Doit contenir 'tag_id' et 'text'
     */
    public function create(array $data): Note
    {
        return Note::create([
            'user_id' => Auth::id(),
            'tag_id'  => $data['tag_id'],
            'text'    => $data['text'],
        ]);
    }

    /**
     * Supprime une note uniquement si elle appartient à l'utilisateur connecté.
     * La vérification d'appartenance est dans le service, pas dans le contrôleur.
     *
     * @param int $noteId  ID de la note à supprimer
     * @return bool  true si la note a été supprimée, false sinon
     */
    public function delete(int $noteId): bool
    {
        return (bool) Note::where('id', $noteId)
            ->where('user_id', Auth::id())
            ->delete();
    }
}
