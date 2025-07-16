# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.13.5
FROM python:${PYTHON_VERSION}-slim AS base
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

WORKDIR /opt

ENV VIRTUAL_ENV=/opt/.venv
RUN python -m venv ${VIRTUAL_ENV}
# Make sure we use the virtualenv:
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install --no-cache-dir -r requirements.txt

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-editable --no-install-project  --active

COPY src src
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv sync --locked --no-editable --active


FROM python:${PYTHON_VERSION}-slim AS db_migration
RUN apt-get update \
    && apt-get -y install libpq-dev

ENV VIRTUAL_ENV=/opt/.venv
COPY --from=base ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY alembic alembic
COPY alembic.ini .
CMD ["alembic", "upgrade", "head"]

FROM python:${PYTHON_VERSION}-slim AS tests_lint_format
RUN apt-get update \
    && apt-get -y install libpq-dev

ENV VIRTUAL_ENV=/opt/.venv
COPY --from=base ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY tests tests
COPY src src
COPY pytest.ini .
COPY --chmod=755 entrypoint.tests.sh .
COPY --chmod=755 entrypoint.format.sh .
COPY --chmod=755 entrypoint.lint.sh .

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv sync --locked  --active --group test --group dev

ENTRYPOINT ["./entypoint.tests.sh"]


FROM python:${PYTHON_VERSION}-slim AS build
RUN apt-get update \
    && apt-get -y install libpq-dev

ENV VIRTUAL_ENV=/opt/.venv
COPY --from=base ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

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

EXPOSE 8000
COPY --chmod=755 entrypoint.sh .
COPY --chmod=755 src src
ENTRYPOINT [ "./entrypoint.sh" ]
