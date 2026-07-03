# MIDAS App Registry

Per-app state for detection and routing. **This table's format is the contract** —
every MIDAS task reads and writes THIS schema; no task invents its own.

**Schema (one row per app):**

| Field | Format | Meaning |
|-------|--------|---------|
| `app` | kebab-case name | The application |
| `path` | absolute path | Repo root on this machine |
| `stage` | `assessed` \| `provisioned` \| `piped` \| `hardened` \| `compliant` | Furthest MIDAS stage completed |
| `last_assessed` | YYYY-MM-DD | Date of most recent `assess` run |
| `posture_score` | 0–100 or `-` | From the latest posture report (`-` = never assessed) |

Per-app artifacts (posture reports, evidence indexes) live at
`~/.base-frameworks/midas/context/{app}/`.

## Registry

| app | path | stage | last_assessed | posture_score |
|-----|------|-------|---------------|---------------|
