#!/usr/bin/env bash

python3 get_names.py $1
bash renamer.sh $1

exit 0
