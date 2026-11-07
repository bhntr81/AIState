#!/usr/bin/env bash
# Free Bitcoin timestamp of the record via OpenTimestamps (opentimestamps-client, v0.8.0, installed in a venv).
# Usage: anchors/anchor.sh <manifest>. After a few hours run `ots upgrade <manifest>.ots` to embed the Bitcoin block proof.
ots stamp "$1" && echo "stamped $1.ots"
