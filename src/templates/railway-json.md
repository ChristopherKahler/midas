# railway.json Template

Generalized from the proven deploy config (graph-portal, 2026-07-03).
Output file: `railway.json` at the app repo root.

Load-bearing patterns: Dockerfile builder, migrate+seed+worker+serve combined
start command (protocols A10 + A12), health check on the framework endpoint,
bounded restart policy.

```json
{
    "$schema": "https://railway.app/railway.schema.json",
    "build": {
        "builder": "DOCKERFILE",
        "dockerfilePath": "Dockerfile"
    },
    "deploy": {
        "startCommand": "sh -c 'php artisan migrate --force && {seed-command} ({worker-command} &) && php artisan serve --host=0.0.0.0 --port=${PORT:-{app-port}}'",
        "healthcheckPath": "{health-path}",
        "healthcheckTimeout": 300,
        "restartPolicyType": "ON_FAILURE",
        "restartPolicyMaxRetries": 3
    }
}
```

## Field Documentation

| Field | Description | Example |
|-------|-------------|---------|
| `{seed-command}` | Idempotent boot seed + `&&`, or empty | `php artisan db:seed --class=Database\\\\Seeders\\\\OwnerSeeder --force &&` |
| `{worker-command}` | The queue worker riding in the combined service | `php artisan queue:work --tries=1 --timeout=1000` |
| `{app-port}` | Fallback port when $PORT unset (match Dockerfile EXPOSE) | `8080` |
| `{health-path}` | The framework health endpoint | `/up` |

## Section Specifications

- **startCommand** is the combined-service pattern: when artifacts later move
  to object storage, split the worker into its own service and delete the
  backgrounded `({worker-command} &)` — the Dockerfile already documents the
  worker override.
- **Per-environment settings live in the dashboard, not here:** repo + trigger
  branch, domains, `APP_URL`, Wait-for-CI are configured PER ENVIRONMENT
  (railway.md framework explains why).

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
