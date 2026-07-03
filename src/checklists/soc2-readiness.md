# SOC 2 Readiness Checklist

**Purpose:** Pass/fail gate for the compliance task's readiness report — every
item is an evidence TRIPLE (control → satisfied-by → location). This produces
readiness, not certification; a licensed auditor certifies. Fail-closed: an
unchecked item is a failed gate for "audit-ready" status.

## Security (Common Criteria)

- [ ] Access control triple recorded — evidence: control → code/config → location
- [ ] Audit logging triple recorded — evidence: control → channel → location
- [ ] Secrets management triple recorded — evidence: control → provisioning pattern → location
- [ ] Change management triple recorded — evidence: control → CI gates + branch protection → location
- [ ] Network controls triple recorded — evidence: control → headers/limits/TLS → location

## Availability

- [ ] Health/restart triple recorded — evidence: platform config location
- [ ] Backup/restore triple recorded (restore TESTED with date) — evidence: ops note
- [ ] Rollback triple recorded (exercised with date) — evidence: ops note

## Processing Integrity

- [ ] CI + smoke gate triple recorded — evidence: workflow + run history
- [ ] Migration discipline triple recorded — evidence: downstream-first history
- [ ] Defensive config triple recorded — evidence: env-fallback idiom sites

## Confidentiality

- [ ] Encryption in transit + at rest triples recorded — evidence: proxy-trust + casts locations
- [ ] Credential isolation triple recorded — evidence: spawn-env sites
- [ ] Tenant isolation triple recorded — evidence: scoped-binding code

## Privacy

- [ ] Data minimization triple recorded — evidence: classification doc
- [ ] Consented scope-change triple recorded — evidence: re-auth flow code
- [ ] Retention/deletion triples recorded (deletion is a CODE PATH) — evidence: deletion implementation

## Report Integrity

- [ ] No unmapped HIGH-RISK criterion (else route back to harden) — evidence: the readiness report's open-items table
- [ ] Honesty clause present verbatim in the readiness report — evidence: report text
- [ ] Subprocessor inventory attached — evidence: report section

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
