#!/usr/bin/env bash
# This script renames all folders in the given directory

# Check if the user has provided a directory
if [ -z "$1" ]; then
    echo "Please provide a directory"
    exit 1
fi

# Check if the directory exists
if [ ! -d "$1" ]; then
    echo "Directory does not exist"
    exit 1
fi

find "$1" -type f -name "*.c" | while read -r file; do
    # Estrai la directory del file corrente
    dir=$(dirname "$file")

    # Rinomina il file in lanterne_estive.c
    mv "$file" "$dir/percorsi.c" 2>/dev/null
done

exit 0
