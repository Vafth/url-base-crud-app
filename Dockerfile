FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 1. Copy only the dependency files first
COPY pyproject.toml uv.lock ./

# 2. Install dependencies (without the app itself)
# --frozen ensures we use the exact versions from uv.lock
RUN uv sync --frozen --no-install-project --no-dev

# 3. Copy the rest of the app
COPY . .

# 4. Use 'uv run' to ensure the environment is correctly loaded
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]