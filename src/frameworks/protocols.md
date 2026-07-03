<codified_protocols>

## Purpose

The MIDAS protocol library — hard-won operational rules proven in live
enterprise-grade builds (origin: the graph-portal/MeetCaddy build, 2026-07-03).
Each protocol records the **rule**, the **failure it prevents** (a real one, not
hypothetical), and the **compliance control it satisfies**. Tasks load this file
when applying or checking any of these rules; the harden and assess tasks walk it
end to end.

**This file is the LIVING canonical protocol library.** The planning doc that
seeded it (devops-security-framework Doc 2 §A) is a historical snapshot — new
protocols land HERE first, then a checklist line, then `base learn`.

## The Protocols

### A1. Reverse-proxy TLS trust

**Rule:** Set `trustProxies('*')` (or the stack equivalent) + force HTTPS in
production whenever the app runs behind a TLS-terminating edge — Railway,
Cloudflare, any PaaS.

**Failure it prevents:** The mixed-content blank screen. The edge terminates TLS
and forwards plain HTTP; the app, seeing HTTP, generates `http://` asset URLs;
browsers block those on an HTTPS page. The page serves 200 to curl and every
automated check — and renders white in every real browser.

**Control satisfied:** Availability, Processing Integrity.

**Diagnosis trap (codified):** curl does not enforce mixed-content policy, and
checking asset *paths* instead of full *URLs* hides the scheme bug. A smoke test
in a real browser is the only reliable catch.

**Contrast:**
- *Wrong confidence:* "curl returns 200 and the HTML has the right asset paths — deploy is fine."
- *Right check:* headless browser loads the page over https, fails on any mixed-content block or empty app mount.

### A2. CSRF survives session rotation

**Rule:** SPA mutations go through the framework's router (e.g., Inertia
`router.put`), never a raw `fetch()` carrying a static meta-tag CSRF token.

**Failure it prevents:** 419s after login. The session token rotates on auth;
the meta tag snapshotted at page load no longer matches; every subsequent
mutation is rejected. Unit tests never see it because they don't rotate sessions
mid-page.

**Control satisfied:** Security (CSRF protection).

### A3. Browser smoke gate is mandatory

**Rule:** Every pipeline runs a headless-browser smoke that logs in, walks every
route, and fails on **four detectors**: console errors · mixed-content blocks ·
non-2xx same-origin XHR (419/500) · an empty app mount (`#app` empty = a render
error unit tests never see).

**Failure it prevents:** The entire class of "passes 107 tests, blank in the
browser" bugs — a missing `ref` import, a mixed-content block, a CSRF break.

**Control satisfied:** Processing Integrity, Change Management.

**Design notes (codified):**
- Run smoke **serial** — shared server + global flag state races under parallel
- Tests that mutate global state must restore it
- Scope failure detectors to **app-origin** — a third-party CDN hiccup is not your bug
- The mixed-content check only applies when the page itself is https

### A4. Explicit spawn environment for child processes

**Rule:** When a job spawns a subprocess (generator, CLI), pass an EXPLICIT
environment. Never rely on ambient env inheritance. Add a timeout to every
outbound provider call.

**Failure it prevents:** Execution-context auth failures — a child spawned by a
differently-launched parent inherits stale/absent env and 401s while the same
command succeeds in an interactive shell (the graph-portal Notion 401 class).
The timeout prevents an untimed provider call from hanging a user-facing flow
forever (the OAuth popup white-screen).

**Control satisfied:** Confidentiality (credential isolation).

### A5. Secrets never touch code, logs, or the session

**Rule:** Provision secrets interactively (`gh secret set` with hidden prompts;
platform dashboard tokens copied one at a time). Inject via env only. Never
echo, never commit, never paste into an agent session.

**Failure it prevents:** Secret leakage into history/logs/transcripts, and the
lockdown that follows.

**Control satisfied:** Confidentiality, Security (secrets management).

**Codified specifics:**
- Environment-scoped deploy tokens (`RAILWAY_TOKEN_{ENV}`) gate each env separately
- A missing *optional* secret must SKIP its job cleanly, never red-fail — map
  secret→env var, gate the step on the env var, because job-level `if:` cannot
  read `secrets` context directly

### A6. Config over code for provider endpoints (the connector protocol)

**Rule:** Every OAuth/provider integration exposes `client_id`, `client_secret`,
`redirect`, `authorize_url`, `token_url` as env vars (endpoints defaulted to
current provider values). Controllers never hardcode a provider URL.

**Failure it prevents:** A code change + redeploy every time an OAuth app is
swapped or a provider moves an endpoint.

**Control satisfied:** Change Management, Vendor Management.

### A7. User-consented scope changes only

**Rule:** The platform can never silently widen its own data access. Scope
(which boards/records a connection sees) changes only through user-consented
provider re-authorization — never a server-side grant. Reflect current scope
read-only via the provider's own API.

**Failure it prevents:** Unauthorized data-access expansion — the thing an
enterprise security reviewer probes first.

**Control satisfied:** Confidentiality, Privacy, HIPAA minimum-necessary.

### A8. Anti-enumeration status codes

**Rule:** Foreign and non-existent resources return the SAME status (404).
403 is reserved for "authenticated but lacks the specific ability."

**Failure it prevents:** Tenant/resource enumeration — a 403-vs-404 split tells
an attacker which IDs exist.

**Control satisfied:** Security, Confidentiality.

### A9. Deny-by-default feature exposure

**Rule:** Features ship dark — 404 when disabled, indistinguishable from
non-existent — and are released deliberately via a code-defined flag registry.
Release flags are globally scoped: one source of truth for definition +
enforcement + UI.

**Failure it prevents:** Accidental exposure of half-built surfaces.

**Control satisfied:** Change Management.

### A10. Migrations rehearse downstream, run automatically, never on prod first

**Rule:** Migrations run automatically on every deploy but reach dev→stage
before prod, so schema changes are proven against real (disposable) data before
touching precious data. Migration file ordering matters: an add-column migration
must sort AFTER the published create-table it alters.

**Failure it prevents:** Prod schema failures, and fresh-DB builds that break
because file ordering doesn't match dependency ordering.

**Control satisfied:** Availability, Processing Integrity.

### A11. Defensive config fallbacks

**Rule:** `env('X') ?: default`, not `env('X', default)`.

**Failure it prevents:** An empty-string env var (e.g., from `.env.example` in
CI) is "set", so the second-arg default never fires — the owner-seed collapse:
config silently resolves to `""` and downstream logic misbehaves with no error.

**Control satisfied:** Processing Integrity.

**Contrast:**
- *Broken:* `env('OWNER_EMAIL', 'admin@app.test')` → CI's empty string wins, seed creates an owner with an empty email.
- *Defensive:* `env('OWNER_EMAIL') ?: 'admin@app.test'` → empty string is falsy, the default fires.

### A12. Single-service constraint awareness

**Rule:** Know your platform's structural limits before designing the deploy
architecture. Railway volumes attach to ONE service — web+worker run combined
until artifact storage moves to object storage (R2/S3), which re-enables the split.

**Failure it prevents:** A deploy architecture the platform silently won't honor.

**Control satisfied:** Availability.

## Anti-Patterns

| Anti-Pattern | Why It Fails | The Protocol |
|--------------|-------------|--------------|
| "Tests pass, ship it" | Unit suites structurally can't see proxy, CSRF-rotation, or render-layer bugs | A1, A2, A3 |
| Trusting ambient env in spawned jobs | Works interactively, 401s in production spawn contexts | A4 |
| Pasting a token into a session "just this once" | It's now in the transcript forever | A5 |
| Hardcoded provider URLs | Vendor swap = code change + redeploy | A6 |
| 403 for foreign resources | Confirms existence to attackers | A8 |
| Feature flags checked in UI only | The API surface is still exposed | A9 |
| Migrating prod first "because it's urgent" | Schema failure lands on precious data | A10 |

## The Growth Contract

This library GROWS. Every future MIDAS run that fixes a novel ops bug appends a
protocol here — same format: Rule / Failure it prevents / Control satisfied —
plus one line in the relevant checklist and a `base learn` entry. The
framework's value compounds precisely because nothing learned is ever re-learned.

## Source

Proven live in the graph-portal build (2026-07-03) — every protocol above
corresponds to a bug actually hit or a control actually implemented, not theory.

</codified_protocols>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
