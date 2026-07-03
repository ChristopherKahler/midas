# MIDAS — Mission-critical Infrastructure, Deployment Assurance System

Opinionated DevOps + security/compliance delivery framework for Claude Code.
Takes an application from local dev to enterprise-grade, audit-defensible
production — gated CI/CD, secrets discipline, browser smoke gates, security
hardening, SOC2/HIPAA/GDPR readiness evidence. Ships with **AEGIS** (the
security/compliance audit framework) vendored inside as a maintained fork.

**This repo is the source of truth.** The installed surfaces are copies —
never edit them directly; edit here, then re-install.

## Layout

```
src/
  midas.md          ← the router (installs to ~/.claude/commands/midas.md)
  tasks/            ← the 9 executable playbooks
  frameworks/       ← reference knowledge (protocols, railway, controls, compliance, adapters, gates)
  agents/           ← MIDAS-framing adapters over the vendored aegis agents
  checklists/       ← pass/fail gates tasks block on
  templates/        ← drop-in artifacts (ci.yml, Dockerfile, railway.json, smoke.spec.ts…)
  context/          ← per-app state (app registry, posture, evidence index)
  aegis/            ← the vendored AEGIS fork (see aegis/README.md for provenance + sync)
```

## Install

```bash
cp src/midas.md ~/.claude/commands/midas.md
mkdir -p ~/.base-frameworks/midas
cp -r src/tasks src/frameworks src/agents src/checklists src/templates src/context src/aegis ~/.base-frameworks/midas/
```

Exactly ONE menu entry (`/midas`); everything else lives off-menu in
`~/.base-frameworks/midas/` (skillsmith canonical installed shape).

## Uninstall

```bash
rm ~/.claude/commands/midas.md
rm -rf ~/.base-frameworks/midas
```

Standalone `/aegis` is unaffected by install or uninstall.

## Canonical plan

`~/chris-ai-systems/planning/devops-security-framework/` — Docs 1 (architecture),
2 (playbooks & controls), 3 (build plan). Doc 2 §A is the protocol library:
session-proven rules, each recording the failure it prevents and the compliance
control it satisfies. That library grows with every build — new protocol =
framework entry + checklist line + `base learn`.

---
*Chris AI Systems · Part of the Agentic OS · https://chrisai.cv/skool*
