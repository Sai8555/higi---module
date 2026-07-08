# Contributing to higi

Thank you for your interest in contributing to `higi`! Contributions are what make the open-source community an amazing place to learn, inspire, and create.

This document provides guidelines for contributing to `higi`.

## How Can I Contribute?

### Reporting Bugs
If you find a bug, please open a Github Issue. Use the bug report template if available, or describe:
- The expected behavior and the actual behavior.
- Clear steps to reproduce the issue.
- The Python version and environment details.

### Suggesting Enhancements
If you have ideas for new features or resilience behaviors:
- Open a Feature Request issue or start a Discussion on GitHub.
- Outline the use-case and why this enhancement is valuable for Python developers.

### Pull Requests
We welcome pull requests to improve the self-healing and validation engine.
1. Fork the repository and create your branch from `main` (e.g., `feature/amazing-enhancement`).
2. Make your changes, keeping the code clean, well-documented, and compliant with PEP 8.
3. Add unit tests for any new logic in the `tests/` directory.
4. Ensure all tests pass.
5. Submit your PR with a clear description of the changes.

## Development Setup

`higi` uses `hatchling` for building and package management. To set up your local development environment:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sai8555/higi---module.git
   cd higi---module
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the package in editable mode with development dependencies:**
   ```bash
   pip install -e .
   ```

4. **Running Tests:**
   We use `pytest` for unit testing. Run the test suite using:
   ```bash
   PYTHONPATH=. pytest tests/
   ```

## Code Style & Standards

- **Formatting**: We follow standard PEP 8. Please run a formatter like `black` or `ruff` before committing.
- **Type Annotations**: Use type hints for all new functions and public APIs where appropriate.
- **Comments**: Keep comments clear and update documentation if any API changes.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).
