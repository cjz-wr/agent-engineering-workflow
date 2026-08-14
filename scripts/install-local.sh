#!/usr/bin/env bash
# Install the two agent-engineering skills into a local Agent client skills directory.
#
# Local-only install: no network access, no npm/pip install.
# Existing skills are never silently overwritten.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"

SKILLS=(project-bootstrap-workflow feature-change-workflow)

usage() {
  cat <<EOF
Usage: $0 <target> [--user]

Install the two agent-engineering skills into a local skills directory.

Targets:
  codex     .agents/skills/    (user-level: ~/.agents/skills/)
  claude    .claude/skills/    (user-level: ~/.claude/skills/)
  cursor    .cursor/skills/    (user-level: ~/.cursor/skills/)

Options:
  --user    install to the user-level directory instead of project-level
  -h, --help  show this help

Examples:
  $0 codex
  $0 claude --user
EOF
}

TARGET=""
USER_LEVEL=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    codex|claude|cursor)
      TARGET="$1"
      ;;
    --target)
      shift
      [[ $# -gt 0 ]] || { echo "error: --target requires a value" >&2; exit 1; }
      TARGET="$1"
      ;;
    --user)
      USER_LEVEL=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
  shift
done

if [[ -z "$TARGET" ]]; then
  echo "error: no target specified" >&2
  usage
  exit 1
fi

# Validate target platform
case "$TARGET" in
  codex)  REL=".agents/skills" ;;
  claude) REL=".claude/skills" ;;
  cursor) REL=".cursor/skills" ;;
  *) echo "error: unsupported target: $TARGET" >&2; exit 1 ;;
esac

# Validate source
if [[ ! -d "$SKILLS_SRC" ]]; then
  echo "error: skills source directory not found: $SKILLS_SRC" >&2
  exit 1
fi
for s in "${SKILLS[@]}"; do
  if [[ ! -d "$SKILLS_SRC/$s" ]]; then
    echo "error: skill source missing: $SKILLS_SRC/$s" >&2
    exit 1
  fi
done

if [[ "$USER_LEVEL" -eq 1 ]]; then
  DEST_ROOT="${HOME}/${REL}"
else
  DEST_ROOT="${PWD}/${REL}"
fi

echo "Installing skills into: $DEST_ROOT"
mkdir -p "$DEST_ROOT"

status=0
for s in "${SKILLS[@]}"; do
  dst="$DEST_ROOT/$s"
  if [[ -e "$dst" ]]; then
    echo "SKIP: $dst already exists — refusing to overwrite." >&2
    status=1
    continue
  fi
  cp -R "$SKILLS_SRC/$s" "$dst"
  echo "OK: installed $s -> $dst"
done

if [[ "$status" -ne 0 ]]; then
  echo "" >&2
  echo "One or more skills already existed and were not overwritten." >&2
  echo "To install manually, copy the skill directories under:" >&2
  echo "  $SKILLS_SRC" >&2
  echo "into:" >&2
  echo "  $DEST_ROOT" >&2
  exit 1
fi

echo ""
echo "Done. Two skills installed. Verify with your client's skill discovery."
