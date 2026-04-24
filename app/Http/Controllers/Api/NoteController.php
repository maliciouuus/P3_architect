<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\NoteService;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

/**
 * NoteController — gère les requêtes HTTP de l'API REST pour les notes.
 *
 * Rôle (MVC) : reçoit la requête, délègue au service, renvoie une réponse JSON.
 * Il ne contient PAS de logique métier (principe S de SOLID).
 *
 * NoteService est injecté automatiquement par Laravel (principe D — Dependency Inversion).
 */
class NoteController extends Controller
{
    /**
     * Le service est injecté dans le constructeur.
     * Le contrôleur ne sait pas comment NoteService est construit → couplage faible.
     */
    public function __construct(private NoteService $noteService) {}

    /**
     * GET /api/notes
     * Retourne toutes les notes de l'utilisateur connecté avec leur tag.
     */
    public function index(): JsonResponse
    {
        $notes = $this->noteService->getAllForUser();

        return response()->json([
            'status' => 'success',
            'data'   => $notes,
        ]);
    }

    /**
     * POST /api/notes
     * Crée une nouvelle note pour l'utilisateur connecté.
     *
     * Body attendu (JSON) :
     * {
     *   "text":   "Mon texte",
     *   "tag_id": 1
     * }
     */
    public function store(Request $request): JsonResponse
    {
        // La validation est dans le contrôleur (frontière système) : pas dans le service
        $validated = $request->validate([
            'text'   => 'required|string',
            'tag_id' => 'required|exists:tags,id',
        ]);

        $note = $this->noteService->create($validated);

        return response()->json([
            'status'  => 'success',
            'message' => 'Note créée.',
            'data'    => $note->load('tag'),
        ], 201);
    }

    /**
     * DELETE /api/notes/{id}
     * Supprime une note appartenant à l'utilisateur connecté.
     * Retourne 404 si la note n'existe pas ou n'appartient pas à l'utilisateur.
     */
    public function destroy(int $id): JsonResponse
    {
        $deleted = $this->noteService->delete($id);

        if (!$deleted) {
            return response()->json([
                'status'  => 'error',
                'message' => 'Note introuvable ou accès refusé.',
            ], 404);
        }

        return response()->json([
            'status'  => 'success',
            'message' => 'Note supprimée.',
        ]);
    }
}
