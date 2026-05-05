<?php

namespace App\Services;

use App\Models\Tag;

/**
 * TagService — contient toute la logique métier liée aux tags.
 * Respecte le principe S de SOLID : une seule responsabilité (gérer les tags).
 * Injecté dans TagController via l'injection de dépendances Laravel (principe D).
 */
class TagService
{
    /**
     * Retourne tous les tags disponibles dans l'application.
     * Les tags ne sont pas liés à un utilisateur : ils sont globaux.
     */
    public function getAll(): \Illuminate\Database\Eloquent\Collection
    {
        return Tag::all();
    }

    /**
     * Crée un nouveau tag.
     * La validation (unicité, longueur) est faite en amont dans le contrôleur.
     *
     * @param array $data  Doit contenir 'name'
     */
    public function create(array $data): Tag
    {
        return Tag::create(['name' => $data['name']]);
    }
}
