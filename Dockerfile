# NOTE: To run this container with GPU access you must use the NVIDIA Container Toolkit:
#   docker run --gpus all ...
FROM python:3.10

# ENV DEBIAN_FRONTEND=noninteractive
# Fix: uv defaults to hardlinks for cache efficiency, but fails when the cache
# and target are on different filesystems (common in Docker). Setting copy mode
# suppresses the warning and ensures installs always succeed.
ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y \
  python3-tk \
  tk-dev \
  build-essential \
  git \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Register /usr/bin/python -> python3.10.
# Ubuntu 22.04 ships python3.10 as the default python3 already, so no
# override is needed for python3. Only the bare 'python' symlink is missing.
#RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY scripts/ ./scripts/

RUN uv sync --reinstall

RUN uv run python -c "import app; print('APP OK:', app.__file__)"

RUN useradd --create-home --shell /bin/bash appuser \
  && chown -R appuser:appuser /app

USER appuser

# Fix: 'uv run python -m app.main' launches a bare Python process that doesn't
# have the src/ layout on sys.path, so 'app' is not found.
# Using the console script defined in pyproject.toml ([project.scripts]:
# tkinter-app = "app.main:main") runs the correct venv entry point directly.
#ENTRYPOINT ["/app/.venv/bin/tkinter-app"]
