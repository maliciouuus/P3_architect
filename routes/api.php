<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\NoteController;
use App\Http\Controllers\Api\TagController;

/*
 * Routes API REST — toutes protégées par le middleware 'auth:sanctum'.
 * Seul un utilisateur authentifié peut accéder à ces endpoints.
 *
 * Convention REST appliquée :
 *   GET    → lecture
 *   POST   → création
 *   DELETE → suppression
 *
 * Toutes les réponses sont en JSON avec le format :
 * { "status": "success"|"error", "data": ..., "message": ... }
 */
/*
 * Le middleware 'auth' utilise la session web de Laravel.
 * Cela fonctionne avec les cookies de session existants (pas besoin de Sanctum ici).
 * Pour une API consommée par un client externe, on ajouterait Sanctum ou JWT.
 */
// 'auth:web' force le guard session cookie — les appels viennent du navigateur connecté
Route::middleware('auth:web')->group(function () {

    /*
     * NOTES
     * GET    /api/notes      → liste les notes de l'utilisateur connecté
     * POST   /api/notes      → crée une nouvelle note
     * DELETE /api/notes/{id} → supprime une note (si elle appartient à l'utilisateur)
     */
    Route::get('/notes',        [NoteController::class, 'index']);
    Route::post('/notes',       [NoteController::class, 'store']);
    Route::delete('/notes/{id}',[NoteController::class, 'destroy']);

    /*
     * TAGS
     * GET  /api/tags  → liste tous les tags
     * POST /api/tags  → crée un nouveau tag
     */
    Route::get('/tags',  [TagController::class, 'index']);
    Route::post('/tags', [TagController::class, 'store']);
});
