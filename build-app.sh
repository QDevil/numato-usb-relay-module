#!/bin/bash -e

scriptdir=$(realpath `dirname $0`)
workdir=${WORKSPACE:-$(realpath $scriptdir)}
pushd "$workdir"
source "venv/bin/activate"

pyinstaller \
	--noconfirm \
	--onefile \
	relay-control.py

popd
