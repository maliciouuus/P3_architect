<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\NoteController;
use App\Http\Controllers\Api\TagController;

/*
 * Routes publiques — pas besoin d'être connecté
 * Utilisées par Postman et le frontend React pour s'authentifier
 */
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login',    [AuthController::class, 'login']);

/*
 * Routes protégées — nécessitent un token Sanctum valide
 * Header requis : Authorization: Bearer {token}
 * Le token est retourné par /api/login ou /api/register
 */
Route::middleware('auth:sanctum')->group(function () {

    // Auth
    Route::post('/logout', [AuthController::class, 'logout']);

    // Notes
    Route::get('/notes',         [NoteController::class, 'index']);
    Route::post('/notes',        [NoteController::class, 'store']);
    Route::delete('/notes/{id}', [NoteController::class, 'destroy']);

    // Tags
    Route::get('/tags',  [TagController::class, 'index']);
    Route::post('/tags', [TagController::class, 'store']);
});
