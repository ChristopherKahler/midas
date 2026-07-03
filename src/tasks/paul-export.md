<purpose>
Export a MIDAS posture report's findings into the assessed app's own PAUL
project: one MIDAS-prefixed remediation folder per gap under `.paul/phases/`
(each with a finding CONTEXT.md), plus a precedence notice block in the app's
STATE.md so every future PAUL session sees the security work BEFORE planning
feature work.
</purpose>

<user-story>
As an operator whose app is PAUL-managed, I want MIDAS findings to land inside
the app's own planning system with precedence signaling, so that remediation
happens through the same ceremony as feature work instead of rotting in a
report nobody re-opens.
</user-story>

<when-to-use>
- After `/midas assess` produced a posture report with gaps, and the app has (or should have) a `.paul/` project
- After `/midas harden` left open items that need scheduled work
- Re-export after a re-assess (the export is idempotent — it refreshes)
- Entry point routes here via `/midas export`
</when-to-use>

<context>
@~/.base-frameworks/midas/context/app-registry.md
@~/.base-frameworks/midas/context/{app}/posture.md (the findings being exported — fail-closed: no report → run assess first)
</context>

<references>
@~/.base-frameworks/midas/frameworks/protocols.md (when a finding cites a protocol)
</references>

<steps>

<step name="locate_targets" priority="first">
1. Identify the app (registry row) and load its posture report.
   **Fail-closed:** no posture report → stop; `/midas assess` runs first —
   exporting unscored findings would put unaudited claims into a planning system.
2. Check for `.paul/` in the app repo.

<if condition="no .paul directory">
Tell the operator: "This app isn't PAUL-managed. Run `/paul:init` there first,
or skip the export and work from the posture report directly." Stop.
</if>

3. Read the app's `.paul/STATE.md` and list existing `MIDAS-*` folders under
   `.paul/phases/` (a prior export may exist — this run REFRESHES it).
</step>

<step name="write_remediation_folders">
For each item in the posture report's prioritized gap list, create:

```
.paul/phases/MIDAS-{NN}-{slug}/CONTEXT.md
```

where `{NN}` is the two-digit priority rank (01 = highest risk×effort priority)
and `{slug}` is a kebab summary (e.g. `MIDAS-01-security-headers`).

Each CONTEXT.md:

```markdown
# MIDAS Finding: {title}

**Source:** MIDAS posture report {date} (score {score}) — ~/.base-frameworks/midas/context/{app}/posture.md
**Priority:** {NN} of {total} · **Effort:** {S/M/L} · **Status:** OPEN

## Finding
{what was found, with the evidence pointer from the report}

## Why it matters
{the real failure class this exposes; cite the protocol (A-number) or control
domain it violates}

## Remediation route
Run `/midas {task}` for the guided fix, or plan it directly in this phase.

## Suggested acceptance criteria
- [ ] {control satisfied, phrased pass/fail with its evidence pointer}
- [ ] Posture re-scored via /midas assess; this finding no longer FAILs
```

Rules:
- **Idempotent refresh:** an existing `MIDAS-{NN}-{slug}` folder for the same
  finding is updated in place; folders for findings that no longer exist in the
  latest report get their CONTEXT.md status flipped to `RESOLVED (re-assess {date})`
  — never silently deleted (they're audit history).
- Never renumber or touch the app's own numeric phase folders.
- UNVERIFIED report items export too, marked `Status: VERIFY` with the operator
  check named — verification is work worth scheduling.
</step>

<step name="inject_state_notice">
Inject the precedence block into the app's `.paul/STATE.md`, immediately after
the `# Project State` heading, wrapped in idempotency markers (replace the
whole block if the markers already exist — never duplicate):

```markdown
<!-- MIDAS:BEGIN — managed by /midas export; do not hand-edit between markers -->
## ⚠️ MIDAS REMEDIATION NOTICE — PRECEDENCE

**This notice takes precedence over roadmap work.** A MIDAS posture assessment
({date}, score {score}/100) filed {N} findings as `MIDAS-*` phase folders. Any
session opening this project MUST review them before planning new feature work:

| Priority | Finding | Folder | Effort | Status |
|----------|---------|--------|--------|--------|
| 01 | {title} | phases/MIDAS-01-{slug}/ | {S/M/L} | OPEN |

**Session instruction:** security-critical findings (priority 01–02) are
planned before or alongside the next feature phase — not after. Read each
folder's CONTEXT.md for evidence and acceptance criteria. This block is
removed only by `/midas export` after a re-assess shows the findings
resolved, or by the operator consciously deferring (log the deferral as a
PAUL decision with a revisit date).
<!-- MIDAS:END -->
```

Why STATE.md: it is PAUL's required reading — every plan/apply/unify workflow
loads it first, so the notice cannot be missed by any future session.
</step>

<step name="record_and_report" priority="last">
1. Note the export in `~/.base-frameworks/midas/context/{app}/` (date, findings
   exported, folders written).
2. `base learn --text "MIDAS export: {app} — {N} findings into .paul ({top finding} top)" --domain development --type insight`
3. Report to the operator: folders created/refreshed, the STATE notice, and the
   recommended first move (usually planning `MIDAS-01` as the next PAUL phase,
   or running the named `/midas {task}` directly).
</step>

</steps>

<output>
## Artifact
`MIDAS-{NN}-{slug}/CONTEXT.md` folders under the app's `.paul/phases/` + the
marker-wrapped precedence block in its STATE.md.

## Location
The assessed app's own `.paul/`; export record under
`~/.base-frameworks/midas/context/{app}/`.
</output>

<acceptance-criteria>
- [ ] Fail-closed held: export refused without a posture report
- [ ] One MIDAS-prefixed folder per gap, priority-ranked, app's own phases untouched
- [ ] Each CONTEXT.md carries finding + evidence + why + route + suggested ACs
- [ ] STATE.md block present exactly once (marker-idempotent), positioned after the heading
- [ ] Resolved findings flipped to RESOLVED, never silently deleted
- [ ] Export recorded in MIDAS context + BASE
- [ ] Operator told the recommended first move
</acceptance-criteria>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
