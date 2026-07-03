---
description: "MIDAS — milestone and phase structure"
type: Roadmap
about: "12-ops-midas"
---

# Roadmap: MIDAS

## Overview

Six phases turn the canonical plan (Docs 1–3) into a shipped skillsmith suite:
skeleton → knowledge → tasks → enforceable artifacts → vendored AEGIS spine →
dogfood against graph-portal and register. Built through PAUL with enterprise
audit on — the framework that preaches gates is built through gates.

## Current Milestone

**v1.0 MIDAS Framework** (v1.0.0)
Status: In progress
Phases: 4 of 6 complete

## Phases

| Phase | Name | Plans | Status | Completed |
|-------|------|-------|--------|-----------|
| 1 | Skeleton & entry point | 1 | Complete | 2026-07-03 |
| 2 | Reference frameworks | 1 | Complete | 2026-07-03 |
| 3 | Core tasks (9 playbooks) | 2 | Complete | 2026-07-03 |
| 4 | Checklists & templates | 1 | Complete | 2026-07-03 |
| 5 | Vendor AEGIS + agents | 1 | Not started | - |
| 6 | Dogfood, register, ship | 1 | Not started | - |

## Phase Details

### Phase 1: Skeleton & entry point

**Goal:** Source repo tree + the single thin router `~/.claude/commands/midas.md` per skillsmith canonical installed shape; `/midas` loads and routes cleanly with one menu entry.
**Depends on:** Nothing (first phase)
**Research:** Unlikely (skillsmith specs already read; pattern proven by /high-signal-extraction)

**Scope:**
- `12-ops-midas/src/{tasks,frameworks,agents,checklists,templates,context}` tree
- Router: frontmatter + activation/persona/commands/routing(detection-first)/greeting
- Install surfaces: `~/.claude/commands/midas.md` + `~/.base-frameworks/midas/`

**Plans:**
- [x] 01-01: Skeleton + router + install surfaces

### Phase 2: Reference frameworks

**Goal:** The six knowledge files a task can load — Doc 2 §A verbatim (protocols), §F (railway), §C (security-controls), §D (compliance-maps), §E (stack-adapters), §A3+taxonomy (testing-gates).
**Depends on:** Phase 1 (tree exists)
**Research:** Unlikely (content is Doc 2, already written)

**Plans:**
- [x] 02-01: Author all six frameworks/ files per skillsmith frameworks spec

### Phase 3: Core tasks (9 playbooks)

**Goal:** Nine executable tasks per skillsmith tasks spec, each loading its frameworks, ending in its checklist gate, teaching the why, logging to BASE + context.
**Depends on:** Phase 2 (tasks load frameworks)
**Research:** Unlikely (Doc 2 §B defines each)

**Plans:**
- [x] 03-01: Critical five — assess, pipeline, smoke, secrets, harden
- [x] 03-02: Remaining four — provision, deploy, compliance, incident + graph-portal dry-run

### Phase 4: Checklists & templates

**Goal:** Five pass/fail checklists + five drop-in templates generalized from graph-portal's proven files (ci.yml, Dockerfile, railway.json, smoke.spec.ts, trustproxy snippet).
**Depends on:** Phase 3 (tasks reference the gates)
**Research:** Unlikely (copy from working repo, generalize)

**Plans:**
- [x] 04-01: Checklists + templates from graph-portal gold

### Phase 5: Vendor AEGIS + agents

**Goal:** AEGIS copied in as maintained fork at `aegis/` with provenance + sync-path README; thin MIDAS-framing agent adapters; harden/compliance wired to the vendored audit/validate.
**Depends on:** Phase 3 (harden/compliance tasks exist)
**Research:** Likely (read aegis README + docs/ARCHITECTURE.md before vendoring)
**Research topics:** aegis command entry points, agent invocation pattern, what to include vs exclude from the fork

**Plans:**
- [ ] 05-01: Vendor fork + adapters + wiring

### Phase 6: Dogfood, register, ship

**Goal:** MIDAS assess run against graph-portal yields an accurate, actionable posture report; framework registered (BASE graph, decision log, registry); repo committed; installed surfaces verified.
**Depends on:** Phases 1–5
**Research:** Unlikely

**Plans:**
- [ ] 06-01: Dogfood + register + ship

---
*Roadmap created: 2026-07-03*
*Last updated: 2026-07-03*
