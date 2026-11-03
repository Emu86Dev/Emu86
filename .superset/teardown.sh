#!/usr/bin/env bash
# Stop the dev server started by .superset/run.sh (setup starts no services).
set -uo pipefail
cd "${SUPERSET_WORKSPACE_PATH:-$(git rev-parse --show-toplevel)}" || exit 0

PORTFILE=.superset/.run-port
if [ -f "$PORTFILE" ]; then
  PORT="$(cat "$PORTFILE")"
  # Kill by port: Django's autoreloader forks a child that holds the socket.
  PIDS="$(lsof -ti "tcp:$PORT" -sTCP:LISTEN 2>/dev/null || true)"
  if [ -n "$PIDS" ]; then
    echo "==> Stopping dev server on port $PORT (pids: $(echo $PIDS))"
    kill $PIDS 2>/dev/null || true
  fi
  rm -f "$PORTFILE"
fi
# Also stop any runserver whose working directory is this worktree
# (match by cwd: macOS framework Python rewrites the process command line).
HERE="$(pwd -P)"
for pid in $(pgrep -f "manage.py runserver" 2>/dev/null); do
  cwd="$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')"
  if [ "$cwd" = "$HERE" ]; then
    echo "==> Stopping runserver pid $pid"
    kill "$pid" 2>/dev/null || true
  fi
done
exit 0
