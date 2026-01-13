---
id: overview
title: CLI Overview
sidebar_label: Overview
sidebar_position: 1
description: Command-line interface for astronomical calculations, deep-sky catalogs, star catalogs, and observation planning.
---

# CLI Overview

starward provides a comprehensive command-line interface for astronomical calculations, deep-sky object browsing, and observation planning.

## Global Options

| Option | Description |
|--------|-------------|
| `--verbose`, `-v` | Show calculation steps |
| `--json` | Output in JSON format |
| `--output`, `-o` | Output format: `plain`, `json`, `rich`, `latex` |
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

### Core Calculations

| Group | Alias | Description |
|-------|-------|-------------|
| `time` | `t` | Time conversions |
| `coords` | `c` | Coordinate transformations |
| `angles` | `a` | Angular calculations |
| `constants` | `const` | Astronomical constants |

### Solar System

| Group | Alias | Description |
|-------|-------|-------------|
| `sun` | `s` | Solar position and events |
| `moon` | `m` | Lunar position and phases |
| `planets` | `p` | Planetary positions |

### Deep-Sky Catalogs

| Group | Description |
|-------|-------------|
| `messier` | Messier catalog (110 objects) |
| `ngc` | NGC catalog (~7,840 objects) |
| `ic` | IC catalog (~5,386 objects) |
| `caldwell` | Caldwell catalog (109 objects) |

### Star Catalogs

| Group | Description |
|-------|-------------|
| `stars` | Hipparcos bright star catalog |

### Observation Tools

| Group | Description |
|-------|-------------|
| `find` | Cross-catalog object finder |
| `list` | Custom observation lists |
| `observer` | Observer profile management |
| `vis` | Visibility calculations |

## Examples

```bash
# Core calculations
starward t now                    # Current time
starward coords transform "12h +45d" --to galactic

# Solar system
starward sun rise --lat 40.7 --lon -74.0
starward planets position mars

# Deep-sky catalogs
starward messier show 31          # M31 Andromeda Galaxy
starward ngc list --type galaxy --magnitude 10
starward caldwell search sculptor

# Star catalog
starward stars show 32349         # Sirius
starward stars list --constellation Ori

# Cross-catalog search
starward find galaxies --mag 10 --constellation Vir
starward find bright              # Naked-eye objects

# Observation lists
starward list create "Tonight"
starward list add "Tonight" M31 --notes "Check visibility"
starward list show "Tonight"

# Pipeline to jq
starward --json messier show 31 | jq '.coordinates'
```

## Detailed References

### Core & Solar System
- [Time Commands](/docs/cli-reference/time)
- [Coordinate Commands](/docs/cli-reference/coords)
- [Sun & Moon](/docs/cli-reference/sun-moon)
- [Planets](/docs/cli-reference/planets)

### Catalogs & Observation
- [Deep-Sky Catalogs](/docs/cli-reference/deep-sky) — Messier, NGC, IC, Caldwell
- [Star Catalog](/docs/cli-reference/stars) — Hipparcos
- [Object Finder](/docs/cli-reference/finder) — Cross-catalog search
- [Observation Lists](/docs/cli-reference/lists) — Custom lists
