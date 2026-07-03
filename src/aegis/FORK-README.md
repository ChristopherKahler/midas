# AEGIS — Vendored Fork (inside MIDAS)

This is a **maintained fork of AEGIS** shipping inside MIDAS as its
security/compliance review spine. MIDAS tasks (`harden`, `compliance`) invoke
the agents, personas, and workflows here directly.

## Provenance

| | |
|---|---|
| **Upstream** | `~/ops-sys/toolbox/frameworks/04-cai-aegis` (github.com/ChristopherKahler/aegis) |
| **Pinned commit** | `68b41b6` — "chore: stage doc assets before toolbox migration" |
| **Vendored** | 2026-07-03 |
| **Included** | README.md, install.sh, commands/, src/ (core agents · personas · workflows, domains, rules, schemas, tools, transform), docs/ |
| **Excluded** | `.git/` |

## Fork rules

1. **This copy stays a faithful mirror.** MIDAS-specific adaptations live in
   `../agents/` (the adapter layer) — NEVER edit files inside this folder.
   A modified vendored copy becomes unsyncable within two upstream releases.
2. **DO NOT run `install.sh` from here.** It would install/overwrite the
   STANDALONE aegis surfaces (`~/.claude/commands/aegis/`). Standalone AEGIS is
   a separate product for audit-only users; MIDAS invokes this copy in place.
3. **`/aegis:*` commands referenced in the vendored docs belong to the
   standalone install.** Inside MIDAS, tasks Read and run the workflow/agent
   files directly (e.g. `src/core/agents/security-engineer.md`).

## Sync procedure (deliberate, never blind)

```bash
# 1. See what upstream changed since the pin
cd ~/ops-sys/toolbox/frameworks/04-cai-aegis && git log --oneline 68b41b6..HEAD

# 2. Review the delta file-by-file
diff -r --exclude='.git' --exclude='FORK-README.md' \
  ~/ops-sys/toolbox/frameworks/04-cai-aegis \
  ~/ops-sys/toolbox/frameworks/12-ops-midas/src/aegis

# 3. If the delta is wanted: re-copy, update the pinned commit above, re-install
rsync -a --exclude='.git' ~/ops-sys/toolbox/frameworks/04-cai-aegis/ \
  ~/ops-sys/toolbox/frameworks/12-ops-midas/src/aegis/
#    (FORK-README.md is ours — restore it if the rsync clobbered it, update the pin)
cp -r ~/ops-sys/toolbox/frameworks/12-ops-midas/src/aegis ~/.base-frameworks/midas/

# 4. Commit in the MIDAS repo with the new pin in the message
```

---
*MIDAS · Chris AI Systems · https://chrisai.cv/skool*
