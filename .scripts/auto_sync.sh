#!/bin/bash
cd ~/.qclaw/workspace || exit 1
git add -A
git commit -m "Auto sync: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null
git pull --rebase origin main 2>/dev/null
git push origin main 2>/dev/null
