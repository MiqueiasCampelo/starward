---
sidebar_position: 1
title: Developer Overview
description: Technical overview for starward developers and contributors
---

# Developer Documentation

Welcome to the starward developer documentation. This section provides technical insight into the project's architecture, testing infrastructure, and contribution guidelines.

## Project Philosophy

starward is built on a few core principles:

- **Zero external astronomy dependencies** — All calculations are implemented from first principles
- **Educational value** — Code should teach as well as compute
- **Professional quality** — Production-ready with comprehensive testing
- **CLI-first design** — Beautiful terminal output with rich formatting

## Architecture Overview

```
starward/
├── src/starward/
│   ├── cli/              # Click-based CLI commands
│   ├── core/             # Core astronomical calculations
│   │   ├── angles.py     # Angular measurements and conversions
│   │   ├── coords.py     # Coordinate systems (ICRS, Galactic, Horizontal)
│   │   ├── time.py       # Julian Date and sidereal time
│   │   ├── sun.py        # Solar position and phenomena
│   │   ├── moon.py       # Lunar position and phases
│   │   ├── planets.py    # Planetary ephemerides
│   │   ├── visibility.py # Observability calculations
│   │   └── constants.py  # Astronomical constants
│   └── output/           # Rich console formatters
├── tests/                # Comprehensive test suite (872 tests)
├── docs/                 # Docusaurus documentation
└── website/              # Documentation website
```

## Quick Links

| Topic | Description |
|-------|-------------|
| [Testing](./testing) | Test suite architecture, Allure reporting, markers |
| [Contributing](./contributing) | How to contribute code and documentation |
| [Dependencies](./dependencies) | Runtime and development dependencies |
| [Cheatsheet](./cheatsheet) | Quick reference for common operations |
| [License](./license) | MIT License details |
| [Maintainers](./maintainers) | Project maintainers and history |

## Development Setup

```bash
# Clone the repository
git clone https://github.com/oddurs/starward.git
cd starward

# Install with development dependencies
pip install -e ".[dev]"

# Run the test suite
pytest

# Generate Allure report
make report
```

## Version History

| Version | Codename | Highlights |
|---------|----------|------------|
| v0.4.1 | — | Allure test reporting, educational test comments |
| v0.4.0 | Deep Sky | Messier, NGC, IC, Caldwell, Hipparcos catalogs |
| v0.3.0 | Planets | Planetary positions and visibility |
| v0.2.0 | Celestial | Sun and Moon calculations |
| v0.1.0 | Genesis | Core time and coordinate systems |
