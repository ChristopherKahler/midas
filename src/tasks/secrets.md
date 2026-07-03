<purpose>
Establish secrets discipline for the app: interactive provisioning, env-scoped
deploy tokens, rotation cadence, spawn-environment safety, and a clean
secret-in-code/log scan. After this task, no secret exists in code, logs, or
any agent session — and the pipeline's env access is separately grantable per
environment.
</purpose>

<user-story>
As a builder working with an AI agent, I want secrets provisioned and handled so
they never enter code, logs, or the session transcript, so that a leaked
credential can't originate from my own tooling.
</user-story>

<when-to-use>
- Posture report flags secrets handling (hardcoded creds, ambient env, one global token)
- Pipeline task needs env-scoped tokens that don't exist yet
- Rotation is due, or a credential may have been exposed
- Entry point routes here via `/midas secrets`
</when-to-use>

<context>
@~/.base-frameworks/midas/context/app-registry.md
@~/.base-frameworks/midas/context/{app}/posture.md (secrets findings)
</context>

<references>
@~/.base-frameworks/midas/frameworks/protocols.md (A4 spawn-env, A5 secrets, A6 connector protocol — load before provisioning)
</references>

<steps>

**THE INVARIANT (applies to EVERY step in this task):** secret values are
entered interactively by the OPERATOR — hidden prompts (`gh secret set`),
platform dashboards, one token at a time. Never echoed. Never requested in this
session. Never written to any file, log, or output by the agent. If a step
seems to need the agent to see a value, the step is wrong — redesign it.

<step name="scan" priority="first">
Scan for secrets where they must not be:

1. Code + history: grep the repo for credential patterns (keys, tokens,
   passwords, connection strings); check `.env` isn't committed
2. Logs: confirm no secret values in application/CI logs
3. Session hygiene: confirm no workflow requires pasting a secret to an agent

Each hit is a FAIL with a remediation: move to env, rotate the exposed value
(exposed = rotate, always — teach why: you can't prove a leaked value wasn't
copied, so exposure and compromise are operationally identical).
</step>

<step name="provision_env_scoped">
Provision what the pipeline and app need, per protocol A5:

1. Deploy tokens: one per environment (`RAILWAY_TOKEN_DEV/_STAGE/_PROD`),
   created in the platform dashboard by the operator, added via `gh secret set`
   hidden prompts. Why env-scoped: prod deploy capability becomes separately
   grantable and revocable (Confidentiality control).
2. Provider credentials: per protocol A6, expose `client_id`, `client_secret`,
   `redirect`, `authorize_url`, `token_url` as env vars — controllers never
   hardcode a provider URL (vendor swap = variable change, not release).
3. Optional secrets: map secret → env var and gate the consuming CI step on the
   env var so a missing optional secret SKIPS cleanly, never red-fails.

Walk the operator through each provisioning action; the agent prepares commands
and verifies EFFECTS (a masked `gh secret list` entry exists), never values.
</step>

<step name="spawn_env_safety">
Apply protocol A4 wherever the app spawns subprocesses:

1. Find spawn sites (queue jobs invoking CLIs, generators)
2. Each passes an EXPLICIT environment — never ambient inheritance (the
   interactive-shell-works-production-401s class)
3. Every outbound provider call has a timeout (an untimed call can hang a
   user-facing flow forever)
</step>

<step name="rotation_policy">
Document rotation in the app's ops notes:

- Cadence per credential class (deploy tokens, provider secrets, DB passwords)
- The rotation PROCEDURE per credential (where it lives, what consumes it,
  restart requirements) — teach: an undocumented rotation is an outage
  generator; people rotate the value and miss a consumer
- Trigger events: exposure, offboarding, provider incident
</step>

<step name="gate_and_record" priority="last">
1. Re-run the scan from step 1 — must be clean
2. Run `~/.base-frameworks/midas/checklists/security.md` items for the
   auth/secrets domain — fail-closed if the checklist file is missing
3. Registry: update the app's row (stage advances per ladder; never regress)
4. `base learn` novel findings; new failure class → protocols.md growth contract

Report: what's provisioned (names only, never values), scan result, rotation
policy location.
</step>

</steps>

<output>
## Artifact
Clean secret scan, env-scoped tokens provisioned (verified by masked listing),
spawn sites hardened, rotation policy documented in the app's ops notes.

## Location
App repo (spawn-site fixes, ops notes); CI secret store; registry + notes under
`~/.base-frameworks/midas/context/{app}/`.
</output>

<acceptance-criteria>
- [ ] Scan clean: no secrets in code, history, logs, or session workflows
- [ ] The invariant held: no secret value ever entered this session or any output
- [ ] Env-scoped deploy tokens exist (verified via masked listing, not values)
- [ ] Provider endpoints config-over-code (A6 shape)
- [ ] Optional secrets skip cleanly when absent
- [ ] Spawn sites pass explicit env; outbound calls have timeouts
- [ ] Rotation cadence + procedure documented
- [ ] Registry updated; learnings logged
</acceptance-criteria>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
