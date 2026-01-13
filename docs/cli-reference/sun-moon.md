---
id: sun-moon
title: Sun & Moon Commands
sidebar_label: Sun & Moon
sidebar_position: 5
---

# Sun & Moon Commands

Solar and lunar position calculations.

## Sun Commands

### `starward sun position`

Current solar position.

```bash
starward sun position
starward sun position --jd 2451545.0  # At J2000.0
```

### `starward sun rise` / `starward sun set`

Sunrise and sunset times.

```bash
starward sun rise --lat 40.7 --lon -74.0
starward sun set --observer home
```

### `starward sun twilight`

Twilight times (civil, nautical, astronomical).

```bash
starward sun twilight --lat 51.5 --lon -0.1
```

### `starward sun altitude`

Current solar altitude.

```bash
starward sun altitude --lat 40.7 --lon -74.0
```

## Moon Commands

### `starward moon position`

Current lunar position.

```bash
starward moon position
```

### `starward moon phase`

Current lunar phase.

```bash
starward moon phase
```

Output includes phase name, illumination percentage, and age in days.

### `starward moon rise` / `starward moon set`

Moonrise and moonset times.

```bash
starward moon rise --lat 40.7 --lon -74.0
```

### `starward moon next`

Find the next occurrence of a phase.

```bash
starward moon next full
starward moon next new
```

## Examples

```bash
# Solar noon at Greenwich
starward sun noon --lat 51.4769 --lon -0.0005

# Day length in summer vs winter
starward sun rise --lat 60 --lon 0 --jd 2460479.5  # June
starward sun rise --lat 60 --lon 0 --jd 2460296.5  # December

# Moon phase with verbose calculation
starward moon phase --verbose

# JSON output for scripting
starward sun position --json | jq '.ra_hours'
```

## Python API

```python
from starward.core.sun import sun_position, sunrise, sunset
from starward.core.moon import moon_position, moon_phase
from starward.core.observer import Observer

# Sun position
sun = sun_position()
print(f"Sun RA: {sun.ra.format_hms()}")
print(f"Equation of time: {sun.equation_of_time:.1f} min")

# Sunrise at a location
observer = Observer.from_degrees("NYC", 40.7, -74.0)
rise = sunrise(observer)
print(f"Sunrise: {rise.to_datetime()}")

# Moon phase
phase = moon_phase()
print(f"Phase: {phase.phase_name.value}")
print(f"Illumination: {phase.percent_illuminated:.1f}%")
```
