<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        api: __DIR__.'/../routes/api.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        // Rien à ajouter — Sanctum gère l'auth via Bearer token, pas de session cookie
    })
    ->withExceptions(function (Exceptions $exceptions) {
        //
    })->create();
