"""Tests for leetcode_list_manager package."""
import re
from pathlib import Path
import tempfile

import pytest

from leetcode_list_manager.manager import ListManager


@pytest.fixture
def temp_markdown():
    """Create a temporary markdown file with problem links."""
    content = """
# LeetCode Problems

- [Two Sum](https://leetcode.com/problems/two-sum/)
- [3Sum](https://leetcode.com/problems/3sum/)
- [Two Sum](https://leetcode.com/problems/two-sum/)  # Duplicate

## Other
- [Binary Search](https://leetcode.com/problems/binary-search/)
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    Path(f.name).unlink()


class MockAPIClient:
    """Mock LeetCode API client for testing."""

    def __init__(self):
        self.calls = []

    def get_question_id(self, slug: str) -> str:
        self.calls.append(("get_question_id", slug))
        # Mock ID mapping
        mapping = {
            "two-sum": "1",
            "3sum": "15",
            "binary-search": "704",
        }
        return mapping.get(slug)

    def add_to_favorite(self, list_id: str, question_id: str) -> bool:
        self.calls.append(("add_to_favorite", list_id, question_id))
        return True


def test_extract_slugs_from_markdown(temp_markdown):
    """Test extracting problem slugs from markdown."""
    mock_client = MockAPIClient()
    manager = ListManager(mock_client)

    slugs = manager.extract_slugs_from_markdown(temp_markdown)

    # Should have 3 unique slugs (two-sum is duplicated)
    assert len(slugs) == 3
    assert "two-sum" in slugs
    assert "3sum" in slugs
    assert "binary-search" in slugs


def test_add_problems_to_list():
    """Test adding problems to a list."""
    mock_client = MockAPIClient()
    manager = ListManager(mock_client, rate_limit_delay=0.01)

    slugs = ["two-sum", "3sum", "binary-search"]
    added, failed = manager.add_problems_to_list("test-list", slugs)

    assert added == 3
    assert len(failed) == 0


def test_add_from_markdown(temp_markdown):
    """Test extracting from markdown and adding to list."""
    mock_client = MockAPIClient()
    manager = ListManager(mock_client, rate_limit_delay=0.01)

    added, failed = manager.add_from_markdown("test-list", temp_markdown)

    assert added == 3
    assert len(failed) == 0


def test_regex_pattern():
    """Test the regex pattern for extracting problem slugs."""
    urls = [
        "https://leetcode.com/problems/two-sum/",
        "https://leetcode.com/problems/3sum",
        "https://leetcode.com/problems/binary-search/",
    ]

    pattern = r"https://leetcode\.com/problems/([a-z0-9-]+)/?"
    slugs = [re.search(pattern, url).group(1) for url in urls]

    assert slugs == ["two-sum", "3sum", "binary-search"]
