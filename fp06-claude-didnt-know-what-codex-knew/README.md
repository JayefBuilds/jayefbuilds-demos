# FP06: Claude Didn't Know What Codex Knew. I Fixed That.

YouTube: _TBD at publish_

## What the viewer sees

- A project folder: `CLAUDE.md` is renamed to `AGENTS.md`, then a tiny `CLAUDE.md` with one line, `@AGENTS.md`.
- Three terminals (Claude Code, Codex, Pi) get the same question: "Who am I, and what are we working on?" All three read the same rules file.
- One skills folder, `~/.agents/skills/`, is the catalog. Codex and Pi already load skills from there.
- Claude Code loads skills from `~/.claude/skills/`, so each skill gets one `ln -s` link (a signpost to the catalog, not a copy).
- A new skill, `commit-style`, is written in the catalog. Claude uses it after one `ln -s` line.

## Honest gap

Claude Code needs the link step for every new skill. There is no watcher yet that does it on its own. The video says so, and Section 5 of the script is for the watcher.

## Reproduce it

Needs Claude Code, Codex and Pi installed. The demo uses a clean home folder, so nothing touches your real one.

1. Build the demo home. `bash setup.sh ~/fp06-demo-home` (default: `./demo-home`). It copies `home/.agents/skills/` (the catalog: `alex-create-coach`, `meeting-notes`, `plain-words`, `commit-style`) and `home/projects/` (`teach-once`, `claims-a`, `claims-b`), then links every catalog skill except `commit-style` into `.claude/skills/`.
2. Use that folder as `HOME` for each agent, and sign in there yourself. The repo holds no logins.
3. Rules file. In `projects/teach-once/`: `mv CLAUDE.md AGENTS.md`, then write a `CLAUDE.md` whose first line is `@AGENTS.md` (the copy in the repo is the finished state; the video shows the rename).
4. Ask all three: "Who am I, and what are we working on?" `claims-a` (AGENTS.md only, codename Kestrel-17) and `claims-b` (CLAUDE.md with `@AGENTS.md` plus a Claude-only word) are the checks that Claude reads `AGENTS.md` alone and follows the `@` line.
5. Skills. Codex and Pi load from `~/.agents/skills/`. Claude Code follows the per-skill link in `~/.claude/skills/`: `ln -s ~/.agents/skills/alex-create-coach ~/.claude/skills/alex-create-coach`.
6. The new skill. The catalog already holds `commit-style`. To repeat the on-camera write, remove its folder and type it again (text in `home/.agents/skills/commit-style/SKILL.md`). Open three new sessions. Codex and Pi list it with no extra step. Link it for Claude: `ln -s ~/.agents/skills/commit-style ~/.claude/skills/commit-style`. Then ask each agent: "Use the commit-style skill. Write a commit message for: added a retry to the login request."

Keep the top of each `SKILL.md` to `name` and `description` only, so every tool accepts it.

## Notes

- The skill files are rewritten stand-ins, not the real skills from the channel's own setup.
- `commit-style` is rebuilt from the recording runner's heredoc text (the exact text typed in beat S4a).
- At the time of writing, Codex and Pi answers using a skill were not yet recorded (usage cap); the loading was checked, the final answers were not.
- `setup.sh` makes the symlinks. The repo does not commit any.
