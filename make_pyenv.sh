#!/usr/bin/env bash
mkdir .pyenv
python3 -m venv .pyenv/
source .pyenv/bin/activate && pip3 install -r requirements.txt