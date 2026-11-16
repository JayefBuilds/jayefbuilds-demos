# FP06: Claude Didn't Know What Codex Knew. I Fixed That.

YouTube: https://youtu.be/ZnfVsmw5Xqs

## What the viewer sees

- A project folder: `CLAUDE.md` is renamed to `AGENTS.md`, then a tiny `CLAUDE.md` with one line, `@AGENTS.md`.
- Three terminals (Claude Code, Codex, Pi) get the same question: "Who am I, and what are we working on?" All three read the same rules file.
- One skills folder, `~/.agents/skills/`, is the catalog. Codex and Pi already load skills from there.
- Claude Code loads skills from `~/.claude/skills/`, so each skill gets one `ln -s` link (a signpost to the catalog, not a copy).
- A new skill, `commit-style`, is written in the catalog. Claude uses it after one `ln -s` line.

## Honest gap

By hand, Claude Code needs the link step for every new skill. The watcher (below) now does that step on its own.

## Reproduce it

Needs Claude Code, Codex and Pi installed. The demo uses a clean home folder, so nothing touches your real one.

1. Build the demo home. `bash setup.sh ~/fp06-demo-home` (default: `./demo-home`). It copies `home/.agents/skills/` (the catalog: `create-coach`, `meeting-notes`, `plain-words`, `commit-style`) and `home/projects/` (`teach-once`, `claims-a`, `claims-b`), then links every catalog skill except `commit-style` into `.claude/skills/`.
2. Use that folder as `HOME` for each agent, and sign in there yourself. The repo holds no logins.
3. Rules file. In `projects/teach-once/`: `mv CLAUDE.md AGENTS.md`, then write a `CLAUDE.md` whose first line is `@AGENTS.md` (the copy in the repo is the finished state; the video shows the rename).
4. Ask all three: "Who am I, and what are we working on?" `claims-a` (AGENTS.md only, codename Kestrel-17) and `claims-b` (CLAUDE.md with `@AGENTS.md` plus a Claude-only word) are the checks that Claude reads `AGENTS.md` alone and follows the `@` line.
5. Skills. Codex and Pi load from `~/.agents/skills/`. Claude Code follows the per-skill link in `~/.claude/skills/`: `ln -s ~/.agents/skills/create-coach ~/.claude/skills/create-coach`.
6. The new skill. The catalog already holds `commit-style`. To repeat the on-camera write, remove its folder and type it again (text in `home/.agents/skills/commit-style/SKILL.md`). Open three new sessions. Codex and Pi list it with no extra step. Link it for Claude: `ln -s ~/.agents/skills/commit-style ~/.claude/skills/commit-style`. Then ask each agent: "Use the commit-style skill. Write a commit message for: added a retry to the login request."

Keep the top of each `SKILL.md` to `name` and `description` only, so every tool accepts it.

## The watcher

`watcher/skill-sync.py` keeps one skills catalog, `~/.agents/skills`.
A new skill in `~/.claude/skills`, `~/.codex/skills` or `~/.pi/agent/skills` is moved into the catalog. A link is left at the old path.
Every catalog skill gets a link in `~/.claude/skills`, so every tool can see it.
It never deletes or overwrites anything. Python 3, standard library only. It polls every 2 seconds (no `fswatch`: polling is simpler).

Only `~/.claude/skills` gets links by default. Codex and Pi already read `~/.agents/skills`, and a second link would show each skill twice. To link another folder, add `--link-dir DIR` (repeat it for more).

Install:

```sh
mkdir -p ~/bin && cp watcher/skill-sync.py ~/bin/ && chmod +x ~/bin/skill-sync.py
```

Run:

```sh
skill-sync.py            # run until Ctrl+C
skill-sync.py --once     # one pass, then exit
skill-sync.py --dry-run  # show what would change, change nothing (one pass)
```

Run in the background on macOS:

```sh
cp watcher/com.example.skill-sync.plist ~/Library/LaunchAgents/
# edit the file: set the two path placeholders (the script and the log) to full paths
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.example.skill-sync.plist
```

On Linux, `watcher/skill-sync.service` is a systemd user unit. The header comment says how to use it.

Stop: `launchctl bootout gui/$(id -u)/com.example.skill-sync`, or Ctrl+C if it runs in a terminal.

Uninstall: run the `bootout` line, then remove the plist and `~/bin/skill-sync.py`. The links it made stay. They are harmless. Nothing in the catalog changes.

Conflict: if a skill has the same name in the catalog and as a real folder in a tool folder, the watcher logs `conflict <name>` once and leaves both alone. Compare the two, keep one, and remove the other by hand. Then the next pass links it.

## Notes

- The skill files are rewritten stand-ins, not the real skills from the channel's own setup. The video shows the earlier `alex-create-coach` name; this reusable demo uses `create-coach`.
- `commit-style` is rebuilt from the recording runner's heredoc text (the exact text typed in beat S4a).
- At the time of writing, Codex and Pi answers using a skill were not yet recorded (usage cap); the loading was checked, the final answers were not.
- `setup.sh` makes the symlinks. The repo does not commit any.
