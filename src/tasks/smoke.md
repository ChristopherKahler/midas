<purpose>
Author the app-specific browser smoke gate: a Playwright spec that logs in,
walks every route, and fails on the four detectors — console errors,
mixed-content blocks, non-2xx same-origin XHR, and an empty app mount. This is
the gate that catches what unit suites structurally cannot see.
</purpose>

<user-story>
As a builder whose 107 green tests once shipped a blank page, I want a browser
gate that fails on the render/proxy/CSRF layer, so that "it passed CI" actually
means "it works in a browser."
</user-story>

<when-to-use>
- The pipeline task routes here (smoke spec is a prerequisite of the smoke gate)
- An app's routes changed materially and the smoke needs re-authoring
- Entry point routes here via `/midas smoke`
</when-to-use>

<context>
@~/.base-frameworks/midas/context/app-registry.md
</context>

<references>
@~/.base-frameworks/midas/frameworks/testing-gates.md (the detectors + design rules — load first)
@~/.base-frameworks/midas/templates/smoke.spec.ts (the proven starting spec)
</references>

<steps>

<step name="map_routes" priority="first">
Enumerate the app's walkable surface:

1. Extract the route list from the app (router files, route:list command —
   read the app, don't guess)
2. Identify the auth path the smoke will use (test user seeding, login flow)
3. Flag routes that mutate global state (feature toggles, settings) — these
   need state restoration in the spec

Present the route walk plan. **Wait for operator confirmation** (they know
which routes are load-bearing).
</step>

<step name="author_spec">
Load @~/.base-frameworks/midas/frameworks/testing-gates.md and start from
@~/.base-frameworks/midas/templates/smoke.spec.ts.

The spec must implement all four detectors, each scoped to app-origin:
1. **Console errors** — collect per page; any app-origin error fails
2. **Mixed content** — only when the page itself is https (teach: curl can't
   catch this class at all; only a real browser enforces mixed-content policy)
3. **Non-2xx same-origin XHR** — 419 means CSRF rotation broke; 500 means the
   page swallowed a server error
4. **Empty app mount** — `#app` (or the app's mount selector) with no children
   = the SPA never rendered; a 200 with an empty mount is a FAIL, not an uptime win

Design rules from the framework (non-negotiable):
- Serial execution — parallel runners race on shared server/flag state
- Any test that mutates a global restores it
- Third-party noise never fails the gate
</step>

<step name="run_against_prod_build">
Gate the spec locally before wiring it:

1. Build the production bundle
2. Serve it (the same way CI will)
3. Run the smoke — it must pass green against the served prod build

<if condition="smoke fails">
Every failure here is a REAL finding the unit suite missed. Diagnose with the
framework's detector table, fix the app (or the spec's route map if the route
genuinely moved), and re-run. Do not weaken a detector to get to green — that
deletes the gate's reason to exist.
</if>
</step>

<step name="wire_and_record" priority="last">
1. Hand the green spec to the pipeline wiring (pre-deploy job + post-deploy
   live variant) — `/midas pipeline` owns that wiring
2. Run `~/.base-frameworks/midas/checklists/pre-deploy.md` items that concern
   the smoke; fail-closed if the checklist is missing
3. Note the smoke's existence in `~/.base-frameworks/midas/context/{app}/`
   and `base learn` any novel detector finding; new failure class → protocols.md
   per the growth contract
4. PAUL sync: if the app has `.paul/phases/MIDAS-*` folders, flip any finding
   this run closed to `RESOLVED ({date} — {evidence})` in its CONTEXT.md and
   update its STATE.md notice row (per tasks/paul-export.md)
</step>

</steps>

<output>
## Artifact
Playwright smoke spec in the app repo — placed per the app's existing Playwright
`testDir` convention (e.g. graph-portal uses `tests/smoke/*.smoke.ts`; don't
impose a different layout on an app that has one) — green against a served prod
build, implementing all four detectors serial + app-origin scoped.

## Location
App repo; run notes under `~/.base-frameworks/midas/context/{app}/`.
</output>

<acceptance-criteria>
- [ ] Route map extracted from the app and confirmed by the operator
- [ ] All four detectors implemented, app-origin scoped
- [ ] Serial execution; global-state tests restore state
- [ ] Mixed-content check https-conditional
- [ ] Green against a locally served production build
- [ ] No detector weakened to force green
- [ ] Findings logged; novel classes appended to protocols.md
</acceptance-criteria>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
