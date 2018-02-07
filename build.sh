#!/bin/sh

# build the file using please and move the pex to the root directory
# this is required as please is not compiled for ARM yet.
./pleasew build //.:devils_tower
cp plz-out/bin/devils_tower.pex ./
