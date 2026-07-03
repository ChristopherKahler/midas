# Pipeline Checklist

**Purpose:** Pass/fail gate for the pipeline task — no deploy path exists that
bypasses machine-verified truth. Fail-closed: an unchecked item is a failed gate.

## Test Gate

- [ ] Test job runs on every push/PR to all mapped branches — evidence: CI workflow triggers
- [ ] Tests run against a PROD-PARITY database (same engine + major version) — evidence: CI service container image vs prod DB version
- [ ] Test job failure blocks everything downstream — evidence: `needs:` chain in the workflow

## Browser Smoke Gate

- [ ] Smoke job needs the test job and runs against a served production build — evidence: CI job definition
- [ ] Smoke implements all four detectors (console errors, mixed content, non-2xx same-origin XHR, empty app mount) — evidence: the spec's failure harness
- [ ] Smoke runs serial (workers: 1) — evidence: playwright config
- [ ] Failure artifacts uploaded (trace) for diagnosis — evidence: CI upload step

## Deploy Gating

- [ ] Wait-for-CI enabled in EVERY environment — evidence: per-env platform settings
- [ ] Deploys traceable to commits (native GitHub integration; org app installed) — evidence: dashboard deploy view shows repo source
- [ ] CLI fallback uses env-scoped tokens only — evidence: masked secret listing shows `RAILWAY_TOKEN_{ENV}` names
- [ ] Post-deploy live smoke runs against the real env URL — evidence: CI job + last run log
- [ ] Missing OPTIONAL secrets skip cleanly, never red-fail — evidence: the secret→env-var step-gating pattern in the workflow

## Proof the Gate Bites

- [ ] A deliberately failing commit was shown to HOLD the deploy (then reverted) — evidence: the held deployment in the dashboard + revert commit

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
