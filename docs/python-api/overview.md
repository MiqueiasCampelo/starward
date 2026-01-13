---
id: overview
title: Python API Overview
sidebar_label: Overview
sidebar_position: 1
description: Use starward as a Python library for astronomical calculations including time, coordinates, sun, moon, and planets.
---

# Python API Overview

starward can be used as a Python library for astronomical calculations.

## Installation

```bash
pip install starward
```

## Quick Example

```python
from starward import (
    JulianDate, jd_now,
    ICRSCoord, Angle,
    Planet, planet_position,
)

# Current Julian Date
now = jd_now()
print(f"JD: {now.jd}")

# Parse coordinates
vega = ICRSCoord.parse("18h36m56s +38d47m01s")
print(f"Vega: RA={vega.ra.hours:.2f}h, Dec={vega.dec.degrees:.2f}°")

# Planetary position
mars = planet_position(Planet.MARS)
print(f"Mars magnitude: {mars.magnitude:+.1f}")
```

## Main Exports

The top-level `starward` module exports commonly used classes:

```python
from starward import (
    # Time
    JulianDate,
    jd_now,
    utc_to_jd,
    jd_to_utc,

    # Angles
    Angle,
    angular_separation,
    position_angle,

    # Coordinates
    ICRSCoord,
    GalacticCoord,
    HorizontalCoord,

    # Planets
    Planet,
    PlanetPosition,
    planet_position,
    all_planet_positions,

    # Constants
    CONSTANTS,

    # Precision
    get_precision,
    set_precision,
)
```

## Core Modules

For more specialized functions, import from `starward.core`:

```python
from starward.core.sun import sun_position, sunrise, sunset
from starward.core.moon import moon_position, moon_phase
from starward.core.planets import planet_rise, planet_set
from starward.core.observer import Observer
from starward.core.visibility import compute_visibility
```

## Verbose Mode

Enable step-by-step calculation output:

```python
from starward.verbose import VerboseContext
from starward.core.sun import sun_position

# Create verbose context
vctx = VerboseContext()

# Run calculation with verbose output
sun = sun_position(verbose=vctx)

# Print the steps
print(vctx.format_steps())
```

## Detailed Reference

- [Core Modules](/docs/python-api/modules) — Detailed module documentation
