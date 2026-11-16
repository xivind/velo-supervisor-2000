# Docker file based on this tutorial https://python.plainenglish.io/turn-your-python-script-into-a-real-program-with-docker-c200e15d5265

# Build stage: resolve dependencies and install the package, git is needed for the version
FROM python:3.12-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

# Use uv as a drop in replacement for pip
COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

# Copy the repository, including .git for the version, and install from the lockfile
WORKDIR /app
COPY . .
RUN uv sync --locked --no-dev --no-editable

# Runtime stage: only the virtual environment and the log configuration
FROM python:3.12-slim
RUN useradd --uid 1000 --create-home app
COPY --from=build /app/.venv /app/.venv
COPY config/uvicorn_log_config.ini /app/
ENV PATH="/app/.venv/bin:$PATH" VELO_SUPERVISOR_CONFIG=/data/config.json
WORKDIR /app
USER app

# Expose the port your application runs on
EXPOSE 8000

# Command to run your application using Uvicorn
CMD ["uvicorn", "velo_supervisor.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "/app/uvicorn_log_config.ini"]

# Healthcheck to monitor the container for errors, see src/velo_supervisor/healthcheck.py
HEALTHCHECK --interval=600s --timeout=5s --retries=3 CMD ["python", "-m", "velo_supervisor.healthcheck"]
