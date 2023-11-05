# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.11.5
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /app
RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=poetry.toml,target=poetry.toml \
    --mount=type=bind,source=poetry.lock,target=poetry.lock \
    poetry install --no-directory --only main,db
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip uninstall -y -r requirements.txt


FROM python:${PYTHON_VERSION}-slim as build
COPY --from=base /opt/venv /opt/venv
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

USER appuser
WORKDIR /app
COPY cr_scraper cr_scraper
COPY alembic alembic
COPY alembic.ini .
EXPOSE 8000
ENV PATH="/opt/venv/bin:$PATH"
COPY --chmod=755 docker/dev/entrypoint.sh .
ENTRYPOINT [ "./entrypoint.sh" ]
