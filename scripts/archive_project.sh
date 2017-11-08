#!/bin/bash
pushd /f/Projects/
git add .
git commit -m "project file archive: $(date +%FT%H:%M)"
popd
