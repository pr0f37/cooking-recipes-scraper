#!/bin/bash

# alembic upgrade head
uvicorn 'cr_scraper.api.main:app' --host=0.0.0.0 --port=8000
