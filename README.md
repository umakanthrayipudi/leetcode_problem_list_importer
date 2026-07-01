# LeetCode List Manager

Bulk add LeetCode problems to private lists using a markdown file.

## Installation

Clone and install:
```bash
git clone https://github.com/umakanthrayipudi/leetcode_problem_list_importer.git
cd leetcode_problem_list_importer
pip install -e .
```

Or install with dev tools:
```bash
pip install -e ".[dev]"
```

## Requirements

- Python 3.9+
- requests >= 2.31.0

## Setup

### 1. Get LeetCode Credentials

Open [LeetCode](https://leetcode.com) → Developer Tools (F12) → **Application** → **Cookies**

Copy these values:
- `LEETCODE_SESSION`
- `csrftoken`

### 2. Create Markdown File

Create `problems.md`:

```markdown
## Two Pointers
- [Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
- [3Sum](https://leetcode.com/problems/3sum/)

## Binary Search
- [Binary Search](https://leetcode.com/problems/binary-search/)
```

### 3. Get List ID

Visit your LeetCode private list: `https://leetcode.com/problem-list/XXXX/`

The `XXXX` is your list ID.

## Usage

### Command Line

```bash
leetcode-add-to-list problems.md \
  --list-id wee9za65 \
  --session-id "YOUR_SESSION_ID" \
  --csrf-token "YOUR_CSRF_TOKEN"
```

### Python Code

```python
from leetcode_list_manager import LeetCodeAPIClient, ListManager

client = LeetCodeAPIClient(
    session_id="YOUR_SESSION_ID",
    csrf_token="YOUR_CSRF_TOKEN",
)
manager = ListManager(client)

added, failed = manager.add_from_markdown("wee9za65", "problems.md")
print(f"Added: {added}, Failed: {len(failed)}")
```

## Options

```bash
leetcode-add-to-list --help
```

- `--rate-limit` - Delay between API calls (default: 1.0 second)
- `-v, --verbose` - Enable debug logging

## Performance

- ~3 seconds per problem (with 1s rate limiting)
- 121 problems = ~6 minutes

## License

MIT - See [LICENSE](LICENSE)
