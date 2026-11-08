#!/usr/bin/env bash
# Scheduled wake: one runner cycle (guardrails are enforced inside runner.py, in plain code).
cd "$(dirname "$0")/.." && exec python3 runtime/runner.py cycle >> runtime/tick.log 2>&1
