# Pre-Deploy Checklist

**Purpose:** Pass/fail gate before any promotion up the ladder — the last stop
before an environment changes. Fail-closed: an unchecked item is a failed gate.

## Gates Green

- [ ] Test job green on the source branch — evidence: CI run link
- [ ] Browser smoke green on the source branch — evidence: CI run link
- [ ] No detector was weakened, skipped, or commented out to get to green — evidence: diff of the smoke spec vs last known-good

## Migrations

- [ ] Schema changes (if any) already ran on the downstream environment(s) — evidence: migration status per env
- [ ] Migration file ordering verified (alterations sort after the tables they alter) — evidence: migration filenames
- [ ] Data-destructive migrations flagged and consciously approved — evidence: named approval in the promotion note

## Recovery Posture

- [ ] Rollback path current: prior known-good build identified — evidence: deployment ID
- [ ] Rollback has been exercised at least once for this app (N → N+1 → N, smoke green) — evidence: ops notes entry
- [ ] Hotfix path documented (branch off prod, gates apply, merge DOWN after) — evidence: ops notes

## Discipline

- [ ] The change reached this environment through the ladder, not directly — evidence: branch history
- [ ] Prod promotions: the diff was reviewed before merge to main — evidence: PR link

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
