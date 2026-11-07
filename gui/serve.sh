#!/usr/bin/env bash
# Rebuild the Gazette and serve it at http://127.0.0.1:8765 (local only, read-only).
cd "$(dirname "$0")" && python3 build.py && python3 capitol.py && python3 chain.py && cd site && exec python3 -m http.server 8765 --bind 127.0.0.1
