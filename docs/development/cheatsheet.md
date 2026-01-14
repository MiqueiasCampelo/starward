---
sidebar_position: 5
title: Cheatsheet
description: Quick reference for starward CLI and Python API
---

# Developer Cheatsheet

Quick reference for common starward operations.

## CLI Quick Reference

### Time Commands

```bash
# Current Julian Date
starward time jd

# Convert calendar to JD
starward time jd --date "2024-06-21 12:00"

# Current sidereal time at Greenwich
starward time lst --lon 0

# Current sidereal time at your location
starward time lst --lon -122.4  # San Francisco
```

### Coordinate Commands

```bash
# Parse coordinates
starward coords parse "05h 34m 32s" "+22d 00m 52s"  # Crab Nebula

# Convert between systems
starward coords convert --ra 83.63 --dec 22.01 --to galactic

# Angular separation
starward coords sep --ra1 83.63 --dec1 22.01 --ra2 84.05 --dec2 -1.20
```

### Sun Commands

```bash
# Current sun position
starward sun

# Sun at specific date
starward sun --date "2024-12-21"

# Sunrise/sunset
starward sun rise --lat 51.5 --lon -0.1
starward sun set --lat 51.5 --lon -0.1
```

### Moon Commands

```bash
# Current moon position and phase
starward moon

# Moon phase calendar
starward moon phase

# Next full moon
starward moon next full
```

### Planet Commands

```bash
# All planet positions
starward planets

# Specific planet
starward planets mars

# Planet visibility tonight
starward planets --tonight
```

### Catalog Commands

```bash
# Messier object
starward messier M31
starward messier 31

# NGC object
starward ngc 7000  # North America Nebula

# Search catalogs
starward search "orion"
starward search --type galaxy
```

## Python API Quick Reference

### Time

```python
from starward.core.time import JulianDate, jd_now, jd_from_datetime

# Current JD
jd = jd_now()
print(f"JD: {jd.jd:.6f}")

# From datetime
from datetime import datetime
jd = jd_from_datetime(datetime(2024, 6, 21, 12, 0))

# Direct construction
jd = JulianDate(2451545.0)  # J2000.0

# Arithmetic
tomorrow = JulianDate(jd.jd + 1)

# Conversions
dt = jd.to_datetime()
mjd = jd.mjd
```

### Angles

```python
from starward.core.angles import Angle

# Construction
a = Angle(degrees=45.5)
a = Angle(radians=0.7854)
a = Angle(hours=6.5)
a = Angle(arcminutes=2730)
a = Angle(arcseconds=163800)

# Properties
a.degrees    # 45.5
a.radians    # 0.7941...
a.hours      # 3.0333...
a.dms        # (45, 30, 0.0)
a.hms        # (3, 2, 0.0)

# Formatting
a.to_dms_str()  # "45° 30' 00.0\""
a.to_hms_str()  # "03h 02m 00.0s"

# Parsing
a = Angle.parse("45d 30m 00s")
a = Angle.parse("03h 02m 00s")

# Normalization
a.normalize()      # 0-360°
a.normalize_180()  # -180 to +180°
```

### Coordinates

```python
from starward.core.coords import ICRSCoord, GalacticCoord

# ICRS (equatorial)
coord = ICRSCoord.from_degrees(ra=83.63, dec=22.01)
coord = ICRSCoord.parse("05h 34m 32s", "+22d 00m 52s")

# Access components
coord.ra      # Angle object
coord.dec     # Angle object
coord.ra.degrees   # 83.63
coord.dec.degrees  # 22.01

# Convert to Galactic
galactic = coord.to_galactic()
galactic.l  # Galactic longitude
galactic.b  # Galactic latitude

# Angular separation
from starward.core.angles import angular_separation
sep = angular_separation(ra1, dec1, ra2, dec2)
```

### Observer

```python
from starward.core.observer import Observer

# Create observer
obs = Observer.from_degrees(
    name="Greenwich",
    lat=51.4772,
    lon=-0.0005,
    elevation=62.0,
    timezone="Europe/London"
)

# Properties
obs.lat_deg   # 51.4772
obs.lon_deg   # -0.0005
obs.elevation # 62.0

# Serialization
d = obs.to_dict()
```

### Sun

```python
from starward.core.sun import (
    sun_position, sunrise, sunset, solar_noon,
    solar_altitude, day_length
)

# Position
pos = sun_position(jd)
pos.ra        # Right ascension
pos.dec       # Declination
pos.longitude # Ecliptic longitude
pos.distance_au  # Distance in AU
pos.equation_of_time  # EoT in minutes

# Events (return JulianDate or None)
rise = sunrise(observer, jd)
set_time = sunset(observer, jd)
noon = solar_noon(observer, jd)

# Altitude
alt = solar_altitude(observer, jd)  # Angle

# Day length
length = day_length(observer, jd)  # hours
```

### Moon

```python
from starward.core.moon import (
    moon_position, moon_phase, moonrise, moonset,
    next_phase, MoonPhase
)

# Position
pos = moon_position(jd)
pos.ra           # Right ascension
pos.dec          # Declination
pos.distance_km  # Distance in km
pos.angular_diameter  # Apparent size
pos.parallax     # Horizontal parallax

# Phase
phase = moon_phase(jd)
phase.phase       # MoonPhase enum
phase.illumination  # 0.0 to 1.0
phase.age         # Days since new moon

# Events
rise = moonrise(observer, jd)
set_time = moonset(observer, jd)

# Next phase
next_full = next_phase(jd, MoonPhase.FULL)
```

### Planets

```python
from starward.core.planets import planet_position, Planet

# Position
pos = planet_position(Planet.MARS, jd)
pos.ra
pos.dec
pos.distance_au   # From Earth
pos.elongation    # From Sun
pos.phase_angle
pos.magnitude

# All planets
for planet in Planet:
    pos = planet_position(planet, jd)
    print(f"{planet.name}: {pos.ra.to_hms_str()}")
```

### Visibility

```python
from starward.core.visibility import (
    airmass, target_altitude, target_azimuth,
    transit_time, compute_visibility
)

# Airmass
X = airmass(altitude_angle)  # 1.0 at zenith, inf below horizon

# Target position
alt = target_altitude(coord, observer, jd)
az = target_azimuth(coord, observer, jd)

# Transit time
transit = transit_time(coord, observer, jd)

# Full visibility calculation
vis = compute_visibility(coord, observer, jd)
vis.current_altitude
vis.transit_time
vis.moon_separation
vis.is_observable
```

### Constants

```python
from starward.core.constants import CONSTANTS

# Physical constants
CONSTANTS.c.value        # Speed of light (m/s)
CONSTANTS.G.value        # Gravitational constant
CONSTANTS.AU.value       # Astronomical unit (m)

# Time constants
CONSTANTS.JD_J2000.value     # 2451545.0
CONSTANTS.MJD_OFFSET.value   # 2400000.5
CONSTANTS.JULIAN_YEAR.value  # 365.25 days

# Search
results = CONSTANTS.search("solar")
all_constants = CONSTANTS.list_all()
```

## Testing Quick Reference

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Specific file
pytest tests/core/test_sun.py

# Pattern matching
pytest -k "moon"

# By marker
pytest -m golden
pytest -m "not slow"

# With coverage
pytest --cov=starward

# Allure report
make report
```

## Common Patterns

### Calculate Rise/Set Times

```python
from starward.core.time import jd_now
from starward.core.sun import sunrise, sunset
from starward.core.observer import Observer

obs = Observer.from_degrees("Home", 40.7, -74.0)
jd = jd_now()

rise = sunrise(obs, jd)
set_t = sunset(obs, jd)

if rise and set_t:
    print(f"Sunrise: {rise.to_datetime()}")
    print(f"Sunset: {set_t.to_datetime()}")
```

### Find Best Observation Time

```python
from starward.core.visibility import transit_time, target_altitude
from starward.core.coords import ICRSCoord

target = ICRSCoord.parse("18h 36m 56s", "+38d 47m 01s")  # Vega
transit = transit_time(target, observer, jd)
alt_at_transit = target_altitude(target, observer, transit)

print(f"Transit: {transit.to_datetime()}")
print(f"Altitude: {alt_at_transit.degrees:.1f}°")
```

### Moon Phase Calendar

```python
from starward.core.moon import next_phase, MoonPhase
from starward.core.time import jd_now

jd = jd_now()
for phase in [MoonPhase.NEW, MoonPhase.FIRST_QUARTER,
              MoonPhase.FULL, MoonPhase.LAST_QUARTER]:
    next_jd = next_phase(jd, phase)
    print(f"{phase.name}: {next_jd.to_datetime().date()}")
```
