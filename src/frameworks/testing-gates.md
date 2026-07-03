<testing_gates>

## Purpose

The MIDAS gate taxonomy — which machine-verified checks stand between code and
each environment, and how to build the browser smoke gate that catches the bugs
unit suites structurally cannot see. Loaded by the pipeline and smoke tasks.

## The Gate Taxonomy

A deploy is gated by machine-verified truth, not hope. The ladder of gates:

| Gate | Runs | Catches | Cannot Catch |
|------|------|---------|--------------|
| 1. Unit/feature tests | CI, prod-parity DB | Logic errors, contract breaks | Anything in the browser/proxy layer |
| 2. Browser smoke (pre-deploy) | CI, headless browser vs served prod build | Render errors, CSRF breaks, console errors, mixed content (locally simulated) | Live-infra drift |
| 3. Wait-for-CI | Platform deploy hold | A deploy racing ahead of red checks | — |
| 4. Live smoke (post-deploy) | Against the real env URL | Proxy-layer drift, TLS/mixed-content in real infra, env-specific config rot | — |

**Why four layers:** each catches a class the previous one structurally cannot.
The graph-portal build proved layers 1 and 2 are NOT redundant twice in one
morning: 107 green unit tests, blank page in every browser.

## The Four Smoke Failure Detectors

The smoke logs in, walks every route, and fails on:

1. **Console errors** — a missing `ref` import throws only at render time
2. **Mixed-content blocks** — `http://` assets on an https page (protocol A1)
3. **Non-2xx same-origin XHR** — 419 = CSRF rotation broke (A2); 500 = server error the page swallowed
4. **Empty app mount** — `#app` empty means the SPA never rendered; unit tests never see this

**Contrast — what a smoke is NOT:**
- *Not* a full E2E regression suite (that's the app's own test estate)
- *Not* an uptime ping — a 200 with an empty `#app` is a FAIL
- *Not* third-party monitoring — detectors scope to app-origin

## Smoke Design Rules (codified from real failures)

- **Serial, not parallel.** Shared server + global flag state races under
  parallel runners; a flaky gate gets deleted, and then you have no gate.
- **Restore global state.** Any test that mutates a global (a feature flag, a
  setting) restores it — otherwise test order changes outcomes.
- **App-origin scoping.** A third-party CDN hiccup must not fail your deploy;
  detectors filter to same-origin resources and XHR.
- **HTTPS-conditional mixed-content check.** The mixed-content detector applies
  only when the page itself is https — locally served http pages would
  false-positive.

## Where the Gates Live

- Test job + smoke job in CI (branch-mapped: dev/stage/main)
- Platform "Wait for CI" holds the deploy until both are green
- Post-deploy live smoke runs against the environment's real URL after the
  platform reports the deploy healthy

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|--------------|-------------|
| "The unit suite is comprehensive, smoke is redundant" | Proxy/CSRF/render bugs live in layers unit tests can't reach |
| Parallel smoke for speed | Races on shared state → flaky → deleted → no gate |
| curl-based "smoke" | curl doesn't enforce mixed-content or execute the SPA (A1 trap) |
| Failing on any console noise | Third-party noise trains people to ignore the gate |
| Smoke only pre-deploy | Live-infra drift (proxy headers, env URLs) only shows post-deploy |

## Source

Gate design proven in the graph-portal pipeline (2026-07-03); detectors derived
from the two bugs its 107-test suite missed.

</testing_gates>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
