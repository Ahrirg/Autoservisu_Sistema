uv sync
uv run ruff check --fix .
uv run ruff format .
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run ty check
Write-Output "all tests passed!"