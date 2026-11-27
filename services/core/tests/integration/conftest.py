"""Integration tests run against local Postgres (OMA-13) via `make test-int`.

Every test under this folder gets the `integration` marker, so `make check` skips them.
"""

from pathlib import Path

import pytest

HERE = Path(__file__).parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        if HERE in Path(item.fspath).parents:
            item.add_marker(pytest.mark.integration)
