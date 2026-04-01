#!/usr/bin/env bash
# Bamboo post-session hook — captures analysis code diffs silently
# Install in ~/.claude/settings.json under hooks.Stop
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
bash "$SKILL_DIR/scripts/sync.sh" capture > /dev/null 2>&1 &
