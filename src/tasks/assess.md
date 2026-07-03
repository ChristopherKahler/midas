<purpose>
Audit an application's ops/security/compliance posture: inventory how it's
actually run, score it against the MIDAS control catalog, and produce a posture
report with a prioritized gap list. This is where every app starts — MIDAS never
provisions, hardens, or certifies an app it hasn't scored.
</purpose>

<user-story>
As a solo builder shipping to enterprise buyers, I want an honest scored picture
of what enterprise-readiness my app is missing, so that I fix the highest-risk
gaps first instead of discovering them in a buyer's security review.
</user-story>

<when-to-use>
- Any app not yet in the MIDAS registry (detection routes here automatically)
- Re-assessing after harden/pipeline work to update the score
- An exec's security team just sent a questionnaire and you need ground truth
- Entry point routes here via `/midas assess`
</when-to-use>

<context>
@~/.base-frameworks/midas/context/app-registry.md
</context>

<references>
@~/.base-frameworks/midas/frameworks/security-controls.md (during scoring — the catalog IS the rubric)
@~/.base-frameworks/midas/frameworks/compliance-maps.md (during readiness mapping)
@~/.base-frameworks/midas/frameworks/protocols.md (when a gap matches a known protocol)
</references>

<steps>

<step name="identify_app" priority="first">
Establish the target app and its repo root.

1. Default to the current working directory's repo; confirm with the operator
   if ambiguous: "Assessing {app} at {path} — correct?"
2. Check the registry for an existing row.

<if condition="app already registered">
Re-run semantics: assess is idempotent — it re-scores and updates the existing
row. Assess is the ONLY task allowed to move `posture_score` down. Tell the
operator the previous score up front so the delta is visible.
</if>

**Wait for confirmation of the target app before proceeding.**
</step>

<step name="inventory">
Build the operational inventory by READING the app, not by asking the operator
to self-report (evidence > assumptions). Inspect in order:

1. **Hosting & environments** — deploy configs (railway.json, Dockerfile, fly.toml…),
   how many environments exist, whether data stores are isolated per env
2. **Pipeline** — CI workflows: what gates exist between push and deploy?
   Test job? Browser smoke? Wait-for-CI?
3. **Secrets handling** — grep for hardcoded credentials, .env committed, tokens
   in code/logs; how are secrets injected?
4. **Migrations** — auto-run on deploy? Rehearsed downstream first?
5. **Audit logging** — is there a dedicated audit channel? Do mutations log
   actor + action + resource + timestamp?
6. **Auth model** — RBAC? Token scoping? Session invalidation on deactivation?
7. **Data classification** — what PII/PHI does it hold? Encrypted at rest?
8. **Subprocessors** — every third party in the data path (host, providers, APIs)

Teach as you go: for each area, one line on WHY it's inventoried — e.g.
"Subprocessors matter because a missing BAA voids HIPAA regardless of your
technical controls."
</step>

<step name="score">
Load @~/.base-frameworks/midas/frameworks/security-controls.md and walk all nine
domains against the inventory.

**Fail-closed rule:** if the control catalog file is missing, STOP — never
improvise a rubric from memory. A score without the canonical catalog behind it
is unauditable, which defeats the report's purpose.

**The rubric (state it in the report):**
- Each catalog control is scored pass / fail / N/A (with reason for N/A)
- `posture_score` = passing ÷ applicable × 100, rounded
- N/A controls are listed with their reasons — an N/A without a reason is a fail

For every FAIL, record: the control, what was found instead, the real failure
class it exposes (cite the matching protocol when one exists), and the fix's
rough effort (S/M/L).
</step>

<step name="map_readiness">
Load @~/.base-frameworks/midas/frameworks/compliance-maps.md.

1. Ask which regime this app targets (default recommendation: SOC 2 for B2B SaaS;
   HIPAA only if PHI is in play).

**Wait for the regime answer.**

2. Map passing controls → the regime's criteria; list unmapped high-risk criteria.
3. State readiness honestly: "audit-ready in X of Y criteria groups" — never
   "compliant" (readiness ≠ certification; overclaiming is itself a failure).
</step>

<step name="write_report">
Write the posture report to
`~/.base-frameworks/midas/context/{app}/posture.md`:

- Header: app, date, posture_score, rubric statement, target regime
- Inventory summary (the 8 areas)
- Scorecard per domain (pass/fail/N/A per control)
- **Prioritized gap list** — ordered by (risk × effort), each gap naming the
  MIDAS task that closes it (`pipeline`, `secrets`, `harden`…)
- Readiness map for the target regime

Then update the registry row per the schema contract:
`| {app} | {path} | assessed | {today} | {score} |`
(create the row if new; update in place if re-run).
</step>

<step name="log_and_recommend" priority="last">
1. Log to BASE: `base learn --text "MIDAS assess: {app} scored {score}, top gap: {gap}" --domain development --type insight`
2. Present the operator the score, the top 3 gaps, and ONE next action — the
   MIDAS task that closes the highest-priority gap.

**Wait for the operator to choose before launching any follow-on task.**
</step>

</steps>

<output>
## Artifact
Posture report at `~/.base-frameworks/midas/context/{app}/posture.md` +
updated registry row.

## Format
Report sections: header (score + rubric + regime) · inventory · nine-domain
scorecard · prioritized gap list (each gap → closing task) · readiness map.
</output>

<acceptance-criteria>
- [ ] Inventory built from reading the app, not operator self-report
- [ ] All nine domains scored pass/fail/N/A; every N/A has a reason
- [ ] posture_score computed per the stated rubric
- [ ] Gap list prioritized and each gap names the MIDAS task that closes it
- [ ] Readiness phrased as "ready", never "compliant/certified"
- [ ] Registry row created/updated per schema contract
- [ ] BASE learn logged
- [ ] Operator confirmed the report and chose the next action
</acceptance-criteria>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
