#!/bin/bash
bin="$(dirname "${BASH_SOURCE[0]}")"
root="$(dirname "$bin")"
cd $root
source "$root"/env/bin/activate
python3 "$root"/app.py
