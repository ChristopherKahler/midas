<railway_opinions>

## Purpose

MIDAS's Railway-specific opinions — the platform facts and configurations proven
in live builds. Tasks load this when provisioning, wiring pipelines, or deploying
on Railway. These are opinions in the strong sense: MIDAS configures Railway this
way unless the operator overrides with a reason.

## The Opinions

### Source repo + trigger branch are per-ENVIRONMENT settings

Connect the GitHub repo **in each environment**, each with its own trigger branch
(dev/stage/main ↔ dev/stage/prod). **Why:** Railway environments are siblings,
not inheritors — an env without its own repo connection silently never deploys
from pushes, and you'll stare at a green pipeline wondering why prod is stale.

### Volumes are single-service

A Railway volume attaches to exactly ONE service. Until artifact storage moves to
object storage (R2/S3), web + worker run **combined in one service**. **Why:**
splitting them with a shared-volume assumption produces an architecture the
platform silently won't honor (protocol A12). Moving artifacts to object storage
is what re-enables the web/worker split.

### "Wait for CI" gates deploys on GitHub checks

Enable Wait for CI so Railway's native deploy holds until the GitHub checks
(tests + browser smoke) are green. **Why:** this is the machine-verified-truth
gate — without it, Railway deploys on push regardless of what CI thinks.

### Env-scoped project tokens for CLI deploys

One token per environment (`RAILWAY_TOKEN_DEV`, `RAILWAY_TOKEN_STAGE`,
`RAILWAY_TOKEN_PROD`), provisioned interactively, never printed. **Why:** a
single almighty token means any pipeline job can touch prod; env-scoping makes
each env's deploy capability separately grantable and revocable.

### Native GitHub integration over CLI uploads

Install the Railway GitHub app on the org and use native integration for
deploys. **Why:** CLI uploads show **no repo source** in the dashboard —
deploys become untraceable to commits, which fails change-management evidence.
CLI (with env-scoped tokens) is the fallback, not the default.

### railway.json runs the combined start command

For the combined web+worker service, the start command runs migrate + seed +
worker + serve. **Why:** migrations auto-run on every deploy (protocol A10) and
the worker rides along until the object-storage split.

### Per-env domains, per-env APP_URL

Each environment gets its own domain, and `APP_URL` + OAuth redirect URIs are
set per env. **Why:** a stage app generating prod URLs (or vice versa) breaks
signed URLs, OAuth callbacks, and asset generation in ways that only surface in
browsers (see protocol A1's diagnosis trap).

### Health check on /up

Point Railway's health check at the framework's health endpoint (`/up` in
Laravel). **Why:** restart policy + health checks are the availability floor;
a deploy that boots but can't serve should never be marked healthy.

## Contrast: the two ways teams get Railway wrong

**Under-configured:** one environment, repo connected once, no Wait for CI, one
token in a `.env` file. Ships fast; unauditable; first bad migration lands on
prod data.

**MIDAS-configured:** three isolated envs each with repo+branch+domain+URL,
Wait for CI on, env-scoped tokens provisioned interactively, migrations
rehearsed downstream first. Same platform, audit-defensible.

## Anti-Patterns

| Anti-Pattern | Consequence |
|--------------|-------------|
| Connecting the repo only in one env | Other envs never auto-deploy; drift |
| Shared database across envs | Stage rehearsal mutates prod data — the ladder is theater |
| CLI-only deploys | Dashboard shows no source; change evidence gone |
| One global token | Prod deploy capability everywhere; revocation is all-or-nothing |
| Health check on `/` | Marketing page 200s while the app layer is down |

## Source

Proven in the graph-portal Railway deployment (2026-07-03).

</railway_opinions>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
