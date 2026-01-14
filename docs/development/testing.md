---
sidebar_position: 2
title: Testing
description: Comprehensive guide to the starward test suite and Allure reporting
---

# Testing Infrastructure

starward maintains a comprehensive test suite with **872 tests** covering all astronomical calculations. The tests serve dual purposes: ensuring correctness and providing educational documentation of astronomical concepts.

## Test Suite Overview

```
tests/
├── conftest.py              # Shared fixtures (observers, coordinates, stars)
├── allure/                  # Allure helpers and step functions
│   ├── helpers.py           # Reusable step decorators
│   └── categories.json      # Test categorization rules
├── core/                    # Core module tests
│   ├── test_angles.py       # Angular measurements (84 tests)
│   ├── test_coords.py       # Coordinate systems (38 tests)
│   ├── test_time.py         # Julian Date, sidereal time (46 tests)
│   ├── test_sun.py          # Solar calculations (28 tests)
│   ├── test_moon.py         # Lunar calculations (26 tests)
│   ├── test_planets.py      # Planetary ephemerides (37 tests)
│   ├── test_visibility.py   # Observability (31 tests)
│   ├── test_constants.py    # Astronomical constants (28 tests)
│   ├── test_messier.py      # Messier catalog (43 tests)
│   ├── test_ngc.py          # NGC catalog (44 tests)
│   ├── test_ic.py           # IC catalog (43 tests)
│   ├── test_caldwell.py     # Caldwell catalog (40 tests)
│   └── test_hipparcos.py    # Hipparcos catalog (50 tests)
├── cli/                     # CLI integration tests
│   └── test_commands.py     # Command-line interface (34 tests)
├── integration/             # End-to-end workflows
│   └── test_workflows.py    # Multi-module integration (8 tests)
└── output/                  # Formatter tests
    └── test_formatters.py   # Rich output formatting (10 tests)
```

## Running Tests

### Basic Commands

```bash
# Run all tests (quiet mode)
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/core/test_sun.py

# Run tests matching a pattern
pytest -k "moon"

# Run with coverage report
pytest --cov=starward --cov-report=html
```

### Using the Makefile

```bash
# Run tests with Allure results
make test

# Generate and open Allure report
make report

# Clean test artifacts
make clean
```

## Test Markers

Tests are organized using pytest markers for selective execution:

| Marker | Description | Example |
|--------|-------------|---------|
| `@pytest.mark.golden` | Reference value tests (high-accuracy validation) | Sun position at J2000.0 |
| `@pytest.mark.slow` | Tests that take longer to execute | Monte Carlo validation |
| `@pytest.mark.edge` | Edge case and boundary tests | Poles, date line |
| `@pytest.mark.skip` | Temporarily skipped (with reason) | Unimplemented features |

```bash
# Run only golden tests
pytest -m golden

# Skip slow tests
pytest -m "not slow"

# Run edge case tests
pytest -m edge
```

## Allure Reporting

The test suite uses [Allure](https://docs.qameta.io/allure/) for rich, interactive test reports.

### Report Structure

Tests are organized into a hierarchy:

- **Epic**: Top-level category (e.g., "Core Calculations")
- **Feature**: Module being tested (e.g., "Sun Module")
- **Story**: Test class grouping (e.g., "Solar Position")
- **Test**: Individual test case with steps

### Allure Decorators

```python
import allure
import pytest

@allure.epic("Core Calculations")
@allure.feature("Sun Module")
@allure.story("Solar Position")
class TestSunPosition:
    """Tests for solar position calculations."""

    @pytest.mark.golden
    @allure.title("Sun position at J2000.0")
    @allure.description("""
    At J2000.0 (Jan 1, 2000 12:00 TT), the Sun should be at:
    - RA: ~281° (in Sagittarius)
    - Dec: ~-23° (near winter solstice)
    """)
    def test_sun_at_j2000(self):
        """Sun position at the J2000.0 epoch."""
        with allure.step("Set reference date: J2000.0"):
            jd = JulianDate(2451545.0)

        with allure.step("Calculate sun position"):
            pos = sun_position(jd)

        with allure.step(f"Verify RA = {pos.ra.degrees:.2f}°"):
            assert 270 < pos.ra.degrees < 290
```

### Generating Reports

```bash
# Run tests (generates allure-results/)
pytest --clean-alluredir

# Serve report locally
allure serve allure-results

# Generate static HTML report
allure generate allure-results -o allure-report
```

### Report Features

The Allure report includes:

- **Test execution timeline** — Visual overview of test runs
- **Step-by-step breakdown** — Each `with allure.step()` shown in detail
- **Attachments** — Screenshots, logs, computed values
- **Categories** — Automatic grouping of failures by type
- **History** — Trends across multiple test runs

## Test Fixtures

Common test fixtures are defined in `conftest.py`:

### Observer Locations

```python
@pytest.fixture
def greenwich():
    """Royal Observatory Greenwich (51.4772°N, 0.0005°W)"""
    return Observer.from_degrees("Greenwich", 51.4772, -0.0005, elevation=62.0)

@pytest.fixture
def mauna_kea():
    """Mauna Kea Observatory (19.82°N, 155.47°W, 4207m)"""
    return Observer.from_degrees("Mauna Kea", 19.82, -155.47, elevation=4207.0)

@pytest.fixture
def paranal():
    """ESO Paranal Observatory (-24.63°S, 70.40°W, 2635m)"""
    return Observer.from_degrees("Paranal", -24.63, -70.40, elevation=2635.0)
```

### Famous Stars

```python
@pytest.fixture
def famous_stars():
    """Dictionary of bright stars with ICRS coordinates."""
    return {
        'sirius': ICRSCoord.parse("06h45m08.9s -16d42m58s"),
        'vega': ICRSCoord.parse("18h36m56.3s +38d47m01s"),
        'polaris': ICRSCoord.parse("02h31m49.1s +89d15m51s"),
        'betelgeuse': ICRSCoord.parse("05h55m10.3s +07d24m25s"),
    }
```

### Reference Times

```python
@pytest.fixture
def j2000():
    """J2000.0 epoch (JD 2451545.0)"""
    return JulianDate(2451545.0)

@pytest.fixture
def vernal_equinox_2024():
    """2024 March Equinox (JD 2460390.3)"""
    return JulianDate(2460390.3)
```

## Writing Tests

### Educational Docstrings

Tests should include educational docstrings explaining the astronomical concepts:

```python
class TestAirmass:
    """
    Tests for airmass calculations.

    Airmass quantifies the amount of atmosphere light must traverse
    to reach an observer. At zenith (directly overhead), airmass = 1.0.
    As objects approach the horizon, airmass increases dramatically:

    - 90° altitude: X = 1.0 (zenith)
    - 45° altitude: X ≈ 1.41 (√2)
    - 30° altitude: X ≈ 2.0 (practical observation limit)
    - 10° altitude: X ≈ 5.8
    -  0° altitude: X → ∞ (horizon)

    The secant formula X = sec(z) = 1/cos(z) works well above 15°.
    Near the horizon, atmospheric refraction requires corrections.
    """
```

### Step Annotations

Use `with allure.step()` for meaningful test steps:

```python
def test_julian_century(self):
    """Julian century = 36525 days (100 Julian years)."""
    with allure.step("Define Julian year = 365.25 days"):
        julian_year = 365.25

    with allure.step("Calculate Julian century"):
        julian_century = 100 * julian_year

    with allure.step(f"Verify: {julian_century} = 36525"):
        assert julian_century == 36525.0
```

### Golden Tests

Mark tests that validate against known reference values:

```python
@pytest.mark.golden
@allure.title("Speed of light = 299,792,458 m/s (exact)")
def test_speed_of_light(self):
    """Speed of light is exact by SI definition since 2019."""
    with allure.step("Verify c = 299,792,458 m/s"):
        assert CONSTANTS.c.value == 299792458.0
```

## Coverage

Current test coverage by module:

| Module | Tests | Coverage |
|--------|-------|----------|
| `core.angles` | 84 | 98% |
| `core.coords` | 38 | 95% |
| `core.time` | 46 | 97% |
| `core.sun` | 28 | 94% |
| `core.moon` | 26 | 92% |
| `core.planets` | 37 | 91% |
| `core.visibility` | 31 | 93% |
| `core.constants` | 28 | 100% |
| `cli` | 34 | 88% |

Generate a detailed coverage report:

```bash
pytest --cov=starward --cov-report=html
open htmlcov/index.html
```
