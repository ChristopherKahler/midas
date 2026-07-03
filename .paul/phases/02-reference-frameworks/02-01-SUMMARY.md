---
phase: 02-reference-frameworks
plan: 01
subsystem: knowledge
tags: [frameworks, protocols, railway, security-controls, compliance, stack-adapters]

requires:
  - phase: 01-skeleton-entry
    provides: src tree + installed skeleton + router referencing these files
provides:
  - The six reference frameworks (installed + source)
  - protocols.md declared the LIVING canonical protocol library (12 protocols)
affects: [03-core-tasks — every task lazy-loads these, 04-checklists — gates derive from security-controls]

tech-stack:
  added: []
  patterns: [teach-by-contrast frameworks, canonicity handoff, inline self-containment, readiness-not-legal-advice scoping]

key-files:
  created: [src/frameworks/protocols.md, src/frameworks/railway.md, src/frameworks/testing-gates.md, src/frameworks/security-controls.md, src/frameworks/compliance-maps.md, src/frameworks/stack-adapters.md]
  modified: []

key-decisions:
  - "protocols.md is canonical from now on; planning Doc 2 §A is a historical snapshot"
  - "Adapter sketches (Express/Django) prove the interface; full adapters land dogfood-first"

patterns-established:
  - "Every control/protocol carries: rule + real failure prevented + control satisfied"
  - "Binary pass/fail phrasing for all controls (auditor-shaped)"

duration: 30min
started: 2026-07-03T12:15:00-05:00
completed: 2026-07-03T12:45:00-05:00
description: "Six spec-conformant reference frameworks shipped — 12-protocol gold preserved, 9-domain control catalog, 3-regime crosswalk, Laravel adapter"
type: Summary
about: "12-ops-midas"
---

# Phase 2 Plan 01: Reference Frameworks Summary

**Six spec-conformant knowledge files shipped: the 12-protocol living library, Railway opinions, the 4-layer gate taxonomy, the 9-domain control catalog, the SOC2/HIPAA/GDPR crosswalk, and the universal/stack adapter split with the proven Laravel adapter.**

## Performance

| Metric | Value |
|--------|-------|
| Duration | ~30 min |
| Tasks | 2 completed |
| Files modified | 6 created + 6 installed |

## Acceptance Criteria Results

| Criterion | Status | Notes |
|-----------|--------|-------|
| AC-1: Protocol gold preserved | Pass | grep confirms 12/12 A-numbered protocols; traps + design notes carried; growth contract present |
| AC-2: Spec conformance | Pass | 6/6: XML container, Purpose, anti-patterns, no frontmatter |
| AC-3: Installed and loadable | Pass | diff -r clean |

## Accomplishments

- The irreplaceable gold (Doc 2 §A) now lives as the living canonical library with an explicit growth contract
- Control catalog phrased binary pass/fail — directly consumable by harden/assess as gates
- Compliance crosswalk carries the BAA hard gate and the honesty scope statement

## Task Commits

| Task | Commit | Type | Description |
|------|--------|------|-------------|
| Tasks 1+2 | `a4b9e30` (see git log) | feat | Six frameworks + install |

## Files Created/Modified

| File | Change | Purpose |
|------|--------|---------|
| `src/frameworks/protocols.md` | Created | Living canonical protocol library (A1–A12 + growth contract) |
| `src/frameworks/railway.md` | Created | Railway opinions with WHY per opinion |
| `src/frameworks/testing-gates.md` | Created | 4-layer gate taxonomy + 4 smoke detectors + design rules |
| `src/frameworks/security-controls.md` | Created | 9-domain pass/fail control catalog |
| `src/frameworks/compliance-maps.md` | Created | SOC2/HIPAA/GDPR crosswalk + evidence shape + scope statement |
| `src/frameworks/stack-adapters.md` | Created | Universal/specific split + Laravel adapter + interface sketches |

## Decisions Made

| Decision | Rationale | Impact |
|----------|-----------|--------|
| Canonicity handoff to protocols.md | Two diverging copies of the gold is a drift time-bomb | Future protocols append here first |

## Deviations from Plan

None — plan executed as audited.

## Issues Encountered

None.

## Next Phase Readiness

**Ready:** All six knowledge files loadable by Phase 3 tasks; control catalog shaped for direct checklist derivation.

**Concerns:** None.

**Blockers:** None.

---
*Built with PAUL Framework v1.4 · https://chrisai.cv/skool · https://youtube.com/@chris-ai-systems*
*Phase: 02-reference-frameworks, Plan: 01*
*Completed: 2026-07-03*
