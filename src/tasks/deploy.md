<purpose>
Run the promotion ladder with discipline: push to dev freely, promote to stage
deliberately, merge to main ceremonially — migrations rehearsing downstream
first, a rollback path that has actually been exercised, and a hotfix path that
can't create drift.
</purpose>

<user-story>
As a builder promoting changes toward production, I want promotion, rollback,
and hotfix procedures that are defined and rehearsed, so that prod changes are
boring and mistakes are recoverable instead of catastrophic.
</user-story>

<when-to-use>
- Promoting work up the ladder (dev → stage → prod)
- A bad deploy needs rolling back
- A prod bug needs a hotfix without waiting for the ladder
- Entry point routes here via `/midas deploy`
</when-to-use>

<context>
@~/.base-frameworks/midas/context/app-registry.md
</context>

<references>
@~/.base-frameworks/midas/frameworks/protocols.md (A10 migrations — load before any promotion involving schema changes)
@~/.base-frameworks/midas/frameworks/railway.md (platform mechanics)
</references>

<steps>

<step name="choose_mode" priority="first">
Ask which mode this is (or infer from what the operator said):

- **Promote** — move work up the ladder
- **Rollback** — a deploy went bad
- **Hotfix** — prod is broken and can't wait for the ladder

**Wait for the answer if not already clear.**
</step>

<step name="promote">
<if condition="mode is promote">
The ladder discipline, and why each rung differs:

1. **dev**: push freely — dev exists to break; its data is disposable
2. **stage**: promote deliberately — stage is the rehearsal against
   realistic data shape; a migration that hasn't run on stage does NOT go to prod
   (protocol A10: schema changes prove themselves on disposable data first)
3. **main/prod**: ceremonial — merge only what stage proved; the pipeline's
   gates (tests + smoke + Wait-for-CI) still stand; never push directly

Check migration file ordering when schema changes are in the promotion:
an add-column migration must sort AFTER the published create-table it alters,
or fresh-DB builds break (A10's second edge).
</if>
</step>

<step name="rollback">
<if condition="mode is rollback">
1. Redeploy the prior known-good build (platform redeploy of deployment N-1)
2. **Migration asymmetry caveat:** schema rollbacks are NOT symmetrical — a
   dropped column's data doesn't come back. If the bad deploy included
   migrations, prefer ROLLING FORWARD with a fix; roll schema back only when
   the migration was provably additive.
3. Verify recovery with the live smoke against the environment URL — a
   rollback isn't done when the deploy completes; it's done when the smoke is green.
</if>
</step>

<step name="hotfix">
<if condition="mode is hotfix">
The drift-proof hotfix path:

1. Branch off the PROD branch (not dev — dev may contain unshipped work)
2. Fix, test, smoke — the gates still apply; urgency doesn't waive
   machine-verified truth
3. Merge to main → deploy
4. **Merge DOWN to stage and dev immediately.** Why: a hotfix that only lives
   on main means the next promotion silently reverts it — the classic drift
   incident.
</if>
</step>

<step name="rehearse_rollback" priority="last">
If this app's rollback has never been exercised, exercise it now on DEV
("rollback tested" is defined, not asserted):

1. Deploy known-good N; deploy trivial N+1; roll back to N
2. Live smoke green on N = rollback path proven
3. Document the procedure in the app's ops notes

Then: run the relevant items of
`~/.base-frameworks/midas/checklists/pre-deploy.md` (fail-closed if missing),
update the registry row, `base learn` anything novel.
</step>

</steps>

<output>
## Artifact
The promotion/rollback/hotfix executed with its gates, plus a PROVEN rollback
procedure documented in the app's ops notes.

## Location
App repo + platform; ops notes under `~/.base-frameworks/midas/context/{app}/`.
</output>

<acceptance-criteria>
- [ ] Mode identified; the matching discipline followed (no direct-to-prod, ever)
- [ ] Schema changes rehearsed on stage before prod; migration ordering checked
- [ ] Rollback (if run) verified by green live smoke, not deploy completion
- [ ] Rollback procedure exercised at least once on dev and documented
- [ ] Hotfixes merged down to stage + dev (drift-proof)
- [ ] Checklist items run fail-closed; registry updated; learnings logged
</acceptance-criteria>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
