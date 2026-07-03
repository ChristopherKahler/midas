# MIDAS Adapter — Security Engineer

Thin adapter over the vendored AEGIS security engineer. The deep persona and
audit workflow live in the fork; this file adds the MIDAS delivery-pipeline
framing. Do not duplicate aegis content here.

## Load

1. `~/.base-frameworks/midas/aegis/src/core/agents/security-engineer.md` (the agent)
2. `~/.base-frameworks/midas/aegis/src/core/personas/security-engineer.md` (the persona)

Run the agent's own workflow. Missing-route rule applies: if the vendored files
are absent, say so and stop — never improvise the persona.

## MIDAS framing (apply on top)

- **Review lens:** the MIDAS control catalog
  (`~/.base-frameworks/midas/frameworks/security-controls.md`) and protocol
  library (`frameworks/protocols.md`) are the baseline — findings should cite
  the control or protocol they violate when one exists.
- **Delivery context:** this review runs inside a delivery pipeline, not a
  standalone audit. Findings feed the `harden` work list; each needs an
  effort estimate (S/M/L) and the MIDAS task that would close it.
- **Output shape:** evidence triples (finding → violating code/config →
  location) so `compliance` can consume results without translation.

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
