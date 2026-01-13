---
id: overview
title: Python API Overview
sidebar_label: Overview
sidebar_position: 1
description: Use starward as a Python library for astronomical calculations, deep-sky catalogs, star catalogs, and observation planning.
---

# Python API Overview

starward can be used as a Python library for astronomical calculations, deep-sky object lookups, and observation planning.

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

## Catalog Example

```python
from starward.core.messier import MESSIER, messier_coords
from starward.core.ngc import NGC, ngc_coords
from starward.core.hipparcos import Hipparcos, star_coords

# Messier catalog
m31 = MESSIER.get(31)
print(f"{m31.name}: {m31.object_type} in {m31.constellation}")

# NGC catalog
ngc7000 = NGC.get(7000)
print(f"{ngc7000.name}: mag {ngc7000.magnitude}")

# Hipparcos stars
sirius = Hipparcos.get(32349)
print(f"{sirius.name}: {sirius.spectral_type}, mag {sirius.magnitude}")

# Get coordinates
coords = messier_coords(31)
print(f"M31: RA={coords.ra.hours:.2f}h, Dec={coords.dec.degrees:.2f}°")
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

### Calculations

```python
from starward.core.sun import sun_position, sunrise, sunset
from starward.core.moon import moon_position, moon_phase
from starward.core.planets import planet_rise, planet_set
from starward.core.observer import Observer
from starward.core.visibility import compute_visibility
```

### Deep-Sky Catalogs

```python
from starward.core.messier import MESSIER, messier_coords, messier_altitude
from starward.core.ngc import NGC, ngc_coords, ngc_altitude
from starward.core.ic import IC, ic_coords, ic_altitude
from starward.core.caldwell import Caldwell, caldwell_coords, caldwell_altitude
```

### Star Catalog

```python
from starward.core.hipparcos import Hipparcos, star_coords, star_altitude
```

### Cross-Catalog Search

```python
from starward.core.finder import (
    find_by_name,
    find_galaxies,
    find_nebulae,
    find_in_constellation,
)
```

### Observation Lists

```python
from starward.core.lists import (
    create_list,
    add_to_list,
    get_list,
    export_list,
)
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
- [Catalog Modules](/docs/module-guides/catalogs) — Deep-sky and star catalogs
- [Finder Module](/docs/module-guides/finder) — Cross-catalog search
- [Lists Module](/docs/module-guides/lists) — Observation list management
