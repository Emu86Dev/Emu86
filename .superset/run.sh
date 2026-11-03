#!/usr/bin/env bash
# Launch the Django dev server on a per-workspace port.
set -euo pipefail
cd "${SUPERSET_WORKSPACE_PATH:-$(git rev-parse --show-toplevel)}"

if [ ! -x venv/bin/python ]; then
  echo "venv/ missing; run: bash .superset/setup.sh" >&2
  exit 1
fi

# Load env vars from .env if present.
if [ -f .env ]; then set -a; . ./.env; set +a; fi

# settings.py reads SECRET_KEY from the environment only.
if [ -z "${SECRET_KEY:-}" ]; then
  SECRET_KEY="$(venv/bin/python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
  export SECRET_KEY
fi

# Pick a port: stable hash of the workspace name into 8000-8999,
# then probe upward until one is free, so parallel workspaces don't collide.
NAME="${SUPERSET_WORKSPACE_NAME:-$(basename "$PWD")}"
PORT="$(venv/bin/python - "$NAME" <<'PY'
import socket, sys, zlib
start = 8000 + zlib.crc32(sys.argv[1].encode()) % 1000
for i in range(1000):
    port = 8000 + (start - 8000 + i) % 1000
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", port))
    except OSError:
        continue
    finally:
        s.close()
    print(port)
    break
else:
    sys.exit("no free port in 8000-8999")
PY
)"
echo "$PORT" > .superset/.run-port

echo "==> Emu86 dev server: http://127.0.0.1:$PORT/"
exec "$PWD/venv/bin/python" manage.py runserver "127.0.0.1:$PORT"
