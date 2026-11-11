#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
chmod +x "$ROOT/.githooks/pre-push" "$ROOT/scripts/"*.sh "$ROOT/scripts/check-structure.py"
git -C "$ROOT" config core.hooksPath .githooks
echo "core.hooksPath=$(git -C "$ROOT" config core.hooksPath)"
