<purpose>
Walk the MIDAS security control catalog against the app domain by domain,
applying every missing control. Each control is explained — its purpose, the
real failure it prevents, and the compliance criterion it satisfies — so the
operator learns the discipline while the app acquires it.
</purpose>

<user-story>
As a builder who is strong on features and unschooled in security controls, I
want the control catalog applied to my app with the reasoning taught alongside,
so that my next app starts hardened by habit instead of by checklist.
</user-story>

<when-to-use>
- Posture report shows failing controls (the usual route after assess + pipeline)
- Before an enterprise buyer's security review
- Entry point routes here via `/midas harden`
</when-to-use>

<context>
@~/.base-frameworks/midas/context/app-registry.md
@~/.base-frameworks/midas/context/{app}/posture.md (which controls already pass — the work list is the FAILs)
</context>

<references>
@~/.base-frameworks/midas/frameworks/security-controls.md (the catalog — this task's spine)
@~/.base-frameworks/midas/frameworks/protocols.md (the mechanism behind many controls)
@~/.base-frameworks/midas/frameworks/stack-adapters.md (the stack's API for each principle)
</references>

<steps>

<step name="build_worklist" priority="first">
1. Load the app's posture report; the work list = every FAIL, ordered by the
   report's risk × effort priority
2. Re-run semantics: for controls the report marks PASSING, re-check their
   evidence briefly (evidence may have rotted); skip only after the evidence
   re-check confirms. Stage never regresses from this task.

Present the work list. **Wait for operator confirmation** — they may re-order
for business reasons; the catalog's requirements themselves are not negotiable.
</step>

<step name="apply_domain_by_domain">
Load @~/.base-frameworks/midas/frameworks/security-controls.md and
@~/.base-frameworks/midas/frameworks/stack-adapters.md.

For each failing control, in work-list order:
1. **Teach first** (two sentences): what this control is, the real failure it
   prevents, the compliance criterion it satisfies
2. **Apply via the stack adapter** — the principle is universal; the mechanism
   comes from the adapter row (e.g., tenant isolation = scoped route-model
   binding in Laravel, not an `if` check after fetch)
3. **Produce evidence** — the code path/config/log line that will satisfy the
   control→evidence map (compliance task consumes this)
4. **Verify** — exercise the control: hit the foreign-tenant route and see 404;
   deactivate a test user and confirm session + tokens die together

Ordering rule within the walk: audit-channel controls come EARLY — every later
control's mutations should land in the audit log as a byproduct (evidence
exists before an auditor asks).

<if condition="a control requires operator-side action (MFA enrollment, dashboard settings)">
Describe the exact action, wait for the operator to complete it, then verify
the EFFECT (never credentials).
</if>
</step>

<step name="gate" priority="last">
1. Run `~/.base-frameworks/midas/checklists/security.md` end to end — every
   item pass/fail with its evidence pointer. **Fail-closed: a missing checklist
   file is a failed gate.**
2. Anything still failing goes back on the work list with a reason — the gate
   is honest, not aspirational.
3. Registry: stage → `hardened` when the checklist is green.
4. `base learn` per novel finding; new failure class → protocols.md growth
   contract + a checklist line.

Report: controls applied (with evidence pointers), controls still open (with
reasons), the delta from the posture report's original score. Recommend
re-running `/midas assess` to re-score, then `/midas compliance` to map evidence.
</step>

</steps>

<output>
## Artifact
Applied controls with per-control evidence pointers; green (or honestly red)
security checklist; updated registry row (stage: hardened when green).

## Location
App repo (the control implementations); evidence notes under
`~/.base-frameworks/midas/context/{app}/`; registry row.
</output>

<acceptance-criteria>
- [ ] Work list built from the posture report's FAILs; passing controls evidence-rechecked
- [ ] Every applied control: taught (why + criterion) + applied via the stack adapter + evidenced + verified by exercising it
- [ ] Audit-channel controls applied early so later work self-evidences
- [ ] Security checklist run fail-closed; open items honest with reasons
- [ ] Registry stage advanced only on green
- [ ] Learnings logged; novel classes appended to protocols.md
- [ ] Operator saw the applied/open split and the evidence pointers
</acceptance-criteria>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
