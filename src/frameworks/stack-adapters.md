<stack_adapters>

## Purpose

The universal/stack-specific split — which MIDAS principles apply to every stack
unchanged, and the adapter interface that expresses each principle in a specific
framework's API. Loaded by tasks whenever they touch app code (pipeline, smoke,
harden).

## The Split

**Universal (every stack, no variation):** the env ladder · deny-by-default ·
secrets discipline · audit logging · the CI test+smoke gate philosophy ·
migration rehearsal · the compliance crosswalk · reverse-proxy TLS trust (any
TLS-terminating edge) · anti-enumeration.

These are *principles*, and they do not vary by stack. What varies is only the
API used to express them. This distinction is load-bearing: when someone says
"but we're on Django," the answer is "same principles, different adapter" — the
posture requirements never relax.

**Stack-specific (the adapter):** the exact mechanism per principle, below.

## The Adapter Interface

An adapter answers these questions for its stack:

| Principle | The Adapter Must Specify |
|-----------|--------------------------|
| Reverse-proxy TLS trust | How the app is told it's behind a TLS edge |
| CSRF-through-router | The mutation mechanism that keeps CSRF tokens fresh across session rotation |
| Encrypted at-rest fields | The encrypted-cast / field-encryption mechanism |
| Tenant-scoped lookups | The scoped binding/query mechanism that 404s foreign IDs |
| Config fallbacks | The empty-string-safe env read idiom |
| Health endpoint | The route the platform health check hits |
| Migration ordering | How schema-change ordering is guaranteed |

## Adapter: Laravel + Inertia + Vue (the proven default)

MIDAS's opinionated default stack — proven end-to-end on Railway with Postgres.

| Principle | Laravel + Inertia Mechanism |
|-----------|----------------------------|
| Reverse-proxy TLS trust | `trustProxies('*')` in bootstrap + force HTTPS in production |
| CSRF-through-router | Inertia `router.put/post/delete` — never raw `fetch()` with the meta-tag token |
| Encrypted at-rest fields | `'token' => 'encrypted'` casts on models holding secrets/PII |
| Tenant-scoped lookups | Scoped route-model binding — bindings resolve through the authenticated org's relation; foreign IDs 404 |
| Config fallbacks | `env('X') ?: $default` — never `env('X', $default)` (empty string defeats the second arg) |
| Health endpoint | `/up` (built-in) |
| Migration ordering | Timestamped filenames — an add-column migration must be dated AFTER the published create-table it alters |

**Contrast (the two idioms that look interchangeable and aren't):**

```php
// BROKEN under partial env (CI's .env.example sets OWNER_EMAIL=""):
'owner' => env('OWNER_EMAIL', 'admin@app.test')   // "" is "set" → default never fires

// DEFENSIVE:
'owner' => env('OWNER_EMAIL') ?: 'admin@app.test' // "" is falsy → default fires
```

## Adapter Sketches (interface proof — expand when an app lands on the stack)

| Principle | Express/Node | Django |
|-----------|--------------|--------|
| Reverse-proxy TLS trust | `app.set('trust proxy', true)` | `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` |
| CSRF-through-router | csurf-style middleware with per-request token fetch, or same-site session pattern | Django forms/middleware CSRF with rotating token |
| Encrypted at-rest fields | Field-level encryption lib or KMS-backed columns | `django-encrypted-model-fields` or equivalent |
| Tenant-scoped lookups | Query middleware scoping every lookup to `req.org` | Custom manager: `Model.objects.for_org(request.org)` |
| Config fallbacks | `process.env.X || defaultVal` (empty string falsy — safe by accident; still write it deliberately) | `os.environ.get('X') or default` |
| Health endpoint | Explicit `/healthz` route checking DB | `/healthz` view with DB ping |

These sketches prove the interface generalizes; a full adapter lands when a real
app on that stack goes through MIDAS (dogfood-first, like the Laravel adapter).

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|--------------|-------------|
| "Our stack doesn't need X" | Principles are universal; only mechanisms vary. A stack without proxy-trust config still serves mixed content behind an edge |
| Porting mechanisms literally across stacks | `trustProxies('*')` means nothing in Django; port the PRINCIPLE via the adapter row |
| Writing adapters speculatively | Untested adapters are theory; MIDAS adapters are proven on real apps first |
| Relaxing a control because the stack makes it awkward | The control catalog is stack-independent; awkward ≠ optional |

## Source

Laravel adapter proven in the graph-portal build; interface derived from it.

</stack_adapters>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
