# LeetCode List Manager

Automated tool to add LeetCode problems to private lists via the GraphQL API. Extract problem links from markdown files and bulk-add them to your LeetCode collection.

## Features

- 🎯 Extract problem links from markdown files
- 🚀 Bulk add problems to LeetCode private lists
- 🔐 Secure authentication via session cookies
- ⏱️ Configurable rate limiting
- 📊 Detailed logging and progress tracking
- 🛠️ Clean, extensible API

## Installation

### From PyPI (when published)

```bash
pip install leetcode-list-manager
```

### From source

```bash
git clone https://github.com/yourusername/leetcode-list-manager.git
cd leetcode-list-manager
pip install -e .
```

### For development

```bash
pip install -e ".[dev]"
```

## Quick Start

### 1. Get Your LeetCode Credentials

You'll need two pieces of information from your LeetCode account:

- **LEETCODE_SESSION**: Your session cookie
- **CSRF_TOKEN**: Your CSRF token for API requests

To find these:

1. Open LeetCode in your browser
2. Open Developer Tools (F12)
3. Go to **Application** → **Cookies** → https://leetcode.com
4. Find `LEETCODE_SESSION` and `csrftoken` values

### 2. Prepare Your Markdown File

Create a markdown file with LeetCode problem links:

```markdown
## Two Pointers
- [Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
- [3Sum](https://leetcode.com/problems/3sum/)

## Binary Search
- [Binary Search](https://leetcode.com/problems/binary-search/)
```

### 3. Get Your List ID

Visit your LeetCode private list URL:
```
https://leetcode.com/problem-list/XXXX/
                                   ^^^^
                              This is your list ID
```

### 4. Run the Tool

#### Command Line

```bash
leetcode-add-to-list problems.md \
  --list-id wee9za65 \
  --session-id "your_session_id" \
  --csrf-token "your_csrf_token"
```

#### Python API

```python
from leetcode_list_manager import LeetCodeAPIClient, ListManager

# Create API client
client = LeetCodeAPIClient(
    session_id="your_session_id",
    csrf_token="your_csrf_token",
)

# Create manager
manager = ListManager(client, rate_limit_delay=1.0)

# Add problems to list
added, failed = manager.add_from_markdown(
    list_id="wee9za65",
    md_path="problems.md",
)

print(f"Added: {added}, Failed: {len(failed)}")
```

## Command Line Options

```bash
usage: leetcode-add-to-list [-h] [--list-id LIST_ID] [--session-id SESSION_ID]
                            [--csrf-token CSRF_TOKEN] [--rate-limit RATE_LIMIT]
                            [-v]
                            markdown_file

positional arguments:
  markdown_file         Path to markdown file with problem links

optional arguments:
  -h, --help            show this help message and exit
  --list-id LIST_ID     Target LeetCode list ID (default: None)
  --session-id SESSION_ID
                        LEETCODE_SESSION cookie value (default: None)
  --csrf-token CSRF_TOKEN
                        CSRF token for API requests (default: None)
  --rate-limit RATE_LIMIT
                        Delay between API calls in seconds (default: 1.0)
  -v, --verbose         Enable verbose logging
```

## API Reference

### LeetCodeAPIClient

GraphQL client for LeetCode API.

```python
from leetcode_list_manager import LeetCodeAPIClient

client = LeetCodeAPIClient(session_id="...", csrf_token="...")

# Get question ID from slug
qid = client.get_question_id("two-sum")

# Add to favorite list
success = client.add_to_favorite("list_id", "question_id")
```

### ListManager

High-level interface for managing problem lists.

```python
from leetcode_list_manager import ListManager

manager = ListManager(api_client, rate_limit_delay=1.0)

# Extract from markdown and add to list
added, failed = manager.add_from_markdown("list_id", "problems.md")

# Or extract and add separately
slugs = manager.extract_slugs_from_markdown("problems.md")
added, failed = manager.add_problems_to_list("list_id", slugs)
```

## Performance

- **Rate limiting**: 1 second delay between API calls (configurable)
- **121 problems**: ~6 minutes with default rate limiting
- **Success rate**: 100% with valid credentials

## Error Handling

The tool logs all operations and failures. Common issues:

- **Invalid credentials**: Check your SESSION_ID and CSRF_TOKEN
- **Invalid list ID**: Verify the list ID from your URL
- **Network errors**: Check your internet connection
- **Invalid markdown format**: Ensure links follow `https://leetcode.com/problems/SLUG/` format

## Requirements

- Python 3.9+
- requests >= 2.31.0

## Development

### Setup

```bash
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
pytest --cov  # with coverage
```

### Code formatting

```bash
black leetcode_list_manager/
ruff check --fix leetcode_list_manager/
```

### Type checking

```bash
mypy leetcode_list_manager/
```

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool uses LeetCode's unofficial GraphQL API. Use at your own discretion. LeetCode's Terms of Service apply.

## Changelog

### v1.0.0 (2024-01-01)

- Initial release
- Extract problems from markdown
- Add to private lists via GraphQL
- CLI and Python API

## Support

For issues or questions, please open an issue on GitHub.
