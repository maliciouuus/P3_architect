<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\TagService;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

/**
 * TagController — gère les requêtes HTTP de l'API REST pour les tags.
 *
 * Rôle (MVC) : reçoit la requête, délègue au TagService, renvoie du JSON.
 * Aucune logique métier ici (principe S de SOLID).
 *
 * TagService est injecté automatiquement par Laravel (principe D).
 */
class TagController extends Controller
{
    /**
     * Le service est injecté dans le constructeur.
     * Couplage faible : le contrôleur dépend de l'interface, pas de l'implémentation.
     */
    public function __construct(private TagService $tagService) {}

    /**
     * GET /api/tags
     * Retourne la liste de tous les tags disponibles.
     */
    public function index(): JsonResponse
    {
        $tags = $this->tagService->getAll();

        return response()->json([
            'status' => 'success',
            'data'   => $tags,
        ]);
    }

    /**
     * POST /api/tags
     * Crée un nouveau tag.
     *
     * Body attendu (JSON) :
     * {
     *   "name": "Travail"
     * }
     */
    public function store(Request $request): JsonResponse
    {
        // La validation est à la frontière (contrôleur), pas dans le service
        $validated = $request->validate([
            'name' => 'required|string|max:50|unique:tags,name',
        ]);

        $tag = $this->tagService->create($validated);

        return response()->json([
            'status'  => 'success',
            'message' => 'Tag créé.',
            'data'    => $tag,
        ], 201);
    }
}
