FROM php:8.4-cli

RUN apt-get update --fix-missing && apt-get install -y \
    git curl zip unzip libzip-dev libsqlite3-dev \
    && docker-php-ext-install pdo pdo_sqlite zip \
    && apt-get clean

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

COPY . .

RUN composer update --no-interaction
RUN php artisan key:generate --force
RUN touch database/database.sqlite
RUN php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider" --force
RUN php artisan migrate --force

EXPOSE 8000

CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
