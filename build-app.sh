#!/bin/bash -e

. "venv/bin/activate"

pyinstaller \
	--noconfirm \
	--onefile \
	relay-control.py
