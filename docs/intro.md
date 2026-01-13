---
id: intro
title: starward Documentation
sidebar_label: Home
slug: /
sidebar_position: 1
description: Professional astronomy calculation toolkit for Python with CLI support. Calculate Julian dates, coordinate transformations, sun/moon positions, and planetary ephemeris.
keywords: [astronomy, python, cli, julian date, coordinates, ephemeris]
---

# starward Documentation

> *Per aspera ad astra* — Through hardships to the stars

Welcome to the starward documentation! starward is a professional astronomy calculation toolkit with a focus on transparency and learning.

## Quick Links

| Document | Description |
|----------|-------------|
| [Installation](/docs/getting-started/installation) | How to install starward |
| [Quick Start](/docs/getting-started/quickstart) | Get up and running in minutes |
| [CLI Overview](/docs/cli-reference/overview) | Command-line interface reference |
| [Python API](/docs/python-api/overview) | Using starward as a Python library |
| [Verbose Mode](/docs/guides/verbose) | See the math behind calculations |

## Features

- **Time Systems** — Julian dates, sidereal time, epoch conversions
- **Coordinates** — ICRS, Galactic, Horizontal transformations
- **Sun & Moon** — Position, rise/set times, phases, twilight
- **Planets** — Mercury through Neptune positions and visibility
- **Verbose Mode** — Show your work with step-by-step calculations
- **Multiple Outputs** — Plain text, JSON, and LaTeX formats

## Philosophy

starward is built on these principles:

1. **Precision First** — Every calculation traceable, every assumption explicit
2. **Show Your Work** — Verbose mode reveals the math behind each result
3. **Modular Design** — Each module stands alone, plays well with others
4. **Test Everything** — 500+ tests validated against authoritative sources

## Getting Started

```bash
# Install via pip
pip install starward

# Check current time in all formats
starward time now

# Get planetary positions
starward planets all

# Show the math with verbose mode
starward sun position --verbose
```

## Version

This documentation is for starward **v0.3.0**.
