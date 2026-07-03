<purpose>
Run an incident end to end: classify severity FIRST, contain, communicate,
recover, then reconstruct what happened from the immutable audit trail and
capture the lesson as a new protocol. The audit log's whole purpose is proven
(or disproven) here.
</purpose>

<user-story>
As an operator whose app just broke in the real world, I want a runbook that
tells me what to do in what order — including my legal communication
obligations — so that a bad hour doesn't become a bad month.
</user-story>

<when-to-use>
- Smoke/health/monitoring detected a failure, or a user reported one
- Suspected data exposure (even unconfirmed — the clock may already be running)
- Post-incident: reconstructing and writing up an event already contained
- Entry point routes here via `/midas incident`
</when-to-use>

<context>
@~/.base-frameworks/midas/context/app-registry.md
</context>

<references>
@~/.base-frameworks/midas/frameworks/compliance-maps.md (breach-notification obligations, during severity classification)
@~/.base-frameworks/midas/frameworks/protocols.md (during protocol capture)
</references>

<steps>

<step name="classify_severity" priority="first">
**Severity BEFORE containment** — the classification changes the obligations:

| Tier | Definition | Comms |
|------|-----------|-------|
| **SEV-DATA** | Personal/customer data exposed or plausibly exposed | User communication MANDATORY; notification clock may be running (GDPR: 72h to authority). Assume exposure until reconstruction proves otherwise. |
| **SEV-AVAIL** | Service degraded/down, no data exposure | Comms to affected users at operator's judgment; status transparency recommended |
| **SEV-MINOR** | Degradation invisible to users | Internal record only |

Teach: under-classifying a data incident to avoid the comms burden is the
single most expensive incident-handling mistake — the exposure compounds with
concealment.

**Record classification + timestamp NOW** (it anchors the notification clock).
</step>

<step name="contain">
Stop the bleeding in this order:

1. **Cut the exposure path** — disable the affected feature via its release
   flag (deny-by-default pays off here: dark = 404), revoke exposed
   credentials (exposed = rotate, always), or take the service down if the
   exposure outweighs the downtime
2. Preserve evidence — do NOT clean up logs or state; reconstruction needs them
3. Note every containment action with timestamps (actor + action + resource —
   the incident itself must be reconstructable)
</step>

<step name="communicate">
<if condition="SEV-DATA">
1. Draft user communication now: what happened, what data, what you've done,
   what they should do. Honest and specific beats lawyerly and vague.
2. Check @~/.base-frameworks/midas/frameworks/compliance-maps.md notification
   obligations for the app's regime (GDPR 72h authority notification; BAA
   notification duties when PHI flows through partners).
3. **All external communications are drafts for the OPERATOR to approve and
   send** — the agent never sends on its own.
</if>

<if condition="SEV-AVAIL">
Recommend a status note if user-visible; draft it for operator approval.
</if>
</step>

<step name="recover">
1. Restore service via the deploy task's rollback/hotfix mode
   (`~/.base-frameworks/midas/tasks/deploy.md`) — its gates still apply
2. Recovery is verified by green live smoke, not by "it looks fine"
</step>

<step name="reconstruct" priority="last">
Post-incident, from the immutable audit trail:

1. Build the timeline: who did what, when, to which resource — from first
   anomalous entry to full recovery
2. **This step is also the audit-trail test:** if reconstruction can't answer
   who-did-what-when, that gap is itself a release-blocking finding → route to
   `/midas harden` (audit & logging domain)
3. Root cause + contributing factors — blameless, mechanism-focused
4. **Protocol capture:** if the incident revealed a novel failure class, append
   it to `~/.base-frameworks/midas/frameworks/protocols.md` per the growth
   contract (rule / failure / control) + a checklist line + `base learn`
5. Write the incident report to
   `~/.base-frameworks/midas/context/{app}/incidents/{date}-{slug}.md`

Gate: the report proves the trail was sufficient to reconstruct — or files the
finding that it wasn't.
</step>

</steps>

<output>
## Artifact
Incident report (classification + timeline + root cause + actions + protocol
capture) at `~/.base-frameworks/midas/context/{app}/incidents/{date}-{slug}.md`.

## Format
Header (severity, clocks, status) · containment log · comms record ·
reconstruction timeline · root cause · protocol/lesson capture.
</output>

<acceptance-criteria>
- [ ] Severity classified FIRST, with timestamp anchoring any notification clock
- [ ] SEV-DATA: user comms drafted and obligations checked; nothing sent without operator approval
- [ ] Containment actions logged with timestamps; evidence preserved
- [ ] Recovery verified by green live smoke
- [ ] Reconstruction answered who-did-what-when — or the trail gap filed as a blocking finding
- [ ] Novel failure class captured to protocols.md + checklist + base learn
- [ ] Incident report written
</acceptance-criteria>

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
