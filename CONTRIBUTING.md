# Contributing to LeetCode List Manager

First off, thanks for considering contributing! It's people like you that make this tool so great.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and expected behavior**

### Pull Requests

- Fill in the required template
- Follow the Python styleguides
- Include appropriate test cases
- End all files with a newline

## Development Setup

1. Fork the repo and clone your fork
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dev dependencies: `pip install -e ".[dev]"`

## Styleguides

### Python Styleguide

- Use [Black](https://github.com/psf/black) for code formatting
- Use [Ruff](https://github.com/charliermarsh/ruff) for linting
- Use [MyPy](https://github.com/python/mypy) for type checking
- Follow [PEP 257](https://www.python.org/dev/peps/pep-0257/) for docstrings

### Format your code

```bash
black leetcode_list_manager tests
ruff check --fix leetcode_list_manager tests
mypy leetcode_list_manager
```

### Run tests

```bash
pytest
pytest --cov  # with coverage
```

## Additional Notes

- Be respectful and constructive in all interactions
- Help others if you can
- Report security issues to maintainers privately

Thank you for contributing!
