#!/bin/bash

pytest . --color=yes --junit-xml=test_results/junit.xml --cov=/app/src/cr_scraper --cov-report xml:test_results/coverage.xml --cov-report term --cov-fail-under=50
