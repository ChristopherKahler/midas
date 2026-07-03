---
phase: 03-core-tasks
plan: 01
subsystem: tasks
tags: [assess, pipeline, smoke, secrets, harden]

requires:
  - phase: 02-reference-frameworks
    provides: the six frameworks these tasks lazy-load
provides:
  - The critical five tasks (assess, pipeline, smoke, secrets, harden)
  - The MIDAS task contract (fail-closed gates, registry writes, teaching, non-echo invariant)
affects: [03-02 — same contract, 04 — checklists these gate on]

tech-stack:
  added: []
  patterns: [fail-closed gates, posture rubric (% applicable controls passing), secrets non-echo invariant, idempotent re-run semantics]

key-files:
  created: [src/tasks/assess.md, src/tasks/pipeline.md, src/tasks/smoke.md, src/tasks/secrets.md, src/tasks/harden.md]
  modified: []

key-decisions:
  - "assess is the only task that may lower posture_score; stages never regress elsewhere"
  - "Missing checklist file = failed gate (fail-closed), everywhere"

patterns-established:
  - "Teach-apply-evidence-verify per control in harden"
  - "Agent verifies secret EFFECTS (masked listings), never values"

duration: 45min
started: 2026-07-03T12:55:00-05:00
completed: 2026-07-03T13:20:00-05:00
description: "Critical five tasks shipped as executable teaching workflows with fail-closed gates and the secrets non-echo invariant"
type: Summary
about: "12-ops-midas"
---

# Phase 3 Plan 01: Critical Five Summary

**assess, pipeline, smoke, secrets, harden shipped — the session's hardest-won lessons as executable teaching workflows, all fail-closed, all registry-writing.**

## Acceptance Criteria Results

| Criterion | Status | Notes |
|-----------|--------|-------|
| AC-1: Spec conformance | Pass | 5/5 all sections; snake_case steps; lazy-loaded references |
| AC-2: MIDAS task contract | Pass | Teaching + fail-closed + registry + BASE logging in all five (assess fail-closed added during verification) |
| AC-3: Installed and loadable | Pass | diff -r clean; router paths resolve for the five |

## Deviations from Plan

**1. [contract] assess.md initially lacked fail-closed language**
- **Found during:** install verification grep
- **Fix:** score step now fails closed when the control catalog is missing (an improvised rubric is unauditable)
- **Verification:** grep passes post-fix

## Next Phase Readiness

**Ready:** contract patterns established for 03-02 to inherit.
**Blockers:** None.

---
*Built with PAUL Framework v1.4 · https://chrisai.cv/skool · https://youtube.com/@chris-ai-systems*
*Phase: 03-core-tasks, Plan: 01*
*Completed: 2026-07-03*
