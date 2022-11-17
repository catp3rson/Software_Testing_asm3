#!/bin/bash

# load configs for webdriver manager
export $(grep -v '^#' .webdriver_manager.env | xargs)

# run the tests
if [[ $# -eq 0 ]]
then
    behave
else
    for var in "$@"
    do
        if [[ "$var" = *?.feature ]]
        then
            behave -i $var
        fi
    done
fi
