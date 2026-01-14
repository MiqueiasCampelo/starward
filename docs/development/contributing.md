---
sidebar_position: 3
title: Contributing
description: How to contribute to starward
---

# Contributing to starward

> *"Per aspera ad astra" — Through hardships to the stars*

Thank you for your interest in making starward better! We welcome contributions from everyone—whether you're fixing a typo, adding a feature, or improving documentation.

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/starward.git
cd starward

# Add upstream remote
git remote add upstream https://github.com/oddurs/starward.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"

# Verify installation
starward --version
pytest --collect-only | tail -5
```

### 3. Create a Feature Branch

```bash
# Sync with upstream
git fetch upstream
git checkout master
git merge upstream/master

# Create feature branch
git checkout -b feature/your-feature-name
```

## Development Workflow

### Code Style

starward follows strict code standards:

- **PEP 8** compliance with 100-character line limit
- **Type annotations** for all public APIs
- **Docstrings** for all modules, classes, and functions
- **ruff** for linting and formatting

```bash
# Run linter
ruff check src/

# Auto-fix issues
ruff check --fix src/

# Type checking
mypy src/starward/
```

### Writing Code

#### Module Structure

```python
"""
Module docstring explaining the astronomical domain.

This module handles [concept]. In astronomy, [concept] is important because...
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from starward.core.angles import Angle


@dataclass
class MyResult:
    """
    Result of calculation.

    Attributes:
        value: The computed value in [units]
        uncertainty: Optional measurement uncertainty
    """
    value: float
    uncertainty: Optional[float] = None


def calculate_something(input: Angle) -> MyResult:
    """
    Calculate something astronomical.

    This implements the [algorithm name] from [reference].

    Args:
        input: Input angle in any supported format

    Returns:
        MyResult with computed value

    Example:
        >>> result = calculate_something(Angle(degrees=45))
        >>> print(f"{result.value:.2f}")
        1.41
    """
    # Implementation with clear comments
    pass
```

#### Astronomical Calculations

When implementing calculations:

1. **Cite your sources** — Reference the algorithm origin (e.g., "Meeus, Astronomical Algorithms, Ch. 25")
2. **Document accuracy** — State the expected precision (e.g., "accurate to 0.01° for dates ±50 years from J2000")
3. **Use established constants** — Import from `starward.core.constants`
4. **Handle edge cases** — Poles, date line, singularities

### Writing Tests

All new code requires tests. See the [Testing Guide](./testing) for details.

```python
import allure
import pytest

from starward.core.your_module import calculate_something
from starward.core.angles import Angle


@allure.story("Your Feature")
class TestYourFeature:
    """
    Tests for your feature.

    Educational context about what this tests and why it matters.
    """

    @allure.title("Basic calculation works")
    def test_basic_calculation(self):
        """Test description."""
        with allure.step("Set up input"):
            input_angle = Angle(degrees=45)

        with allure.step("Perform calculation"):
            result = calculate_something(input_angle)

        with allure.step(f"Verify result = {result.value:.2f}"):
            assert result.value == pytest.approx(1.41, rel=0.01)

    @pytest.mark.golden
    @allure.title("Reference value validation")
    def test_golden_value(self):
        """Validate against known reference."""
        # Test against published astronomical data
        pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=starward

# Run specific tests
pytest tests/core/test_your_module.py -v

# Generate Allure report
make report
```

## Submitting Changes

### Commit Guidelines

Write clear, atomic commits:

```bash
# Good commit messages
git commit -m "add lunar libration calculation"
git commit -m "fix airmass formula for low altitudes"
git commit -m "update sun position test golden values"

# Bad commit messages
git commit -m "fixes"
git commit -m "WIP"
git commit -m "addressed review comments"
```

### Pull Request Process

1. **Ensure all tests pass**
   ```bash
   pytest
   ruff check src/
   mypy src/starward/
   ```

2. **Update documentation** if needed

3. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request** on GitHub with:
   - Clear title describing the change
   - Description of what and why
   - Reference to related issues

### Code Review

- All PRs are reviewed for quality, clarity, and alignment with project goals
- Be open to feedback and ready to revise
- Reviews are constructive and respectful

## Types of Contributions

### Bug Fixes

1. Check existing issues for duplicates
2. Create an issue describing the bug
3. Reference the issue in your PR

### New Features

1. **Discuss first** — Open an issue for major features
2. **Start small** — Break large features into incremental PRs
3. **Document thoroughly** — Include docstrings and user docs

### Documentation

Documentation improvements are always welcome:

- Fix typos and clarify explanations
- Add examples and use cases
- Improve API documentation
- Translate to other languages

### Educational Content

starward is an educational project. Consider adding:

- Explanatory comments in code
- Background on astronomical concepts
- Historical context and references
- Worked examples

## Project Structure

Understanding where things go:

| Directory | Purpose |
|-----------|---------|
| `src/starward/core/` | Core astronomical calculations |
| `src/starward/cli/` | Click CLI commands |
| `src/starward/output/` | Rich formatters and display |
| `tests/core/` | Unit tests for core modules |
| `tests/cli/` | CLI integration tests |
| `tests/integration/` | End-to-end workflow tests |
| `docs/` | Docusaurus documentation |
| `website/` | Documentation website config |

## Getting Help

- **Questions?** Open a GitHub issue
- **Stuck?** Check existing issues and discussions
- **Ideas?** Share them in an issue first

## Recognition

Contributors are recognized in:

- Git commit history
- Release notes
- The [maintainers page](./maintainers)

---

*Thank you for helping make starward shine brighter!*
