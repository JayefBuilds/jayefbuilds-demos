# jayefbuilds-demos agent rules

Shared rules come from rig: `~/.claude/CLAUDE.md` and `~/.config/rig/docs/`.
This repo holds the demo files for each jayefbuilds video. The video production island is `~/jayef/library/youtube/jayefbuilds` (naming and the tracker: its `AGENTS.md` and `videos/index.json`).

## Rules
- One top-level folder per video, named `<id>-<slug>` in lowercase, the same as the island `videos/` folder.
- Every video folder has a `README.md`.
- A project big enough for its own repo gets its own repo. Its folder here holds only a `README.md` with the link.
- No nested `.git`, no `.gitmodules`, no file over 1 MiB, no committed symlinks.
- No secrets, no developer-specific absolute paths, no employer or work material. Use `$HOME`, `~` and `Path.home()`.
- Work on a branch. Never push from an agent without the Ship Captain's go. The repo is private until publish.

## Commands
| Task | Command |
| --- | --- |
| Structure check (pass: exit 0) | `python3 scripts/check-structure.py [--island PATH]` |
| Pre-push scan (pass: exit 0) | `bash scripts/scan.sh` |
| Install the pre-push hook | `bash scripts/install-hooks.sh` |

Run both checks before every push. The hook `.githooks/pre-push` runs them.
The scan needs `~/work/rig/tools/employer-scan/scan.py`. If it is missing, the scan fails.
