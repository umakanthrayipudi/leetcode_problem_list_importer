"""LeetCode list manager - extract and add problems to lists."""
import logging
import re
import time
from pathlib import Path
from typing import List, Optional

from .api import LeetCodeAPIClient

logger = logging.getLogger(__name__)


class ListManager:
    """Manage LeetCode problem lists."""

    def __init__(
        self,
        api_client: LeetCodeAPIClient,
        rate_limit_delay: float = 1.0,
    ) -> None:
        """
        Initialize list manager.

        Args:
            api_client: LeetCodeAPIClient instance
            rate_limit_delay: Delay between API calls in seconds
        """
        self.api_client = api_client
        self.rate_limit_delay = rate_limit_delay

    def extract_slugs_from_markdown(self, md_path: str) -> List[str]:
        """
        Extract unique problem slugs from markdown file.

        Args:
            md_path: Path to markdown file with problem links

        Returns:
            List of unique problem slugs
        """
        with open(md_path, encoding="utf-8") as f:
            content = f.read()

        # Find all LeetCode problem URLs
        raw = re.findall(
            r"https://leetcode\.com/problems/([a-z0-9-]+)/?",
            content,
        )

        # Deduplicate while preserving order
        seen = set()
        unique = []
        for slug in raw:
            if slug not in seen:
                seen.add(slug)
                unique.append(slug)

        logger.info("Extracted %d unique problems from %s", len(unique), md_path)
        return unique

    def add_problems_to_list(
        self,
        list_id: str,
        slugs: List[str],
    ) -> tuple[int, List[str]]:
        """
        Add problems to a LeetCode list.

        Args:
            list_id: Target list ID
            slugs: List of problem slugs

        Returns:
            Tuple of (added_count, failed_slugs)
        """
        total = len(slugs)
        added = 0
        failed = []

        logger.info("Adding %d problems to list %s", total, list_id)

        for i, slug in enumerate(slugs, 1):
            logger.info("[%d/%d] %s", i, total, slug)

            # Resolve slug to question ID
            qid = self.api_client.get_question_id(slug)
            time.sleep(self.rate_limit_delay)

            if not qid:
                logger.error("  ✗ Could not resolve question ID")
                failed.append(slug)
                continue

            # Add to favorite list
            ok = self.api_client.add_to_favorite(list_id, qid)
            time.sleep(self.rate_limit_delay)

            if ok:
                logger.info("  ✓ Added (id=%s)", qid)
                added += 1
            else:
                logger.error("  ✗ Failed to add")
                failed.append(slug)

        logger.info("Completed. Added: %d / %d", added, total)
        if failed:
            logger.warning(
                "Failed (%d):\n%s",
                len(failed),
                "\n".join(f"  - {s}" for s in failed),
            )

        return added, failed

    def add_from_markdown(
        self,
        list_id: str,
        md_path: str,
    ) -> tuple[int, List[str]]:
        """
        Extract problems from markdown and add to list in one call.

        Args:
            list_id: Target list ID
            md_path: Path to markdown file

        Returns:
            Tuple of (added_count, failed_slugs)
        """
        slugs = self.extract_slugs_from_markdown(md_path)
        return self.add_problems_to_list(list_id, slugs)
