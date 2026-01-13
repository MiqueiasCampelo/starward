---
id: quickstart
title: Quick Start
sidebar_label: Quick Start
sidebar_position: 2
---

# Quick Start

Get up and running with starward in minutes.

## Current Time

```bash
# Show current time in multiple formats
starward time now
```

Output:
```text
  Time Systems
  ─────────────────────────────────────────
  UTC:        2026-01-11 08:30:00
  JD:         2461051.854167
  MJD:        61051.354167
  Unix:       1768133400
```

## Planetary Positions

```bash
# All planets at once
starward planets all

# Specific planet
starward planets position mars
```

## Sun and Moon

```bash
# Solar position
starward sun position

# Sunrise/sunset (requires location)
starward sun rise --lat 40.7 --lon -74.0

# Moon phase
starward moon phase
```

## Coordinate Transformations

```bash
# Parse and transform coordinates
starward coords transform "12h30m +45d" --to galactic

# Angular separation between objects
starward angles sep "10h30m +20d" "11h00m +22d"
```

## Verbose Mode

Add `--verbose` or `-v` to see the math:

```bash
starward sun position --verbose
```

This shows step-by-step calculations with formulas and intermediate values.

## JSON Output

For scripting and integration:

```bash
starward planets position jupiter --json
```

## Setting Up an Observer

For rise/set calculations, save your location:

```bash
# Add a named observer
starward observer add "Home" 40.7128 -74.0060

# Set as default
starward observer default "Home"

# Now rise/set commands use your location automatically
starward sun rise
starward planets rise mars
```

## Python Library

```python
from starward import planet_position, Planet, jd_now

# Get Mars position
mars = planet_position(Planet.MARS)

print(f"Mars RA: {mars.ra.format_hms()}")
print(f"Mars Dec: {mars.dec.format_dms()}")
print(f"Distance: {mars.distance_au:.3f} AU")
print(f"Magnitude: {mars.magnitude:+.1f}")
```

## Next Steps

- [CLI Overview](/docs/cli-reference/overview) — Full command reference
- [Python API](/docs/python-api/overview) — Library documentation
- [Verbose Mode](/docs/guides/verbose) — Understanding the calculations
