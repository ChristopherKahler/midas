# Security Checklist

**Purpose:** Pass/fail gate for the harden task — the nine control domains
distilled to checkable items. Every item needs an evidence pointer (code path,
config key, or log channel); "we do this" without a pointer is a fail.
Fail-closed: an unchecked item is a failed gate.

## Access Control

- [ ] RBAC with least privilege; deny-by-default everywhere — evidence: role/ability definitions
- [ ] Owner transfer flow exists for single-owner constraints — evidence: code path
- [ ] MFA on admin/platform accounts — evidence: account settings (effect, not credentials)
- [ ] Deactivation kills session + tokens + login in one action — evidence: deactivation code path + verified test
- [ ] Tenant isolation enforced in queries, not UI-hiding — evidence: scoped binding/query code

## Authentication & Secrets

- [ ] Secret scan clean: none in code, history, logs, or session workflows — evidence: scan output
- [ ] Env-only injection; interactive provisioning — evidence: masked secret listings
- [ ] Rotation cadence + procedure documented — evidence: ops notes location
- [ ] Spawn sites pass explicit env; outbound calls have timeouts — evidence: spawn-site code
- [ ] Token abilities scoped + org-bound + expirable — evidence: token creation code

## Audit & Logging

- [ ] Dedicated immutable audit channel — evidence: logging config
- [ ] Mutations log actor + action + resource + timestamp — evidence: audit log sample
- [ ] No secret values in logs — evidence: scan of log output
- [ ] Reconstruction test passes (who-did-what-when answerable) — evidence: a reconstructed timeline
- [ ] Retention policy stated — evidence: doc location

## Data Protection

- [ ] TLS end-to-end incl. reverse-proxy trust configured — evidence: proxy-trust config line
- [ ] Sensitive fields encrypted at rest — evidence: encrypted casts/columns
- [ ] Data classification exists — evidence: doc location
- [ ] Deletion path implemented (not just policy) — evidence: deletion code path
- [ ] Backup exists AND restore tested — evidence: restore-test note with date

## Network & Transport

- [ ] Zero mixed content (smoke detector green on https) — evidence: smoke run
- [ ] Security headers (HSTS, X-Content-Type-Options; CSP where practical) — evidence: response headers
- [ ] Rate limiting on auth + expensive endpoints — evidence: limiter config

## Input & Tenant Safety

- [ ] Boundary validation on all inputs — evidence: request validation classes
- [ ] Anti-enumeration: foreign + non-existent = same 404 — evidence: verified probe
- [ ] CSRF via framework router (survives session rotation) — evidence: mutation call sites
- [ ] Whitelist over blacklist for user-supplied identifiers — evidence: validation code

## Change Management

- [ ] Pipeline checklist green (see checklists/pipeline.md) — evidence: its run record
- [ ] Branch protection on prod branch — evidence: repo settings
- [ ] Migrations rehearse downstream — evidence: env migration history

## Vendor / Subprocessor

- [ ] Subprocessor inventory current — evidence: doc location
- [ ] BAAs where PHI flows — evidence: agreement records (existence, not contents)
- [ ] Provider endpoints config-over-code — evidence: env-var connector config

## Availability

- [ ] Health checks + restart policy live — evidence: platform config
- [ ] Rollback exercised; DR posture stated — evidence: ops notes

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
