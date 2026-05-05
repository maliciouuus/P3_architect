<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Hash;

/**
 * AuthController — gère l'authentification via Sanctum.
 *
 * Les tokens sont stockés dans la table personal_access_tokens.
 * Le client (Postman, React) reçoit le token dans la réponse et
 * doit l'envoyer dans chaque requête via : Authorization: Bearer {token}
 */
class AuthController extends Controller
{
    /**
     * POST /api/register
     * Crée un compte et retourne un token Sanctum.
     *
     * Body : { "name": "...", "email": "...", "password": "..." }
     * Retourne : { "status": "success", "token": "1|abc...", "user": {...} }
     */
    public function register(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name'     => 'required|string|max:255',
            'email'    => 'required|email|unique:users,email',
            'password' => 'required|string|min:8',
        ]);

        $user  = User::create([
            'name'     => $validated['name'],
            'email'    => $validated['email'],
            'password' => Hash::make($validated['password']),
        ]);

        // Crée un token Sanctum — stocké dans personal_access_tokens
        $token = $user->createToken('api-token')->plainTextToken;

        return response()->json([
            'status' => 'success',
            'token'  => $token,
            'user'   => $user,
        ], 201);
    }

    /**
     * POST /api/login
     * Vérifie les identifiants et retourne un token Sanctum.
     *
     * Body : { "email": "...", "password": "..." }
     * Retourne : { "status": "success", "token": "2|xyz...", "user": {...} }
     */
    public function login(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'email'    => 'required|email',
            'password' => 'required|string',
        ]);

        $user = User::where('email', $validated['email'])->first();

        if (!$user || !Hash::check($validated['password'], $user->password)) {
            return response()->json([
                'status'  => 'error',
                'message' => 'Identifiants invalides.',
            ], 401);
        }

        // Supprime les anciens tokens pour éviter l'accumulation
        $user->tokens()->delete();

        // Crée un nouveau token — visible dans personal_access_tokens
        $token = $user->createToken('api-token')->plainTextToken;

        return response()->json([
            'status' => 'success',
            'token'  => $token,
            'user'   => $user,
        ]);
    }

    /**
     * POST /api/logout
     * Révoque le token actuel (le supprime de personal_access_tokens).
     * Nécessite : Authorization: Bearer {token}
     */
    public function logout(Request $request): JsonResponse
    {
        // Supprime uniquement le token utilisé pour cette requête
        $request->user()->currentAccessToken()->delete();

        return response()->json([
            'status'  => 'success',
            'message' => 'Déconnecté.',
        ]);
    }
}
