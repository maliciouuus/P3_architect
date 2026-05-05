FROM php:8.4-cli

RUN apt-get update && apt-get install -y \
    git curl zip unzip libzip-dev libsqlite3-dev nodejs npm \
    && docker-php-ext-install pdo pdo_sqlite zip \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apt-get clean

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

COPY . .

RUN composer install --no-interaction
# --legacy-peer-deps contourne les conflits de versions entre les packages npm
RUN npm install --legacy-peer-deps
RUN php artisan key:generate --force
RUN touch database/database.sqlite
RUN php artisan migrate --force

EXPOSE 8000

CMD ["sh", "-c", "npm run build && php artisan serve --host=0.0.0.0 --port=8000"]
