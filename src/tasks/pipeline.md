<purpose>
Stand up the gated CI/CD pipeline: branch↔environment mapping, a test job on a
prod-parity database, the browser smoke gate, Wait-for-CI deploy holds, and a
post-deploy live smoke. After this task, a deploy that would ship a blank shell
or a CSRF-broken build is structurally impossible.
</purpose>

<user-story>
As a solo builder, I want deploys gated by machine-verified truth instead of
hope, so that the bug classes my unit suite structurally can't see (mixed
content, CSRF rotation, render failures) never reach an environment.
</user-story>

<when-to-use>
- App is assessed and its gap list names the pipeline (the most common top gap)
- CI exists but deploys aren't gated on it
- Entry point routes here via `/midas pipeline`
</when-to-use>

<context>
@~/.base-frameworks/midas/context/app-registry.md
@~/.base-frameworks/midas/context/{app}/posture.md (the assess findings for this app)
</context>

<references>
@~/.base-frameworks/midas/frameworks/testing-gates.md (the gate taxonomy — load before designing jobs)
@~/.base-frameworks/midas/frameworks/railway.md (during platform wiring)
@~/.base-frameworks/midas/templates/ci.yml (the proven starting point)
</references>

<steps>

<step name="confirm_ladder" priority="first">
Confirm the environment ladder and branch mapping with the operator:

- Default: `dev`/`stage`/`main` branches ↔ dev/stage/prod environments
- Each environment must have an ISOLATED database — a shared DB makes stage
  rehearsal theater (teach: migrations rehearsed downstream only prove anything
  against isolated data)

**Wait for confirmation of branches and environments.**
</step>

<step name="author_test_job">
Load @~/.base-frameworks/midas/frameworks/testing-gates.md.

Create the CI test job from @~/.base-frameworks/midas/templates/ci.yml:
1. Unit/feature tests against a PROD-PARITY database service (same engine +
   major version as production — teach: SQLite-in-CI vs Postgres-in-prod lets
   dialect bugs through the gate)
2. Runs on every push to the three mapped branches

Why this gate: logic errors and contract breaks die here — cheapest place to
catch them. Control satisfied: Change Management, Processing Integrity.
</step>

<step name="wire_smoke_gate">
The browser smoke job runs AFTER the test job, against a served production
build.

<if condition="the app has no smoke spec yet">
Route to `/midas smoke` first (`~/.base-frameworks/midas/tasks/smoke.md`) — the
smoke spec is its own task; this step only WIRES it into CI. Return here after.
</if>

Wire: build → serve → wait-on the local URL → run the Playwright smoke serial.
Why this gate: the four detectors catch the "passes 107 tests, blank in every
browser" class. Control satisfied: Processing Integrity.
</step>

<step name="gate_platform_deploys">
Load @~/.base-frameworks/midas/frameworks/railway.md.

1. Connect the GitHub repo in EACH environment with its trigger branch
   (per-environment setting — teach why: envs are siblings, not inheritors)
2. Enable **Wait for CI** in each environment so the platform's deploy holds
   until GitHub checks are green
3. Native GitHub integration (org must have the Railway GitHub app) so every
   deploy is traceable to a commit in the dashboard — change-management evidence
4. CLI fallback only via env-scoped tokens (`RAILWAY_TOKEN_{ENV}`) — if these
   don't exist, route to `/midas secrets` to provision them interactively

Secret invariant: token values are entered by the OPERATOR interactively —
never echoed, never pasted into this session, never written to a file.
</step>

<step name="post_deploy_live_smoke">
Add the post-deploy smoke against the environment's REAL URL after the platform
reports the deploy healthy.

Why a second smoke: pre-deploy smoke can't see live-infra drift — proxy headers,
env-specific URLs, TLS termination (protocol A1's whole failure class lives
here). A missing optional secret must SKIP this job cleanly, never red-fail:
map secret → env var, gate the step on the env var (job-level `if:` can't read
`secrets` context).
</step>

<step name="gate_and_record" priority="last">
1. Run the pipeline checklist at
   `~/.base-frameworks/midas/checklists/pipeline.md` — every item pass/fail.
   **Fail-closed rule: if the checklist file is missing, the gate FAILS** — a
   gate you can't run is a gate that didn't pass. Fix the install, then gate.
2. Prove the gate bites: push a deliberately failing commit to dev (or use a
   draft PR) and confirm the platform HOLDS the deploy; revert.
3. Update the registry row: stage → `piped` (never regress the stage).
4. PAUL sync: if the app has `.paul/phases/MIDAS-*` folders, flip any finding
   this run closed to `RESOLVED ({date} — {evidence})` in its CONTEXT.md and
   update its STATE.md notice row (per tasks/paul-export.md).
5. `base learn` anything novel discovered; if a new failure class was found and
   fixed, append it to protocols.md per the growth contract.

Report to the operator: gates now standing between code and each environment,
with evidence (the held deploy).
</step>

</steps>

<output>
## Artifact
CI workflow (test + smoke + live-smoke jobs), platform environments gated with
Wait-for-CI, updated registry row (stage: piped), evidence of a held deploy.

## Location
CI workflow in the app repo (`.github/workflows/ci.yml`); registry + notes under
`~/.base-frameworks/midas/context/{app}/`.
</output>

<acceptance-criteria>
- [ ] Test job runs on prod-parity DB for all three mapped branches
- [ ] Browser smoke job wired after tests, serial, against a served prod build
- [ ] Wait-for-CI enabled in every environment; repo connected per env
- [ ] Post-deploy live smoke wired; optional-secret jobs skip cleanly
- [ ] Gate proven to bite (held deploy demonstrated, then reverted)
- [ ] Pipeline checklist green — or the run stopped fail-closed
- [ ] Registry row updated to piped; learnings logged
- [ ] Operator saw the evidence and confirmed
</acceptance-criteria>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
