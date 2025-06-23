#!/usr/bin/env bash
# Author: Matteo Spanio <spanio@dei.unipd.it>
#
# Arguments:
#   -d --> the .zip file containing solutions downloaded from moodle
#   -z --> the destination folder where to unzip the files
# Example:
#   ./main.sh -d solutions -z submissions.zip

TEMP=$(getopt -o 'd:z:h' -n 'submission-unpacker' -- "$@")

if [ $? -ne 0 ]; then
    echo 'Terminating...' >&2
    exit 1
fi

eval set -- "$TEMP"
unset TEMP

while true; do
    case "$1" in
        '-d')
            DIR=$2
            echo "$DIR"
            shift 2
            continue
            ;;
        '-z')
            ZIP=$2
            echo "$ZIP"
            shift 2
            continue
            ;;
        '-h')
            echo 'Usage: submission-unpacker.sh -d <dir> -z <zip>'
            echo 'Options:'
            echo '  -d <dir>  the destination folder where to unzip the files'
            echo '  -z <zip>  the .zip file containing solutions downloaded from moodle'
            echo '  -h        show this help message'
            exit 0
            ;;
        '--')
            shift
            break
            ;;
        *)
            echo 'Internal error!' >&2
            exit 1
            ;;
    esac
done

unzip "$ZIP" -d "$DIR"
python3 get_names.py "$DIR"
bash renamer.sh "$DIR"

exit 0
