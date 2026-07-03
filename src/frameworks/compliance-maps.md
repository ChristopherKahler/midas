<compliance_maps>

## Purpose

The MIDAS compliance crosswalk — how implemented security controls map to
SOC 2, HIPAA, and GDPR, and how to generate the evidence an exec's security
team asks for. Loaded by the compliance and assess tasks.

**Scope statement (read first):** This is engineering-readiness guidance, not
legal advice. MIDAS makes you **audit-ready** — controls in place, evidence
indexed — and tells the truth about the difference: a real auditor certifies,
real counsel advises on obligations. Overclaiming compliance is itself a
compliance failure.

## The Opinionated Stance

**Pick ONE target regime per app, up front — usually SOC 2 — design to it from
day one, and let the others fall out of the overlap.** Chasing compliance
retroactively is the failure mode: controls bolted on after the fact cost more,
prove less, and produce no historical evidence. Front-loaded control design
means the eventual audit *confirms* rather than *discovers*.

## SOC 2 (Trust Service Criteria) — the default target for B2B SaaS

| TSC | What Satisfies It |
|-----|-------------------|
| **Security (Common Criteria)** | The bulk of the control catalog: access control, audit logging, change management, secrets discipline, network controls |
| **Availability** | Health checks, restart policy, DR/backup, monitoring |
| **Processing Integrity** | CI + browser smoke gates, migration rehearsal discipline, defensive config fallbacks |
| **Confidentiality** | Encryption in transit/at rest, credential isolation, tenant isolation in code |
| **Privacy** | Data minimization, user-consented scope changes, retention/deletion paths |

**The deliverable:** a control→evidence map — for each control: what satisfies
it (code/config/log), and where the evidence lives. This is literally the
artifact a SOC 2 auditor requests on day one.

## HIPAA — when PHI is present

| Safeguard Class | What Satisfies It |
|-----------------|-------------------|
| **Administrative** | Access management, workforce roles, audit controls |
| **Physical/Technical** | Encryption in transit + at rest, access controls, audit logging, transmission security, automatic logoff |
| **Minimum necessary** | The consented-scope connection model — PHI never enters the system unless explicitly granted, and scope widens only by user re-authorization |

### The BAA hard gate

**Every subprocessor touching PHI needs a Business Associate Agreement** — the
host (Railway), every integrated provider (Notion, etc.), every vendor in the
data path. This is a HARD GATE, not a footnote: it's the thing solo builders
miss that **voids HIPAA compliance entirely** regardless of how good the
technical controls are.

**Contrast:**
- *Voided:* encrypted database, immutable audit log, MFA everywhere — and PHI
  flowing through a vendor with no BAA. Non-compliant, full stop.
- *Compliant posture:* the same controls + a subprocessor inventory where every
  PHI-touching vendor has a signed BAA (or PHI is architecturally excluded from
  their path).

## GDPR / Privacy

| Obligation | What Satisfies It |
|------------|-------------------|
| Data subject rights (access, deletion) | Implemented export + deletion paths — a policy without a code path is not a control |
| Lawful basis + minimization | Data classification + minimum-necessary collection |
| Breach notification (72h) | The immutable audit trail — reconstruction is what makes the 72-hour window survivable |
| Processor agreements | The subprocessor inventory, again — same list as BAAs, different paperwork |

## Evidence Generation

For every satisfied control, the evidence index records:

```
control → satisfied by (code path / config / log channel) → evidence location
```

**Why this shape:** auditors don't ask "are you secure"; they ask "show me."
An answer that points at a file, a config, and a log line closes the question
in minutes. An answer that starts with "well, generally..." opens a finding.

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|--------------|-------------|
| "SOC 2 compliant" on the website after self-assessment | Overclaiming — you're audit-READY until an auditor certifies |
| Chasing all three regimes at once from day one | Diluted effort; pick one, let overlap carry the rest |
| BAA treated as legal detail for later | Missing BAAs void HIPAA regardless of technical posture |
| Deletion policy in a doc, no deletion code path | Paper controls fail the "show me" test |
| Evidence assembled the week before the audit | Historical evidence can't be retrofitted; emit it as a byproduct from day one |

## Source

Crosswalk grounded in the AEGIS compliance framework (vendored in `aegis/`) and
the graph-portal control implementation.

</compliance_maps>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
