<security_controls>

## Purpose

The MIDAS security control catalog — the spine vibe-coders skip. Nine domains,
every control pass/fail phrased so the harden task can walk it and the assess
task can score against it. Each control is explained inline; pointers to the
protocol library (protocols.md) are optional deeper context, never required
reading.

## How to Read a Control

Every control is a **binary gate**: the app either satisfies it (with evidence)
or it doesn't. "Mostly" is a fail. This phrasing is deliberate — auditors think
in evidence, not intentions.

## The Nine Domains

### 1. Access Control

- [ ] RBAC with least privilege — roles grant the minimum abilities their job needs
- [ ] Deny-by-default — access starts closed and opens explicitly, everywhere
- [ ] Single-owner constraints have transfer flows — ownership can move without support tickets or DB surgery
- [ ] MFA on admin/platform accounts
- [ ] Session invalidation on deactivation — one action kills session + tokens + login simultaneously (a deactivated user with a live token is not deactivated)
- [ ] Org/tenant isolation enforced in code, not UI-hiding — hiding a nav link is not a control; the query scope is

### 2. Authentication & Secrets

- [ ] No secrets in code, logs, or agent sessions — ever
- [ ] Env-only injection; interactive provisioning (hidden prompts, one token at a time)
- [ ] Rotation cadence documented and followed
- [ ] Explicit spawn environments for child processes (ambient inheritance is an auth bug factory)
- [ ] Passwords hashed (bcrypt/argon2), never reversible
- [ ] API token abilities scoped and org-bound; tokens expirable

### 3. Audit & Logging

- [ ] Dedicated immutable audit channel — application logs are not audit logs
- [ ] Every mutation logs actor + action + resource + timestamp
- [ ] No secret values in logs
- [ ] Logs sufficient to reconstruct "who did what when" after an incident
- [ ] Retention policy stated

**Why "byproduct, not feature":** audit logs emitted as a side effect of doing
ops work correctly exist BEFORE an auditor asks. Retrofitted logging can't
testify about the past.

### 4. Data Protection

- [ ] Encryption in transit — TLS end-to-end, including reverse-proxy trust so the app knows it's behind TLS
- [ ] Encryption at rest for sensitive fields — encrypted casts for tokens/PII
- [ ] Data classification exists (what's PII, what's PHI, what's public)
- [ ] Minimum-necessary collection — the app can't leak what it never stored
- [ ] Retention + deletion policy; deletion path actually implemented
- [ ] Backups exist AND restore has been tested — an untested backup is a hope, not a control

### 5. Network & Transport

- [ ] Deny-by-default egress where feasible
- [ ] TLS enforced; zero mixed content
- [ ] Security headers: HSTS, X-Content-Type-Options, CSP where practical
- [ ] Rate limiting on auth + expensive endpoints

### 6. Input & Tenant Safety

- [ ] Validation at system boundaries
- [ ] Anti-enumeration status codes — foreign and non-existent resources return the SAME 404
- [ ] IDOR prevention via scoped route-model binding — the query scope makes foreign IDs unresolvable, not an `if` check after fetch
- [ ] CSRF protection through the framework router (static-token fetch breaks on session rotation)
- [ ] Whitelist over blacklist for user-supplied identifiers

### 7. Change Management

- [ ] CI test + browser smoke gates on every deploy path
- [ ] Branch protection on the prod branch
- [ ] Deploy approval on prod (merge to main is ceremonial, not casual)
- [ ] Migrations rehearsed downstream (dev→stage) before prod
- [ ] No direct-to-prod work; reviewable diffs for everything

### 8. Vendor / Subprocessor Management

- [ ] Inventory of every third party handling data (host, integrations, providers)
- [ ] Each vendor's data-handling posture noted
- [ ] BAAs in place where PHI flows (see compliance-maps — this one voids HIPAA entirely if missed)
- [ ] Config-over-code so a vendor swap is a variable change, not a release

### 9. Availability

- [ ] Health checks wired to the platform's restart policy
- [ ] Platform structural limits known (e.g., single-service volumes) and the architecture honors them
- [ ] Rollback path documented AND exercised
- [ ] DR/backup posture stated

## Contrast: UI-hiding vs enforced isolation

**Fails the control:** tenant B's records don't appear in tenant A's list view,
but `GET /records/{tenant-B-id}` returns 200 with data. The control was a WHERE
clause in one view.

**Passes the control:** route-model binding scopes every lookup to the
authenticated tenant; the foreign ID resolves to 404 — indistinguishable from
non-existent (anti-enumeration for free).

## Anti-Patterns

| Anti-Pattern | Why It Fails Review |
|--------------|---------------------|
| "We'll harden before launch" | Retrofitting is the #1 failure mode; controls woven in are cheaper than controls bolted on |
| App logs as audit trail | Mutable, rotated, mixed with noise — can't reconstruct an incident |
| 403 on foreign resources | Enumerable tenancy |
| Backup never restored | Schrödinger's DR |
| "Admin will remember to deactivate" | Controls that depend on memory aren't controls |

## Source

Catalog assembled from the graph-portal hardening pass; every control was either
implemented or consciously gated there.

</security_controls>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
