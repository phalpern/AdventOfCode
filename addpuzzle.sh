#! /bin/bash

if [ $# < 1 ]; then
    echo >&2 "Usage: $0 <puzzle-number>"
fi

git add puzzle$1*.py puzzle$1*.txt
git status
