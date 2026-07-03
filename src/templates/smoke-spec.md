# Browser Smoke Spec Template

Generalized from the proven detector harness (graph-portal, 2026-07-03).
Output file: per the app's Playwright `testDir` convention (e.g.
`tests/smoke/portal.smoke.ts`); pair with `playwright.config.ts` set to
`fullyParallel: false, workers: 1` (serial — shared server + global state).

**The detector harness (`watchForFailures`) is NON-NEGOTIABLE.** Adapt the
route list, credentials plumbing, and selectors to the app — never weaken or
remove a detector. Each one exists because its bug class reached production
past a green unit suite.

```typescript
import { expect, Page, test } from '@playwright/test';

// Every route an authenticated {primary-role} should reach. Flag-gated routes
// are included when the CI seed releases flags; on live targets a dark route
// may 404 — skip cleanly rather than red-failing a healthy dark deploy.
const AUTHED_ROUTES = [
    {authed-routes-list}
];

const EMAIL = process.env.SMOKE_EMAIL;
const PASSWORD = process.env.SMOKE_PASSWORD;

/**
 * DETECTOR HARNESS — do not weaken.
 * Fails the test on the four classes unit suites structurally cannot see:
 * console errors, mixed-content blocks, failed/erroring same-origin requests,
 * and (asserted per-test) an empty app mount.
 */
function watchForFailures(page: Page) {
    const problems: string[] = [];
    const appOrigin = new URL(process.env.SMOKE_BASE_URL || 'http://127.0.0.1:{ci-app-port}').origin;
    const pageIsHttps = appOrigin.startsWith('https://');
    const isApp = (url: string) => {
        try {
            return new URL(url).origin === appOrigin;
        } catch {
            return false;
        }
    };

    page.on('console', (msg) => {
        if (msg.type() === 'error') {
            const text = msg.text();
            if (/favicon/i.test(text)) return;
            problems.push(`console.error: ${text}`);
        }
    });

    // Only OUR requests failing is a bug; third-party CDN hiccups are not.
    page.on('requestfailed', (req) => {
        if (isApp(req.url())) {
            problems.push(`requestfailed: ${req.url()} — ${req.failure()?.errorText}`);
        }
    });

    page.on('response', (res) => {
        const url = res.url();
        if (!isApp(url)) return;
        // Mixed content: only meaningful when the page itself is https.
        if (pageIsHttps && /\.(js|css)(\?|$)/.test(url) && url.startsWith('http://')) {
            problems.push(`mixed content — asset over http on https page: ${url}`);
        }
        if (res.status() >= 400) {
            if (res.status() === 401 || res.status() === 404) return; // expected on some probes
            problems.push(`${res.status()} on ${url}`);
        }
    });

    return () => problems;
}

async function login(page: Page) {
    await page.goto('/login');
    await page.getByLabel(/email/i).fill(EMAIL!);
    await page.getByLabel(/password/i).fill(PASSWORD!);
    await page.getByRole('button', { name: /log in/i }).click();
    await page.waitForURL('**{post-login-path}', { timeout: 15_000 });
}

test('entry page renders (no mixed content, no blank shell)', async ({ page }) => {
    const drain = watchForFailures(page);
    await page.goto('/');
    // The SPA must actually mount — a mixed-content block leaves the mount empty.
    await expect(page.locator('{app-mount-selector}')).not.toBeEmpty();
    expect(drain()).toEqual([]);
});

test('authenticated walk: every route renders clean', async ({ page }) => {
    const drain = watchForFailures(page);
    await login(page);
    for (const route of AUTHED_ROUTES) {
        const res = await page.goto(route);
        // Dark/flag-gated routes may 404 on live targets — skip, don't fail.
        if (res && res.status() === 404) continue;
        await expect(page.locator('{app-mount-selector}')).not.toBeEmpty();
    }
    expect(drain()).toEqual([]);
});

// Add app-specific flows below (auth-mutating actions, toggles). RULES:
// - any test that mutates global state MUST restore it before finishing
// - keep everything serial (config: workers 1) — no parallel races on shared state
```

## Field Documentation

| Field | Description | Example |
|-------|-------------|---------|
| `{authed-routes-list}` | Every load-bearing route, quoted + comma-separated | `'/dashboard', '/settings/profile'` |
| `{primary-role}` | The role whose view the walk covers | `owner` |
| `{ci-app-port}` | Must match the CI workflow's served port | `8010` |
| `{post-login-path}` | Where a successful login lands | `/dashboard` |
| `{app-mount-selector}` | The SPA mount element | `#app` |

## Section Specifications

- **Credentials** come from env (`SMOKE_EMAIL`/`SMOKE_PASSWORD`) — set by CI env
  for local runs and by GitHub secrets for live runs. Avoid in-repo fallback
  defaults; even dev-seed values in code invite copy-paste into real config.
- **The 401/404 allowances** exist for probe routes and dark features — do not
  widen them to 4xx generally; a 419 IS the CSRF bug this gate exists to catch.

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
