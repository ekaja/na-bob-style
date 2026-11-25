#!/usr/bin/env bash
# ติดตั้ง na-bob-style เป็น skill ส่วนตัวของ Claude Code (ไม่ผ่าน marketplace)
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills/na-bob-style"
mkdir -p "$HOME/.claude/skills"
if [ -d "$DEST" ]; then mv "$DEST" "$DEST.bak.$(date +%s)"; fi
cp -r "$DIR/plugins/na-bob-style/skills/na-bob-style" "$HOME/.claude/skills/"
echo "ติดตั้งแล้วที่ $DEST"
