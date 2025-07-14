# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.13.5
FROM python:${PYTHON_VERSION}-slim AS base

WORKDIR /opt
RUN python -m venv /opt/.venv
# Make sure we use the virtualenv:
ENV PATH="/opt/.venv/bin:$PATH"
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-editable --no-install-project  --active

COPY src src
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv sync --locked --no-editable --active


FROM python:${PYTHON_VERSION}-slim AS build
COPY --from=base /opt/.venv /opt/.venv
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update \
    && apt-get -y install libpq-dev
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

ENV PATH="/opt/.venv/bin:$PATH"
USER appuser
WORKDIR /app

EXPOSE 8000
COPY --chmod=755 docker/dev/entrypoint.sh .
COPY --chmod=755 src src
ENTRYPOINT [ "./entrypoint.sh" ]
