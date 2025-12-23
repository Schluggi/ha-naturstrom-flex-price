# Copilot Instructions for Naturstrom Project

This repository follows specific guidelines to ensure consistency, quality, and automation. GitHub Copilot should adhere to these instructions when generating code, suggestions, or documentation.

## General Guidelines
- **Programming Language**: Use Python for all code contributions.
- **Testing**: Always include unit tests for new features or changes. Use pytest as the testing framework.
- **Dependency Management**: Use `pip-compile` to manage and lock dependencies in `requirements.txt` and `requirements-dev.txt`. Ensure `requirements.in` files are updated before compiling.

## Versioning and Releases
- **Semantic Versioning**: Enforce semantic versioning (e.g., MAJOR.MINOR.PATCH) for all releases. Increment versions appropriately based on changes (breaking changes for MAJOR, new features for MINOR, bug fixes for PATCH).
- **Automatic Tagging**: After changes are pushed to the `main` branch, automatically tag the commit with the new semantic version. Update the version in `custom_components/naturstrom_flex/manifest.json` before pushing to trigger the tagging workflow.

## Documentation
- **Keep Documentation Up-to-Date**: Update README.md, docstrings, and any API documentation whenever code changes are made. Ensure inline comments and external docs reflect the latest functionality.

## Code Style and Best Practices
- Follow PEP 8 for Python code style.
- Use type hints where possible.
- Avoid introducing breaking changes without justification.

If a suggestion violates these guidelines, Copilot should refrain from proposing it and instead suggest compliant alternatives.