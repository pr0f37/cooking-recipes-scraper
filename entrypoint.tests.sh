#!/bin/bash

pytest . --verbose --junit-xml=test_results/junit.xml --cov=/app/src/cr_scraper --cov-report xml:test_results/coverage.xml
