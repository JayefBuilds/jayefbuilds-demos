#!/usr/bin/env bash
# Pre-push scan. Fails closed. Prints rule name and path:line, never a matched value.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCANNER="$HOME/work/rig/tools/employer-scan/scan.py"
fail=0

# (a) employer and secret scanner
if [ ! -f "$SCANNER" ]; then
  echo "scan: FAIL: employer scanner missing at \$HOME/work/rig/tools/employer-scan/scan.py (failing closed)"
  exit 2
fi
OUT="$(mktemp -d)"
if ! python3 "$SCANNER" --repo "$ROOT" --out "$OUT" >"$OUT/scan.log" 2>&1; then
  echo "scan: FAIL: scanner exited non-zero; log: $OUT/scan.log"
  tail -n 5 "$OUT/scan.log"
  exit 2
fi
if [ ! -f "$OUT/report.json" ]; then
  echo "scan: FAIL: no report.json (failing closed)"; exit 2
fi
if ! python3 - "$OUT/report.json" <<'PY'
import json, sys
r = json.load(open(sys.argv[1]))
bad = 0
def walk(o, path=""):
    global bad
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("errors", "scan_errors") and v:
                print(f"scan: scanner reported {k}"); bad += 1
            if isinstance(v, (int, float)) and v and any(t in k.lower() for t in ("employer", "secret", "finding", "hit")) \
               and not any(t in k.lower() for t in ("excluded", "info", "false", "pull")):
                print(f"scan: scanner finding count {path}{k}={v}"); bad += 1
            walk(v, f"{path}{k}.")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}{i}.")
walk(r)
sys.exit(1 if bad else 0)
PY
then
  echo "scan: FAIL: scanner report shows findings (report: $OUT/report.json)"; fail=1
else
  echo "scan: scanner ok (0 findings)"
fi

# (b) pattern grep over the tracked tree at HEAD. Patterns are built from pieces so this file does not match itself.
declare -a RULES=(
  "abs-path-users|/Us""ers/"
  "abs-path-volumes|/Vol""umes/"
  "anthropic-key|sk-""ant-"
  "github-token-ghp|gh""p_"
  "github-pat|github_""pat_"
  "github-token-gho|gh""o_"
  "slack-token|xox""[bp]-"
  "aws-key|AK""IA[0-9A-Z]{16}"
  "private-key|-----BEGIN .*PRIVATE"" KEY"
)
cd "$ROOT" || exit 2
git rev-parse --verify HEAD >/dev/null 2>&1 || { echo "scan: FAIL: no commit at HEAD (failing closed)"; exit 2; }
# Files to check: tracked at HEAD, content read from HEAD (not the working copy).
for rule in "${RULES[@]}"; do
  name="${rule%%|*}"; pat="${rule#*|}"
  hits="$(git grep -n -I -E -e "$pat" HEAD -- . 2>/dev/null | sed -E 's/^HEAD://' | cut -d: -f1,2)"
  if [ -n "$hits" ]; then
    while IFS= read -r h; do echo "scan: FAIL: rule $name at $h"; done <<<"$hits"
    fail=1
  fi
done
# Also check working-tree changes not yet committed, so a hook run sees them.
for rule in "${RULES[@]}"; do
  name="${rule%%|*}"; pat="${rule#*|}"
  hits="$(git grep -n -I -E --untracked -e "$pat" -- . 2>/dev/null | cut -d: -f1,2)"
  if [ -n "$hits" ]; then
    while IFS= read -r h; do echo "scan: FAIL: rule $name at $h (working tree)"; done <<<"$hits"
    fail=1
  fi
done
[ "$fail" = 0 ] && echo "scan: ok"
exit "$fail"
