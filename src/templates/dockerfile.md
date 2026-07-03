# Dockerfile Template (Laravel + Vite, combined web+worker)

Generalized from the proven multi-stage image (graph-portal, 2026-07-03).
Output file: `Dockerfile` at the app repo root.

Load-bearing patterns: three-stage build (vendor → assets → runtime; assets
stage receives `vendor/` because Vite may alias into it), migrations + seed in
the start command (protocol A10), single image serving both web and worker
(platform single-service volume constraint, protocol A12).

```dockerfile
# {app-name} — single image, two processes (web default, worker via start command override)

# --- PHP dependencies ---
FROM composer:2 AS vendor
WORKDIR /build
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-interaction --no-scripts --prefer-dist --optimize-autoloader

# --- Frontend assets (needs vendor: vite may alias packages into vendor/) ---
FROM node:{node-version}-slim AS assets
WORKDIR /build
COPY package.json package-lock.json vite.config.ts tsconfig.json tailwind.config.js ./
COPY resources ./resources
COPY public ./public
COPY --from=vendor /build/vendor ./vendor
RUN npm ci && npm run build

# --- Runtime ---
FROM php:{php-version}-cli-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev unzip \
    && docker-php-ext-install pdo_pgsql pcntl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

{node-in-runtime-block}

WORKDIR /app
COPY . .
COPY --from=vendor /build/vendor ./vendor
COPY --from=assets /build/public/build ./public/build

RUN php artisan storage:link || true

ENV APP_ENV=production

EXPOSE {app-port}

# Web process. Worker service (if split later) overrides the start command:
# php artisan queue:work --tries=1 --timeout={worker-timeout}
CMD ["sh", "-c", "php artisan migrate --force && {seed-command} php artisan serve --host=0.0.0.0 --port=${PORT:-{app-port}}"]
```

## Field Documentation

| Field | Description | Example |
|-------|-------------|---------|
| `{app-name}` | The application | `acme-app` |
| `{node-version}` / `{php-version}` | Runtime versions (match CI) | `22` / `8.3` |
| `{node-in-runtime-block}` | Only if the app spawns Node subprocesses: `COPY --from=assets /usr/local/bin/node /usr/local/bin/node` (+ the env vars its generators need) | omit when unused |
| `{app-port}` | The serve port | `8080` |
| `{seed-command}` | Idempotent boot seed, or empty | `php artisan db:seed --class=Database\\\\Seeders\\\\OwnerSeeder --force &&` |
| `{worker-timeout}` | Queue worker timeout — longer than the slowest job | `1000` |

## Section Specifications

- **Migrations in CMD** make every deploy self-migrating (rehearsed downstream
  first by the ladder — the pipeline guarantees ordering, the image guarantees execution).
- **Combined web+worker**: background the worker in the platform start command
  (`railway-json` template) rather than a second CMD here — one image, one
  source of truth.

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
