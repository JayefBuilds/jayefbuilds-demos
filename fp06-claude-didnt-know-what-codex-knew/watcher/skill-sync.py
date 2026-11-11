#!/usr/bin/env python3
"""skill-sync: keep one skills catalog, and let every AI tool see it.

The catalog is ~/.agents/skills. A skill is a folder with a SKILL.md in it.

Every pass does three things:
  1. Adopt.  A new skill (a real folder) in ~/.claude/skills, ~/.codex/skills
     or ~/.pi/agent/skills is moved into the catalog. A link is left at the
     old path, so the tool that made it still finds it.
  2. Flag.   If the catalog and a tool folder each hold a real folder with the
     same name, nothing is touched. The script tells you once. You clean up.
  3. Link.   Each catalog skill gets a link in the link folders (default:
     ~/.claude/skills), because Claude Code does not read the catalog itself.

It never deletes or overwrites anything. Standard library only.

  skill-sync.py            run until Ctrl+C (checks every 2 seconds)
  skill-sync.py --once     one pass, then exit
  skill-sync.py --dry-run  show what would change, change nothing (one pass)
"""
import argparse
import os
import shutil
import sys
import time

MIN_AGE = 2  # seconds a skill must sit unchanged before it is moved
HOME = os.environ.get("HOME") or os.path.expanduser("~")
AGENT_DIRS = ["~/.claude/skills", "~/.codex/skills", "~/.pi/agent/skills"]
flagged = set()  # warnings already printed in this run


def full(path):
    """Turn a leading ~ into the home folder (read from $HOME at run time)."""
    return os.path.join(HOME, path[2:]) if path.startswith("~/") else path


def short(path):
    """Show the home folder as ~ so logs never carry a real user name."""
    path = os.path.abspath(path)
    if path == HOME:
        return "~"
    if path.startswith(HOME + os.sep):
        return "~" + path[len(HOME):]
    return path


def log(msg):
    print(time.strftime("%H:%M:%S ") + msg, flush=True)


def is_skill(path):
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, "SKILL.md"))


def is_real_skill(path):
    return not os.path.islink(path) and is_skill(path)


def list_skills(folder, real_only=False):
    """Names of skills in a folder. Missing folder: empty list."""
    try:
        names = sorted(os.listdir(folder))
    except OSError:
        return []
    check = is_real_skill if real_only else is_skill
    return [n for n in names if check(os.path.join(folder, n))]


def newest_age(path):
    """Seconds since the newest change inside a folder."""
    newest = os.lstat(path).st_mtime
    for root, dirs, files in os.walk(path):
        for n in dirs + files:
            try:
                newest = max(newest, os.lstat(os.path.join(root, n)).st_mtime)
            except OSError:
                pass
    return time.time() - newest


def flag_once(key, msg):
    if key not in flagged:
        flagged.add(key)
        log(msg)


def one_pass(catalog, agent_dirs, link_dirs, dry):
    mv, ln = ("would move", "would link") if dry else ("moved", "linked")
    cat = full(catalog)

    # 1. Adopt new skills from the tool folders.
    for folder in agent_dirs:
        for name in list_skills(full(folder), real_only=True):
            src = os.path.join(full(folder), name)
            dst = os.path.join(cat, name)
            if os.path.lexists(dst):
                continue  # same name in the catalog: step 2 flags it
            if newest_age(src) < MIN_AGE:
                continue  # still being written; try again next pass
            if not dry:
                os.makedirs(cat, exist_ok=True)
                shutil.move(src, dst)
                os.symlink(dst, src)
            log(f"{mv} {name}: {folder} -> {catalog} (linked back)")

    # 2. Flag same-name real folders. Touch neither.
    for name in list_skills(cat, real_only=True):
        places = [short(os.path.join(full(f), name)) for f in agent_dirs
                  if is_real_skill(os.path.join(full(f), name))]
        if places:
            flag_once(("conflict", name),
                      f"conflict {name}: in {catalog}/{name} and in {', '.join(places)}; left both alone")

    # 3. Link every catalog skill into the link folders.
    for folder in link_dirs:
        for name in list_skills(cat):
            target = os.path.join(cat, name)
            link = os.path.join(full(folder), name)
            if os.path.islink(link):
                if os.path.realpath(link) != os.path.realpath(target):
                    flag_once(("elsewhere", link),
                              f"skipped {name}: {folder}/{name} points to "
                              f"{short(os.readlink(link))}, not {catalog}/{name}; left alone")
                continue
            if os.path.lexists(link):
                continue  # a file or folder is already there: never touch it
            if not dry:
                os.makedirs(full(folder), exist_ok=True)
                os.symlink(target, link)
            log(f"{ln} {name} -> {folder}")


def main():
    p = argparse.ArgumentParser(description="Move new skills into one catalog and link them back.")
    p.add_argument("--catalog", default="~/.agents/skills", help="catalog folder (default: ~/.agents/skills)")
    p.add_argument("--link-dir", action="append", default=None, metavar="DIR",
                   help="folder that gets a link per catalog skill; repeat to add more "
                        "(default: ~/.claude/skills)")
    p.add_argument("--interval", type=float, default=2.0, help="seconds between passes (default: 2)")
    p.add_argument("--once", action="store_true", help="run one pass and exit")
    p.add_argument("--dry-run", action="store_true", help="show what would change; change nothing (one pass)")
    a = p.parse_args()
    link_dirs = a.link_dir or ["~/.claude/skills"]
    # Show paths the way the user typed them (~ stays ~).
    shown = [a.catalog] + [d for d in AGENT_DIRS]
    log("watching " + ", ".join(short(full(d)) for d in shown))
    try:
        while True:
            try:
                one_pass(a.catalog, AGENT_DIRS, link_dirs, a.dry_run)
            except OSError as e:  # for example a folder without permission: log it, keep watching
                log(f"error: {e.strerror}: {short(e.filename or '?')}")
            if a.once or a.dry_run:
                return 0
            time.sleep(a.interval)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())
