#!/bin/bash

flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude playground.py
flake8 . --count --max-complexity=10 --max-line-length=127 --statistics --exclude playground.py