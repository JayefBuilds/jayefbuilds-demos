#!/usr/bin/env bash
# Build the FP06 demo home. Usage: setup.sh [TARGET_DIR]   (default: $PWD/demo-home)
set -eu
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-$PWD/demo-home}"
case "$TARGET" in /*) ;; *) TARGET="$PWD/$TARGET" ;; esac
if [ -e "$TARGET" ] && [ -n "$(ls -A "$TARGET" 2>/dev/null)" ]; then
  echo "setup: $TARGET exists and is not empty; pick a new path" >&2; exit 1
fi
mkdir -p "$TARGET/.agents" "$TARGET/.claude/skills"
cp -R "$HERE/home/.agents/skills" "$TARGET/.agents/skills"
cp -R "$HERE/home/projects" "$TARGET/projects"
# Claude Code looks only in ~/.claude/skills, so link each catalog skill except commit-style.
# commit-style is the skill the video writes on camera and then links by hand (step 6 in README.md).
for d in "$TARGET/.agents/skills"/*/; do
  name="$(basename "$d")"
  [ "$name" = "commit-style" ] && continue
  ln -s "$TARGET/.agents/skills/$name" "$TARGET/.claude/skills/$name"
done
echo "demo home built at $TARGET"
echo "set HOME=$TARGET for the agents; link commit-style yourself:"
echo "  ln -s \$HOME/.agents/skills/commit-style \$HOME/.claude/skills/commit-style"
