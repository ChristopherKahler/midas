# Dry-Run: assess + pipeline guidance vs graph-portal ground truth

**Date:** 2026-07-03 · **Mode:** read-only · **App:** ~/chris-ai-systems/apps/graph-portal

## Method

Walked assess.md's inventory steps and pipeline.md's wiring guidance against the
app whose ops decisions we lived. Each row: what the task guidance expects → what
the app actually has → verdict.

## Findings

| Guidance | Ground Truth | Verdict |
|----------|-------------|---------|
| pipeline: test job → smoke job → deploy gating chain | `ci.yml`: `test` → `smoke` (needs: test) → `post-deploy-smoke` (needs: smoke) | **Match** |
| pipeline/railway: migrate + seed + worker + serve combined start command | `railway.json` startCommand: `migrate --force && db:seed OwnerSeeder && (queue:work &) && serve` | **Match** (A10 + A12 exactly as codified) |
| railway: health check on /up, restart policy | `healthcheckPath: "/up"`, `ON_FAILURE` ×3 | **Match** |
| smoke: serial execution, one worker | `playwright.config.ts`: `fullyParallel: false, workers: 1` | **Match** (testing-gates design rule) |
| smoke: tests restoring mutated global state | `permissions.smoke.ts` flips graphs.generate Off → verifies → restores Default | **Match** |
| A9/deny-by-default: dark features 404 and smoke skips cleanly | permissions spec: pane 404 on live until release → `test.skip`, "rather than red-failing a healthy dark deploy" | **Match** (guidance literally implemented) |
| A1: trustProxies behind TLS edge | `bootstrap/app.php:19`: `$middleware->trustProxies(at: '*')` | **Match** |
| smoke.md references template path `tests/e2e/smoke.spec.ts` as example location | graph-portal uses `tests/smoke/*.smoke.ts` with `testDir: './tests/smoke'` | **Task gap (minor):** example path was invented; guidance should defer to the app's playwright `testDir` convention. Fixed in smoke.md. |
| assess inventory: CI files | ci.yml + lint.yml + tests.yml (tests.yml triggers `ci`) | Match — inventory step reads workflows plural, correct |

## Task Gaps (fixed now)

1. `smoke.md` output example location updated to defer to the app's existing
   Playwright `testDir` convention instead of a hardcoded example path.

## App Findings (parked for Phase 6 dogfood)

- `SMOKE_EMAIL`/`SMOKE_PASSWORD` have in-repo fallback defaults in the spec —
  dev-seed credentials, not production secrets, but assess's secrets scan should
  flag seeded-credential defaults for review. Park for dogfood scoring.

## Verdict

Guidance matches lived reality 8/9; the one mismatch was in the task's example
text, not its principles — fixed before phase close.
