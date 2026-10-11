#!/bin/bash
set -euo pipefail

sudo apt install python3-venv python3-pip libglfw3 libportaudio2

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install pyxel

echo "Environment is ready."
echo "Activate it with: source .venv/bin/activate"
