<purpose>
Stand up the app's environments and services: the project, Postgres, volumes,
per-environment domains, and the dev/stage/prod ladder with isolated databases
and a deny-by-default network posture. After this task, the app has somewhere
real and correctly shaped to deploy TO.
</purpose>

<user-story>
As a builder starting from "it runs locally," I want environments provisioned
as an isolated ladder from day one, so that stage rehearsal actually proves
things and a bad migration can never find prod data first.
</user-story>

<when-to-use>
- Assessed app has no (or single) environment
- New app graduating from local dev toward its first deploy
- Entry point routes here via `/midas provision`
</when-to-use>

<context>
@~/.base-frameworks/midas/context/app-registry.md
@~/.base-frameworks/midas/context/{app}/posture.md (hosting findings)
</context>

<references>
@~/.base-frameworks/midas/frameworks/railway.md (the platform opinions — load first)
@~/.base-frameworks/midas/frameworks/protocols.md (A12 single-service constraint)
</references>

<steps>

<step name="confirm_shape" priority="first">
Load @~/.base-frameworks/midas/frameworks/railway.md.

Confirm with the operator:
1. Platform (default: Railway — the proven target; other platforms via the
   same principles, adapter pending)
2. The ladder: dev / stage / prod (three isolated environments is the default;
   fewer requires a stated reason)
3. Services: does the app need a worker? A volume? — teach protocol A12 here:
   Railway volumes are single-service, so web+worker run COMBINED until
   artifacts move to object storage. Design the service shape to what the
   platform will actually honor.

**Wait for confirmation.**
</step>

<step name="provision_ladder">
For each environment (operator performs dashboard actions; agent prepares and
verifies effects):

1. Create the environment; connect the GitHub repo IN THIS ENVIRONMENT with its
   trigger branch (per-env setting — envs are siblings, not inheritors)
2. Provision an ISOLATED Postgres per environment. Why non-negotiable: shared
   data stores across tiers make the ladder theater — stage rehearsal proves
   nothing, and stage bugs mutate prod data (Confidentiality + Availability)
3. Per-env domain; set `APP_URL` and OAuth redirect URIs for THIS env's domain
   (protocol A1's cousin: wrong-env URLs break signed URLs and OAuth in
   browser-only ways)
4. Health check on the app's health endpoint (`/up` for Laravel) wired to the
   platform restart policy
</step>

<step name="deny_by_default">
Set the network posture:

1. Nothing publicly exposed except the web service's domain — DBs and workers
   have no public networking
2. Egress: where the platform supports it, restrict to the providers the app
   actually calls
3. Teach: deny-by-default is stance #2 — everything starts closed and opens
   explicitly, because you can audit an allowlist but not an "everything
   except…" list.
</step>

<step name="gate_and_record" priority="last">
1. Run `~/.base-frameworks/midas/checklists/provision.md` — fail-closed if
   missing: every env isolated, no shared stores, domains + health checks live
2. Verify by EFFECT: each env boots, health check green, DB connections point
   at that env's own database (read the config, don't assume)
3. Registry: stage → `provisioned` (never regress)
4. `base learn` novel platform findings; new failure class → protocols.md

Report: the ladder as provisioned (envs, domains, isolation), and the next
recommended task (usually `/midas pipeline`).
</step>

</steps>

<output>
## Artifact
Three isolated environments with per-env repos/branches/domains/DBs, health
checks live, deny-by-default networking; updated registry row.

## Location
Platform project; provisioning notes under `~/.base-frameworks/midas/context/{app}/`.
</output>

<acceptance-criteria>
- [ ] Ladder confirmed and provisioned; every environment's DB isolated (verified by config, not assumption)
- [ ] Repo + trigger branch connected per environment
- [ ] Per-env domains with matching APP_URL/redirect URIs
- [ ] Health checks green in every environment
- [ ] Deny-by-default: nothing public except the web domain
- [ ] Provision checklist green (fail-closed)
- [ ] Registry updated; learnings logged
</acceptance-criteria>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
