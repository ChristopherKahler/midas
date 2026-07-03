---
phase: 05-vendor-aegis
plan: 01
subsystem: security-spine
tags: [aegis, fork, vendoring, agents, adapters]

requires:
  - phase: 03-core-tasks
    provides: harden/compliance tasks referencing the vendored path
provides:
  - AEGIS fork at aegis/ pinned to upstream 68b41b6 with FORK-README (provenance + sync + do-not-install)
  - Three MIDAS-framing adapters (security-engineer, compliance-officer, sre)
affects: [06 — compliance dogfood invokes the vendored agents]

tech-stack:
  added: [vendored aegis (1.8M, 12 agents/personas, 9 workflows, 14 domains)]
  patterns: [fork purity (adaptations in agents/, never inside aegis/), provenance pinning, effect-verified isolation]

key-files:
  created: [src/aegis/ (full fork), src/aegis/FORK-README.md, src/agents/security-engineer.md, src/agents/compliance-officer.md, src/agents/sre.md]
  modified: []

key-decisions:
  - "Fork stays a faithful mirror; MIDAS adaptations confined to the adapter layer"
  - "Vendored install.sh must never run (would collide with standalone aegis surfaces)"

patterns-established:
  - "Adapter = load vendored agent+persona, apply MIDAS framing (catalog lens, evidence triples, delivery context)"

duration: 20min
started: 2026-07-03T15:00:00-05:00
completed: 2026-07-03T15:20:00-05:00
description: "AEGIS vendored as provenance-pinned fork with MIDAS adapters; standalone aegis proven untouched"
type: Summary
about: "12-ops-midas"
---

# Phase 5 Plan 01: Vendor AEGIS Summary

**AEGIS ships inside MIDAS: faithful fork pinned to 68b41b6 with a documented deliberate-sync procedure, three MIDAS-framing adapters routing exclusively into the vendored copy — and standalone AEGIS byte-for-byte untouched.**

## Acceptance Criteria Results

| Criterion | Status | Notes |
|-----------|--------|-------|
| AC-1: Provenance-pinned fork | Pass | diff-clean vs upstream (minus FORK-README); pin + sync + do-not-install recorded |
| AC-2: Standalone untouched | Pass | upstream git status: 0 changes; ~/.claude/commands/aegis/ intact (10 files) |
| AC-3: Adapters vendored-path-only | Pass | grep: zero refs to toolbox or standalone paths |

## Deviations from Plan

None — plan executed as audited.

## Next Phase Readiness

**Ready:** compliance.md's deep-review step now resolves; full dogfood can run.
**Blockers:** None.

---
*Built with PAUL Framework v1.4 · https://chrisai.cv/skool · https://youtube.com/@chris-ai-systems*
*Phase: 05-vendor-aegis, Plan: 01*
*Completed: 2026-07-03*
