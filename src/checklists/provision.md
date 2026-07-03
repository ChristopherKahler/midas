# Provision Checklist

**Purpose:** Pass/fail gate for the provision task — an environment ladder is
only real if every tier is isolated and reachable. Fail-closed: an unchecked
item is a failed gate.

## Environment Ladder

- [ ] Three environments exist (dev/stage/prod) or fewer with a stated reason — evidence: platform project view
- [ ] Each environment has its OWN database; no shared data stores across tiers — evidence: per-env DB connection config read from the platform, not assumed
- [ ] GitHub repo connected IN EACH environment with the correct trigger branch — evidence: per-env service source settings
- [ ] Service shape honors platform constraints (e.g., single-service volume ⇒ combined web+worker) — evidence: service topology vs volume attachments

## Domains & URLs

- [ ] Per-environment domain assigned — evidence: platform domain settings
- [ ] `APP_URL` matches THIS env's domain in every environment — evidence: env var listing (names/values of non-secret config)
- [ ] OAuth redirect URIs registered per environment — evidence: provider app settings

## Health & Availability

- [ ] Health check points at the app's health endpoint (e.g. `/up`) in every env — evidence: deploy config
- [ ] Restart policy set (on-failure with bounded retries) — evidence: deploy config
- [ ] Each environment boots and health-checks green — evidence: live check per env

## Deny-by-Default Posture

- [ ] Nothing publicly exposed except the web service's domain — evidence: platform networking view
- [ ] Databases/workers have no public networking — evidence: platform networking view

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
