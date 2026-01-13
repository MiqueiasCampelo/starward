---
slug: steady-tracking
title: "astr0 v0.2.0: Steady Tracking"
authors: [oddur]
tags: [release]
---

Version 0.2.0 "Steady Tracking" brings the Sun and Moon into astr0, along with comprehensive observation planning tools. This release transforms astr0 from a coordinate toolkit into a complete observation planning assistant.

<!-- truncate -->

## New Modules

### Sun Module

Calculate everything you need to know about our nearest star:

- **Position**: Right ascension, declination, altitude, azimuth
- **Rise/Set Times**: Accurate to the minute for any location
- **Twilight**: Civil, nautical, and astronomical twilight times
- **Equation of Time**: The difference between solar and clock time

```bash
astr0 sun position --observer "New York"
astr0 sun rise --observer "Tokyo"
astr0 sun twilight --type astronomical
```

### Moon Module

Track Earth's companion through its phases:

- **Phase**: Current phase name and illumination percentage
- **Position**: Where to find the Moon in the sky
- **Rise/Set**: When the Moon appears and disappears
- **Next Phase**: When to expect the next full or new moon

```bash
astr0 moon phase --verbose
astr0 moon rise --observer "London"
```

### Observer Module

Save and manage your observing locations:

```bash
astr0 observer add "Home" --lat 40.7128 --lon -74.0060 --tz "America/New_York"
astr0 observer list
astr0 observer use "Home"
```

Locations are stored in a simple TOML file and persist between sessions.

### Visibility Module

Plan your observations with precision:

- **Airmass**: Calculate atmospheric extinction at any altitude
- **Transit Time**: When objects cross the meridian
- **Rise/Set**: General rise/set calculations for any celestial object
- **Moon Separation**: Avoid lunar interference

```bash
astr0 visibility airmass --alt 45
astr0 visibility transit "Vega" --observer "Home"
```

## LaTeX Output

For academic use, astr0 now supports LaTeX-formatted output:

```bash
astr0 sun position --format latex
```

## Quality Milestone

This release includes over 500 tests validated against authoritative sources:

- US Naval Observatory calculations
- JPL Horizons ephemeris data
- IAU SOFA library results
- Jean Meeus's *Astronomical Algorithms*

## Getting Started

```bash
pip install astr0
```

## What's Next

v0.3.0 will extend astr0 to the planets — Mercury through Neptune. Position calculations, magnitude, elongation, and opposition timing are all on the roadmap.
