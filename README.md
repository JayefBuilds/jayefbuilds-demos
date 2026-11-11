# jayefbuilds-demos

Demo files for every jayefbuilds YouTube video. If you want to repeat what a video shows, start in that video's folder.

## Folder rule

- One folder per video, at the top level.
- The folder name is `<id>-<slug>`, lowercase, exactly as the folder in the island repo `videos/` (for example `fp06-claude-didnt-know-what-codex-knew`).
- Each video folder has a `README.md`: what the viewer sees, the YouTube link, and the steps to reproduce the demo.
- `scripts/` holds the checks. Dot-folders are tooling.

## Big-project rule

A project that is big enough to need its own repo gets its own repo. Its folder here holds only a `README.md` with the link to that repo.

- No nested repos. No submodules.
- No file over 1 MiB.

## Checks

```sh
python3 scripts/check-structure.py      # folder names, READMEs, no nested .git, no .gitmodules, no file over 1 MiB
bash scripts/scan.sh                    # pre-push scan: employer and secret scanner, plus a pattern grep
bash scripts/install-hooks.sh           # once per clone: runs both checks before every push
```

The repo is private until the first video that uses it is published. See `LICENSE-TODO.md`.
