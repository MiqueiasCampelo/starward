---
id: installation
title: Installation
sidebar_label: Installation
sidebar_position: 1
description: Install starward astronomy toolkit via pip or from source. Requires Python 3.9+.
---

# Installation

## Requirements

- Python 3.9 or higher
- No compiled dependencies (pure Python)

## Install from PyPI

```bash
pip install starward
```

## Install from Source

```bash
git clone https://github.com/oddurs/starward.git
cd starward
pip install -e .
```

## Development Install

For development with all test dependencies:

```bash
pip install -e ".[dev]"
```

## Verify Installation

```bash
starward --version
# starward, version 0.2.1

starward time now
```

## Dependencies

starward has minimal dependencies:

| Package | Purpose |
|---------|---------|
| click | CLI framework |
| rich | Terminal formatting |

Development dependencies include pytest, hypothesis, mypy, and ruff.
