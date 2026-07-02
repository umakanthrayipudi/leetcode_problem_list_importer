"""Command-line interface for LeetCode list manager."""
import argparse
import logging
import sys
from typing import Optional

from .api import LeetCodeAPIClient
from .manager import ListManager


def setup_logging(verbose: bool = False) -> None:
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s %(message)s",
    )


def main(argv: Optional[list[str]] = None) -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="leetcode-add-to-list",
        description="Add LeetCode problems to private lists",
    )
    parser.add_argument(
        "markdown_file",
        help="Path to markdown file with problem links",
    )
    parser.add_argument(
        "--list-id",
        required=True,
        help="Target LeetCode list ID",
    )
    parser.add_argument(
        "--session-id",
        required=True,
        help="LEETCODE_SESSION cookie value",
    )
    parser.add_argument(
        "--csrf-token",
        required=True,
        help="CSRF token for API requests",
    )
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=1.0,
        help="Delay between API calls (seconds)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args(argv)
    setup_logging(args.verbose)

    try:
        # Initialize API client
        api_client = LeetCodeAPIClient(
            session_id=args.session_id,
            csrf_token=args.csrf_token,
        )

        # Initialize manager
        manager = ListManager(
            api_client=api_client,
            rate_limit_delay=args.rate_limit,
        )

        # Add problems
        added, failed = manager.add_from_markdown(
            list_id=args.list_id,
            md_path=args.markdown_file,
        )

        # Exit with appropriate code
        return 1 if failed else 0

    except FileNotFoundError as e:
        logging.error("File not found: %s", e)
        return 1
    except Exception as e:
        logging.error("Error: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
