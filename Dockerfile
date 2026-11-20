
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Python and uv configuration
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONPATH=/app

# Install dependencies using the lockfile
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

# Copy application source and data
COPY . .

# FastAPI port
EXPOSE 8000

# Default command: FastAPI
CMD ["uv", "run", "--no-sync", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
