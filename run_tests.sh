#!/bin/bash

# load configs for webdriver manager
export $(grep -v '^#' .webdriver_manager.env | xargs)

# run the tests
if [[ $# -eq 0 ]]
then
    python -m unittest discover -s test_cases -p "TC_*_*.py"
else
    for var in "$@"
    do
        python -m unittest discover -s test_cases/$var -p "TC_*_*.py"
    done
fi
