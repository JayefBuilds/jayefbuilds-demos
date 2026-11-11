# WORKLOG

## Next Up / Open To-Dos
- Make the repo public and add a LICENSE (MIT) at the FP06 publish, with the Admiral's go. Run both checks first.
- Replace the YouTube placeholder in `fp06-claude-didnt-know-what-codex-knew/README.md` with the real link at publish.
- Re-check the FP06 steps for Codex and Pi after the OpenAI cap lifts (2026-11-11 21:08 UTC).
- Check whether Codex or Pi list a skill twice when the watcher leaves a link in `~/.codex/skills` or `~/.pi/agent/skills` (FP06 S5c and H1 takes show it).

## 2026-11-11: FP06 skill watcher (ship jayefbuilds-18)
- `fp06-claude-didnt-know-what-codex-knew/watcher/skill-sync.py`: moves new skills from the Claude, Codex and Pi folders into `~/.agents/skills` and links them back; links every catalog skill into `~/.claude/skills`. Never deletes or overwrites; flags same-name conflicts once. `--once`, `--dry-run`, polling loop; an OS error in a pass is logged and the loop goes on.
- launchd plist and systemd unit examples; README section "The watcher" (install, run, stop, uninstall).
- Tested in a temporary home: link, move from `.claude` and `.codex`, conflict, dry run, no home path in the log, `plutil -lint`.

## 2026-11-10: scan checks every commit; first push (ship jayefbuilds-13)
- `scripts/scan.sh` pattern grep now reads every commit on every branch, not only HEAD. Negative test: a path in an old commit fails the scan.
- Private GitHub repo `JayefBuilds/jayefbuilds-demos` created; `build` merged to `main` and pushed through the pre-push hook.

## 2026-11-10: repo created (ship jayefbuilds-13)
- Root files, `scripts/check-structure.py`, `scripts/scan.sh`, pre-push hook and installer.
- First video folder: `fp06-claude-didnt-know-what-codex-knew/` with a demo-home builder (`setup.sh`).
