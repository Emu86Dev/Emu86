#!/usr/bin/env bash
# Superset workspace setup for Emu86. Idempotent: safe to re-run.
set -euo pipefail
cd "${SUPERSET_WORKSPACE_PATH:-$(git rev-parse --show-toplevel)}"
ROOT="${SUPERSET_ROOT_PATH:-}"

echo "==> Copying untracked env files from main checkout"
if [ -n "$ROOT" ] && [ "$ROOT" != "$PWD" ]; then
  shopt -s nullglob
  for f in "$ROOT"/.env "$ROOT"/*.env; do
    [ -f "$f" ] || continue
    cp -p "$f" "./$(basename "$f")"
    echo "    copied $(basename "$f")"
  done
  shopt -u nullglob
fi

echo "==> Initializing git submodules (utils, ASM_Comment_Shortcut)"
git submodule update --init --recursive || echo "    WARNING: submodule init failed (offline?); continuing"

echo "==> Python virtualenv (venv/)"
# Django 4.2 supports Python <= 3.12, so don't use a newer default python3.
if [ ! -x venv/bin/python ]; then
  PY=""
  for cand in python3.11 python3.12; do
    if command -v "$cand" >/dev/null 2>&1; then PY="$cand"; break; fi
  done
  if [ -z "$PY" ]; then
    echo "ERROR: need python3.11 or python3.12 (Django 4.2 doesn't support newer)" >&2
    exit 1
  fi
  "$PY" -m venv venv
fi
if command -v uv >/dev/null 2>&1; then
  uv pip install --python venv/bin/python -q -r docker/requirements-dev.txt
else
  venv/bin/pip install -q --disable-pip-version-check -r docker/requirements-dev.txt
fi

echo "==> Node dev deps (eslint)"
if command -v npm >/dev/null 2>&1; then
  npm ci --no-audit --no-fund --loglevel=error || echo "    WARNING: npm ci failed; lint tools unavailable"
else
  echo "    npm not found; skipping"
fi

echo "==> Setup complete. Click Run (or: bash .superset/run.sh) to start the dev server."
