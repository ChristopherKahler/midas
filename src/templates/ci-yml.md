# CI Workflow Template

Generalized from a proven production pipeline (graph-portal, 2026-07-03).
Output file: `.github/workflows/ci.yml` in the app repo.

The load-bearing patterns — keep these when adapting:
- Job chain `test → smoke → post-deploy-smoke` via `needs:` (each gate blocks the next)
- Prod-parity database service in CI
- Smoke against a SERVED production build, with `wait-on` before running
- The secret→env-var step-gating pattern so a missing optional secret SKIPS cleanly
- Trace upload on failure

```yaml
name: CI/CD

on:
  push:
    branches: [dev, stage, main]
  pull_request:
    branches: [dev, stage, main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:{postgres-version}-alpine
        env:
          POSTGRES_USER: {db-user}
          POSTGRES_PASSWORD: {ci-db-password}
          POSTGRES_DB: {db-name}_test
        ports:
          - {ci-db-port}:5432
        options: >-
          --health-cmd "pg_isready -U {db-user}"
          --health-interval 5s
          --health-timeout 5s
          --health-retries 10
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '{php-version}'
          extensions: pdo_pgsql, pgsql
          coverage: none
      - uses: actions/setup-node@v4
        with:
          node-version: '{node-version}'
          cache: npm
      - name: Install PHP dependencies
        run: composer install --no-interaction --prefer-dist
      - name: Prepare app
        run: |
          cp .env.example .env
          php artisan key:generate
      - name: Build frontend
        run: |
          npm ci
          npm run build
      - name: Run test suite
        run: php artisan test

  smoke:
    needs: test
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:{postgres-version}-alpine
        env:
          POSTGRES_USER: {db-user}
          POSTGRES_PASSWORD: {ci-db-password}
          POSTGRES_DB: {db-name}
        ports:
          - {ci-db-port}:5432
        options: >-
          --health-cmd "pg_isready -U {db-user}"
          --health-interval 5s
          --health-timeout 5s
          --health-retries 10
    env:
      APP_ENV: local
      APP_URL: http://127.0.0.1:{ci-app-port}
      DB_CONNECTION: pgsql
      DB_HOST: 127.0.0.1
      DB_PORT: {ci-db-port}
      DB_DATABASE: {db-name}
      DB_USERNAME: {db-user}
      DB_PASSWORD: {ci-db-password}
      SMOKE_BASE_URL: http://127.0.0.1:{ci-app-port}
      SMOKE_EMAIL: {ci-seed-email}
      SMOKE_PASSWORD: {ci-seed-password}
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '{php-version}'
          extensions: pdo_pgsql, pgsql
          coverage: none
      - uses: actions/setup-node@v4
        with:
          node-version: '{node-version}'
          cache: npm
      - name: Install dependencies
        run: |
          composer install --no-interaction --prefer-dist
          npm ci
      - name: Prepare app
        run: |
          cp .env.example .env
          php artisan key:generate
          npm run build
          php artisan migrate --force
          php artisan db:seed --force
      - name: Install Playwright browser
        run: npx playwright install --with-deps chromium
      - name: Serve app
        run: |
          php artisan serve --host=127.0.0.1 --port={ci-app-port} &
          npx wait-on http://127.0.0.1:{ci-app-port}/up --timeout 60000
      - name: Run smoke suite
        run: npm run smoke
      - name: Upload trace on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-trace
          path: test-results/
          retention-days: 5

  # Deploys are handled natively by the platform's GitHub integration
  # (branch-per-environment triggers with "Wait for CI" gating on the
  # test + smoke jobs above). Env-scoped tokens remain available for
  # manual CLI deploys if the integration is ever unavailable.

  post-deploy-smoke:
    needs: smoke
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    # Secrets can't gate a job-level `if`; map to env and gate each step instead,
    # so a missing SMOKE_LIVE_PASSWORD skips cleanly rather than red-failing.
    env:
      SMOKE_LIVE_PASSWORD: ${{ secrets.SMOKE_LIVE_PASSWORD }}
    steps:
      - name: Check for live-smoke password
        id: gate
        run: |
          if [ -n "$SMOKE_LIVE_PASSWORD" ]; then
            echo "enabled=true" >> "$GITHUB_OUTPUT"
          else
            echo "enabled=false" >> "$GITHUB_OUTPUT"
            echo "SMOKE_LIVE_PASSWORD not set — skipping live smoke. Set it with: gh secret set SMOKE_LIVE_PASSWORD -R {github-org}/{repo-name}"
          fi
      - if: steps.gate.outputs.enabled == 'true'
        uses: actions/checkout@v4
      - if: steps.gate.outputs.enabled == 'true'
        uses: actions/setup-node@v4
        with:
          node-version: '{node-version}'
          cache: npm
      - name: Select live URL
        if: steps.gate.outputs.enabled == 'true'
        id: live
        run: |
          case "${GITHUB_REF_NAME}" in
            main)  echo "url={prod-url}"  >> "$GITHUB_OUTPUT" ;;
            stage) echo "url={stage-url}" >> "$GITHUB_OUTPUT" ;;
            dev)   echo "url={dev-url}"   >> "$GITHUB_OUTPUT" ;;
          esac
      - name: Wait for the platform to redeploy, then smoke the live URL
        if: steps.gate.outputs.enabled == 'true'
        env:
          SMOKE_BASE_URL: ${{ steps.live.outputs.url }}
          SMOKE_EMAIL: {live-smoke-email}
          SMOKE_PASSWORD: ${{ secrets.SMOKE_LIVE_PASSWORD }}
        run: |
          npm ci
          npx playwright install --with-deps chromium
          # Give the platform's build+deploy time to publish the new commit.
          sleep 120
          npx wait-on "${SMOKE_BASE_URL}/up" --timeout 180000
          npm run smoke
```

## Field Documentation

| Field | Description | Example |
|-------|-------------|---------|
| `{postgres-version}` | Match the PRODUCTION major version (prod-parity rule) | `17` |
| `{php-version}` / `{node-version}` | The app's runtime versions | `8.3` / `22` |
| `{db-user}` / `{db-name}` | CI database identifiers | `myapp` / `myapp` |
| `{ci-db-password}` | Throwaway CI-only value (never a real credential) | `secret` |
| `{ci-db-port}` / `{ci-app-port}` | Local CI ports | `5434` / `8010` |
| `{ci-seed-email}` / `{ci-seed-password}` | Dev-seed login the smoke uses IN CI ONLY | from the app's DevSeeder |
| `{github-org}/{repo-name}` | For the helpful gh hint text | `acme/acme-app` |
| `{dev-url}` / `{stage-url}` / `{prod-url}` | The per-environment live URLs | platform domains |
| `{live-smoke-email}` | The live smoke login user | a dedicated smoke account |

## Section Specifications

- **test**: prod-parity DB is the point — same engine, same major version.
- **smoke**: must run against a SERVED PRODUCTION BUILD (`npm run build` +
  serve + wait-on), not the dev server — dev servers mask prod-only failures.
- **post-deploy-smoke**: `SMOKE_LIVE_PASSWORD` lives in GitHub secrets, set
  interactively (`gh secret set`, hidden prompt) — never in this file.

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
