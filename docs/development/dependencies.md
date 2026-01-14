---
sidebar_position: 4
title: Dependencies
description: Runtime and development dependencies for starward
---

# Dependencies

starward is designed with minimal dependencies to remain lightweight and easy to install. All astronomical calculations are implemented from first principles without external astronomy libraries.

## Runtime Dependencies

These packages are required to run starward:

| Package | Version | Purpose |
|---------|---------|---------|
| **Python** | ≥3.9 | Runtime environment |
| **click** | ≥8.0 | CLI framework |
| **rich** | ≥13.0 | Terminal formatting and tables |

### Why These Dependencies?

#### click

[Click](https://click.palletsprojects.com/) provides a clean, composable CLI framework:

- Automatic help generation
- Type conversion and validation
- Nested command groups
- Shell completion support

```python
@click.command()
@click.option('--date', type=click.DateTime(), help='Target date')
def sun(date):
    """Calculate sun position."""
    pass
```

#### rich

[Rich](https://rich.readthedocs.io/) enables beautiful terminal output:

- Tables with Unicode box-drawing
- Syntax highlighting
- Progress bars
- Markdown rendering

```python
from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="Sun Position")
table.add_column("Property", style="cyan")
table.add_column("Value", style="green")
table.add_row("RA", "18h 45m 23s")
console.print(table)
```

## Development Dependencies

Install with: `pip install -e ".[dev]"`

| Package | Version | Purpose |
|---------|---------|---------|
| **pytest** | ≥7.0 | Test framework |
| **pytest-cov** | ≥4.0 | Coverage reporting |
| **hypothesis** | ≥6.0 | Property-based testing |
| **mypy** | ≥1.0 | Static type checking |
| **ruff** | ≥0.1 | Linting and formatting |
| **allure-pytest** | ≥2.13.0 | Test reporting |

### Testing Stack

#### pytest

The de facto standard Python test framework:

```python
def test_julian_date():
    jd = JulianDate(2451545.0)
    assert jd.jd == 2451545.0
```

#### pytest-cov

Integrates coverage.py with pytest:

```bash
pytest --cov=starward --cov-report=html
```

#### hypothesis

Property-based testing for edge cases:

```python
from hypothesis import given, strategies as st

@given(st.floats(min_value=-90, max_value=90))
def test_latitude_bounds(lat):
    angle = Angle(degrees=lat)
    assert -90 <= angle.degrees <= 90
```

#### allure-pytest

Rich HTML test reports with step-by-step breakdowns:

```python
import allure

@allure.title("Sun position calculation")
def test_sun_position():
    with allure.step("Calculate position"):
        pos = sun_position(jd)
    with allure.step("Verify coordinates"):
        assert pos.ra.degrees > 0
```

### Code Quality

#### mypy

Static type checking catches errors before runtime:

```bash
mypy src/starward/
```

Configuration in `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.9"
strict = true
warn_return_any = true
```

#### ruff

Fast linting and formatting (replaces flake8, isort, black):

```bash
ruff check src/        # Lint
ruff check --fix src/  # Auto-fix
ruff format src/       # Format
```

## Documentation Dependencies

The documentation site uses:

| Package | Purpose |
|---------|---------|
| **Docusaurus** | Static site generator |
| **TypeScript** | Configuration typing |
| **Sass** | Custom styling |
| **KaTeX** | Math rendering |
| **Prism** | Syntax highlighting |

Install documentation dependencies:

```bash
cd website
npm install
```

## Why No Astronomy Dependencies?

starward intentionally avoids external astronomy libraries like Astropy, Skyfield, or PyEphem. This is a deliberate design choice:

1. **Educational Value** — Implementing algorithms from scratch teaches computational astronomy
2. **Transparency** — Every calculation can be traced and understood
3. **Lightweight** — Minimal install size and startup time
4. **Control** — Full control over precision and algorithm choices

### Trade-offs

| Aspect | With Dependencies | Without (starward) |
|--------|-------------------|-------------------|
| Accuracy | Higher (SPICE kernels) | Good (analytical) |
| Install size | Large (~100MB+) | Small (~200KB) |
| Startup time | Slow (data loading) | Fast |
| Learning | Black box | Transparent |
| Maintenance | External updates | Self-contained |

For applications requiring arcsecond precision, consider Astropy or Skyfield. For learning, CLI usage, and moderate precision, starward provides an excellent balance.

## Updating Dependencies

```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade click

# Update all dev dependencies
pip install --upgrade -e ".[dev]"
```

## Security

Dependencies are monitored for vulnerabilities:

```bash
# Check for known vulnerabilities
pip audit
```

Report security issues privately via GitHub.
