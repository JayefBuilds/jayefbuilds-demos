# WORKLOG

## Next Up / Open To-Dos
- Make the repo public and add a LICENSE (MIT) at the FP06 publish, with the Admiral's go. Run both checks first.
- Replace the YouTube placeholder in `fp06-claude-didnt-know-what-codex-knew/README.md` with the real link at publish.
- Re-check the FP06 steps for Codex and Pi after the OpenAI cap lifts (2026-11-11 21:08 UTC).

## 2026-11-10: scan checks every commit; first push (ship jayefbuilds-13)
- `scripts/scan.sh` pattern grep now reads every commit on every branch, not only HEAD. Negative test: a path in an old commit fails the scan.
- Private GitHub repo `JayefBuilds/jayefbuilds-demos` created; `build` merged to `main` and pushed through the pre-push hook.

## 2026-11-10: repo created (ship jayefbuilds-13)
- Root files, `scripts/check-structure.py`, `scripts/scan.sh`, pre-push hook and installer.
- First video folder: `fp06-claude-didnt-know-what-codex-knew/` with a demo-home builder (`setup.sh`).
