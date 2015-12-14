#!/bin/sh

if [ $# -eq 0 ]; then
    python -m unittest discover -v
elif [ $1 = "unit" ]; then
    python -m unittest discover -v -p test_unit*$2*.py
elif [ $1 = "performance" ]; then
    python -m unittest discover -v -p test_performance*$2*.py
else
    echo Incorrect parameter \"$1\". Usage runtest.sh [unit\|performance] [\<chapter\>]
fi