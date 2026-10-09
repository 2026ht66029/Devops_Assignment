# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN groupadd --system aceest && useradd --system --gid aceest --home-dir /app aceest

COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt

COPY --chown=aceest:aceest app.py ./
COPY --chown=aceest:aceest aceest ./aceest

FROM base AS test

USER root
COPY requirements-dev.txt pyproject.toml ./
RUN pip install --no-cache-dir --requirement requirements-dev.txt
COPY --chown=aceest:aceest tests ./tests
USER aceest

CMD ["pytest"]

FROM base AS runtime

USER aceest
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2", "app:app"]
