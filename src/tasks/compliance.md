<purpose>
Crosswalk the app's implemented controls to its target regime (SOC 2 / HIPAA /
GDPR), generate the evidence index, and produce a readiness report an exec's
security team can act on. Honest scoping throughout: this produces
audit-READINESS — a real auditor certifies.
</purpose>

<user-story>
As a builder selling into $2–20M companies, I want a control→evidence map and a
readiness report in the language a buyer's security team expects, so that their
review is a confirmation exercise instead of a discovery of gaps.
</user-story>

<when-to-use>
- App is hardened (stage: hardened) and needs its evidence assembled
- An enterprise buyer sent a security questionnaire
- Entry point routes here via `/midas compliance`
</when-to-use>

<context>
@~/.base-frameworks/midas/context/app-registry.md
@~/.base-frameworks/midas/context/{app}/posture.md (scorecard — the control ground truth)
</context>

<references>
@~/.base-frameworks/midas/frameworks/compliance-maps.md (the crosswalk — this task's spine)
@~/.base-frameworks/midas/aegis/ (the vendored AEGIS fork — deep compliance review; missing-route rule applies until vendored)
</references>

<steps>

<step name="confirm_regime" priority="first">
1. Confirm the target regime chosen at assess (default SOC 2; HIPAA when PHI
   is in the data path; GDPR obligations when EU data subjects exist)
2. Teach the stance: ONE regime designed-to up front; the others fall out of
   the overlap. Retrofitting compliance is the failure mode this framework
   exists to prevent.

<if condition="PHI is flagged in the app's data classification">
**The BAA hard gate activates:** every subprocessor touching PHI needs a
Business Associate Agreement — the host, every provider in the data path.
This is release-blocking for HIPAA posture, not a footnote: missing BAAs void
compliance regardless of technical controls.
</if>

**Wait for regime confirmation.**
</step>

<step name="build_evidence_index">
Load @~/.base-frameworks/midas/frameworks/compliance-maps.md.

For every PASSING control in the app's scorecard, record the evidence triple:

```
control → satisfied by (code path / config / log channel) → evidence location
```

Rules:
- Evidence must POINT somewhere concrete (file:line, config key, log channel) —
  "we do this" without a pointer is not evidence
- Paper-only controls (policy without a code path) are flagged, not counted —
  a deletion policy with no deletion code path fails the "show me" test
- Controls whose evidence has rotted (file moved, config changed) go back to
  the harden work list

Write the index to `~/.base-frameworks/midas/context/{app}/evidence.md`.
</step>

<step name="deep_review_via_aegis">
For regulated or high-stakes apps, invoke the vendored AEGIS fork for deep
review: `~/.base-frameworks/midas/aegis/` (its compliance-officer +
security-engineer agents audit beyond the catalog walk).

Fail-closed note: if the vendored aegis is not installed, say so and continue
WITHOUT the deep review, marking the readiness report "catalog-verified, deep
review pending" — never imply a review that didn't happen.
</step>

<step name="readiness_report" priority="last">
Produce the readiness report at
`~/.base-frameworks/midas/context/{app}/readiness.md`, written for an exec's
security team:

- Target regime; criteria groups satisfied (with evidence-index references)
- Unmapped or failing criteria — stated plainly with remediation plans
- Subprocessor inventory (+ BAA status when PHI applies)
- **The honesty clause, verbatim in the report:** "This is engineering
  readiness, not certification. Controls listed are implemented and evidenced;
  formal attestation requires an independent auditor."

Gate: no unmapped HIGH-RISK criterion — if one exists, the report routes back
to `/midas harden` instead of shipping as "ready."

Registry: stage → `compliant` only when the gate passes. `base learn` the
readiness milestone. Present the report to the operator.
</step>

</steps>

<output>
## Artifact
Evidence index (`evidence.md`) + readiness report (`readiness.md`) under
`~/.base-frameworks/midas/context/{app}/`; updated registry row.

## Format
Evidence: one triple per control. Readiness: regime → satisfied criteria (with
pointers) → open items (with plans) → subprocessors/BAAs → honesty clause.
</output>

<acceptance-criteria>
- [ ] Regime confirmed; BAA gate surfaced when PHI present
- [ ] Every counted control has a concrete evidence pointer
- [ ] Paper-only controls flagged, never counted
- [ ] Deep review run via vendored aegis, or its absence stated in the report
- [ ] Report readable by a non-engineer security reviewer; honesty clause verbatim
- [ ] No unmapped high-risk criterion (else routed back to harden)
- [ ] Registry updated only on gate pass; milestone logged
</acceptance-criteria>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
