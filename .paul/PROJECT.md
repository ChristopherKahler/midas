---
description: "A solo operator ships enterprise-grade, audit-defensible software through one command — taught while enforced"
type: Project
about: "12-ops-midas"
---

# MIDAS — Mission-critical Infrastructure, Deployment Assurance System

## What This Is

A skillsmith-authored, opinionated DevOps + Security/Compliance framework invoked
through a single slash command (`/midas`) that takes an application from local dev
to enterprise-grade, audit-defensible production on Railway (and beyond). Ships
with AEGIS vendored inside as a maintained fork — the security/compliance review
spine. Canonical plan: `~/chris-ai-systems/planning/devops-security-framework/` Docs 1–3.

## Core Value

A solo operator ships like a mature engineering org — gated CI/CD, secrets
discipline, audit evidence, compliance readiness — through one command that
teaches the *why* while enforcing the *what*.

## Current State

| Attribute | Value |
|-----------|-------|
| Type | Other — Claude Code framework (instructional/orchestration content) |
| Version | 0.0.0 |
| Status | Initializing |
| Last Updated | 2026-07-03 |

## Requirements

### Core Deliverables

- One thin router command `~/.claude/commands/midas.md` (skillsmith canonical installed shape)
- 9 executable tasks: assess, provision, pipeline, secrets, deploy, smoke, harden, compliance, incident
- 6 reference frameworks: protocols (the §A gold), railway, security-controls, compliance-maps, stack-adapters, testing-gates
- 5 checklists + 5 drop-in templates generalized from graph-portal's proven files
- AEGIS vendored as a maintained fork at `aegis/` with documented upstream-sync path

### Validated (Shipped)
None yet.

### Active (In Progress)
- [ ] Phase 1 — Skeleton & entry point

### Planned (Next)
- [ ] Phases 2–6 per ROADMAP.md

### Out of Scope
- Feature building (PAUL's job), code-quality linting (app CI's job)
- Formal certification — MIDAS produces audit-*readiness*, never claims certified
- Non-Laravel stack adapters beyond the adapter interface (slot in later)

## Target Users

**Primary:** Solo indie builders / small-team founders shipping real software to
executives at $2–20M companies — strong on features, unschooled in operational
discipline and compliance controls.

## Constraints

### Technical Constraints
- Instructional/orchestration content — validation is spec conformance + dogfood accuracy, not compilation
- Every file must validate against its skillsmith spec (entry-point/tasks/frameworks/checklists/templates)
- Installed shape: ONE flat command file + `~/.base-frameworks/midas/`; never a commands subdirectory
- Railway single-service volume constraint shapes deploy architecture guidance

### Business Constraints
- Doc 2 §A protocol library is irreplaceable gold — capture verbatim, do not water down
- Standalone AEGIS must remain untouched and fully functional
- Honest compliance scoping — overclaiming is itself a compliance failure

### Compliance Constraints
- Framework content maps controls to SOC 2 TSC, HIPAA safeguards, GDPR articles

## Key Decisions

| Decision | Rationale | Date | Status |
|----------|-----------|------|--------|
| Name: MIDAS (Mission-critical Infrastructure, Deployment Assurance System) | Mythological pairing with AEGIS; DAS anchors the function; golden touch = enterprise-grade | 2026-07-03 | Active |
| AEGIS vendored as maintained fork inside MIDAS | Zero-extra-install security spine for MIDAS users; standalone aegis untouched | 2026-07-03 | Active |
| Skillsmith canonical installed shape (thin router + ~/.base-frameworks/) | Menu hygiene; codified into skillsmith specs 2026-07-03 | 2026-07-03 | Active |
| Git home: toolbox convention `frameworks/12-ops-midas` (own repo) | Matches every sibling framework | 2026-07-03 | Active |
| Default stack adapter: Laravel + Inertia + Vue on Railway | Proven end-to-end in graph-portal build | 2026-07-03 | Active |

## Success Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Skillsmith spec conformance | 100% of files pass | - | Not started |
| Menu hygiene | Exactly 1 new command entry | - | Not started |
| Dogfood accuracy | graph-portal posture report matches lived reality | - | Not started |
| Critical-five tasks proven | assess, pipeline, smoke, secrets, harden validated vs graph-portal | - | Not started |

## Tech Stack / Tools

| Layer | Technology | Notes |
|-------|------------|-------|
| Authoring | skillsmith specs (toolbox/frameworks/02-kit-skillsmith/specs) | The contract; validated per file type |
| Security spine | AEGIS fork (from toolbox/frameworks/04-cai-aegis) | Vendored at aegis/ |
| Build ceremony | PAUL v1.4, enterprise audit ON | plan → audit → apply → unify per phase |
| Ecosystem | BASE v2 graph | decisions, learnings, per-app posture |
| Reference app | graph-portal (~/chris-ai-systems/apps/graph-portal) | Golden test fixture + template source |

## Links

| Resource | URL |
|----------|-----|
| Repository | ~/ops-sys/toolbox/frameworks/12-ops-midas (local git) |
| Canonical plan | ~/chris-ai-systems/planning/devops-security-framework/ |

---
*PROJECT.md — Updated when requirements or context change*
*Last updated: 2026-07-03*
