#!/bin/bash -e

. "venv/bin/activate"

pyinstaller \
	--name relay-control \
	--noconfirm \
	--onefile \
	--log-level WARN \
	relay-control.py
