#!/bin/bash

if [[ $@ == "format" ]] || [[ $@ == "all" ]]; then
    black . --check
fi

if [[ $@ == "lint" ]] || [[ $@ == "all" ]]; then
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
fi

if [[ $@ == "test" ]] || [[ $@ == "all" ]]; then
    pytest . --verbose --junit-xml=test_results/junit.xml
fi
