#!/usr/bin/env python3
"""Structure check for jayefbuilds-demos. Exit 0 pass, 1 fail, one line per problem."""
import argparse
import re
import subprocess
import sys
from pathlib import Path

MAX_BYTES = 1024 * 1024
FALLBACK = re.compile(r"^[a-z]+[0-9]+-[a-z0-9-]+$")
DEFAULT_ISLAND = Path.home() / "jayef/library/youtube/jayefbuilds"


def island_folders(island):
    videos = island / "videos"
    if not videos.is_dir():
        return None
    return {p.name for p in videos.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))}


def big_files(root):
    """Tracked plus untracked-not-ignored files over the limit; fall back to a walk."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            capture_output=True, check=True).stdout.decode().split("\0")
        files = [root / f for f in out if f]
    except (subprocess.CalledProcessError, FileNotFoundError):
        files = [p for p in root.rglob("*") if p.is_file() and ".git" not in p.relative_to(root).parts]
    return [f for f in files if f.is_file() and not f.is_symlink() and f.stat().st_size > MAX_BYTES]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--island", type=Path, default=DEFAULT_ISLAND)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    a = ap.parse_args()
    root = a.root.resolve()
    problems = []

    known = island_folders(a.island.expanduser())
    if known is None:
        print(f"warning: island not found at {a.island}; using pattern {FALLBACK.pattern}", file=sys.stderr)

    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        if d.name == "scripts" or d.name.startswith("."):
            continue
        ok = (d.name in known) if known is not None else bool(FALLBACK.match(d.name))
        if not ok:
            problems.append(f"{d.name}: not a video folder (expected <id>-<slug> from the island videos/ folder)")
        if not (d / "README.md").is_file():
            problems.append(f"{d.name}: missing README.md")

    for p in root.rglob(".git"):
        if p.relative_to(root) != Path(".git"):
            problems.append(f"{p.relative_to(root)}: nested .git")
    if (root / ".gitmodules").exists():
        problems.append(".gitmodules: submodules are not allowed")
    for f in big_files(root):
        problems.append(f"{f.relative_to(root)}: over 1 MiB")

    for line in problems:
        print(line)
    if not problems:
        print("check-structure: ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
