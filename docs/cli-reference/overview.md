---
id: overview
title: CLI Overview
sidebar_label: Overview
sidebar_position: 1
description: Command-line interface for astronomical calculations. Time conversions, coordinates, sun/moon positions, and planetary ephemeris.
---

# CLI Overview

starward provides a comprehensive command-line interface for astronomical calculations.

## Global Options

| Option | Description |
|--------|-------------|
| `--verbose`, `-v` | Show calculation steps |
| `--json` | Output in JSON format |
| `--output`, `-o` | Output format: `plain`, `json`, `latex` |
| `--precision`, `-p` | Precision level (see below) |
| `--version` | Show version |
| `--help` | Show help |

## Precision Levels

| Level | Decimals | Use Case |
|-------|----------|----------|
| `compact` | 2 | Quick reference |
| `display` | 4 | Readable output |
| `standard` | 6 | Default |
| `high` | 10 | Research |
| `full` | 15 | Maximum precision |

```bash
starward --precision high sun position
```

## Command Groups

| Group | Alias | Description |
|-------|-------|-------------|
| `time` | `t` | Time conversions |
| `coords` | `c` | Coordinate transformations |
| `angles` | `a` | Angular calculations |
| `sun` | `s` | Solar position and events |
| `moon` | `m` | Lunar position and phases |
| `planets` | `p` | Planetary positions |
| `observer` | `o` | Observer management |
| `vis` | `v` | Visibility calculations |
| `constants` | `const` | Astronomical constants |

## Examples

```bash
# Using aliases
starward t now          # time now
starward p all          # planets all
starward s rise         # sun rise

# Combining options
starward -v --json planets position mars

# Pipeline to jq
starward planets all --json | jq '.planets.jupiter'
```

## Detailed References

- [Time Commands](/docs/cli-reference/time)
- [Coordinate Commands](/docs/cli-reference/coords)
- [Sun & Moon](/docs/cli-reference/sun-moon)
- [Planets](/docs/cli-reference/planets)
