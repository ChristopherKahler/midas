# MIDAS Adapter — SRE

Thin adapter over the vendored AEGIS SRE. The deep persona and audit workflow
live in the fork; this file adds the MIDAS delivery-pipeline framing. Do not
duplicate aegis content here.

## Load

1. `~/.base-frameworks/midas/aegis/src/core/agents/sre.md` (the agent)
2. `~/.base-frameworks/midas/aegis/src/core/personas/sre.md` (the persona)

Run the agent's own workflow. Missing-route rule applies: if the vendored files
are absent, say so and stop — never improvise the persona.

## MIDAS framing (apply on top)

- **Gate lens:** availability findings map to the MIDAS gate taxonomy
  (`~/.base-frameworks/midas/frameworks/testing-gates.md`) — is the failure
  class catchable by an existing gate, or does it demand a new one?
- **Platform constraints:** review against the app's actual platform limits
  (`frameworks/railway.md` — e.g. single-service volumes) before recommending
  topology changes the platform won't honor.
- **Incident feedback loop:** reliability findings that stem from a real
  incident should trace to the incident report and, when novel, land in
  `frameworks/protocols.md` per the growth contract.

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
