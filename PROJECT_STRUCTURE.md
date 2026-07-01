# Project Structure

```
leetcode-list-manager/
├── .github/
│   └── workflows/
│       └── tests.yml              # GitHub Actions CI/CD pipeline
├── leetcode_list_manager/         # Main package
│   ├── __init__.py                # Package initialization
│   ├── api.py                     # LeetCode GraphQL API client
│   ├── manager.py                 # Problem list manager
│   └── cli.py                     # Command-line interface
├── tests/                         # Test suite
│   ├── __init__.py
│   └── test_manager.py            # Manager tests
├── .gitignore                     # Git ignore rules
├── CONTRIBUTING.md                # Contribution guidelines
├── LICENSE                        # MIT License
├── MANIFEST.in                    # Package manifest
├── README.md                      # Project documentation
├── example_problems.md            # Example markdown file
├── pyproject.toml                 # Project configuration (PEP 518)
├── requirements.txt               # Production dependencies
├── requirements-dev.txt           # Development dependencies
└── setup.py                       # Setup script (backward compatibility)
```

## Key Files

### Core Package (`leetcode_list_manager/`)

- **`__init__.py`**: Exports public API (LeetCodeAPIClient, ListManager)
- **`api.py`**: GraphQL client with methods for:
  - `get_question_id(slug)` - Resolve problem slug to numeric ID
  - `add_to_favorite(list_id, question_id)` - Add problem to list
- **`manager.py`**: High-level interface with methods for:
  - `extract_slugs_from_markdown(md_path)` - Parse markdown
  - `add_problems_to_list(list_id, slugs)` - Bulk add problems
  - `add_from_markdown(list_id, md_path)` - Combined operation
- **`cli.py`**: Command-line entry point with argparse

### Configuration Files

- **`pyproject.toml`**: Modern Python packaging config
  - Package metadata
  - Dependencies
  - Build backend configuration
  - Tool settings (black, ruff, mypy)
- **`requirements.txt`**: Production dependencies only
- **`requirements-dev.txt`**: Development tools (pytest, black, ruff, mypy)
- **`setup.py`**: Backward compatible setup file

### Documentation

- **`README.md`**: User guide with examples
- **`CONTRIBUTING.md`**: Developer guidelines
- **`example_problems.md`**: Example markdown input

### CI/CD

- **`.github/workflows/tests.yml`**: GitHub Actions pipeline
  - Tests Python 3.9, 3.10, 3.11, 3.12
  - Runs linting, formatting, type checks
  - Executes tests with coverage

## Installation Options

### Development (editable install)
```bash
pip install -e .
```

### With dev tools
```bash
pip install -e ".[dev]"
```

### From requirements
```bash
pip install -r requirements-dev.txt
```

## Publishing to PyPI

1. **Build**: `python -m build`
2. **Check**: `twine check dist/*`
3. **Upload**: `twine upload dist/*`

## Package Contents

- **Main module**: `leetcode_list_manager`
- **CLI entry point**: `leetcode-add-to-list` command
- **Exported classes**: 
  - `LeetCodeAPIClient` - Low-level API access
  - `ListManager` - High-level problem management
