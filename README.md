# starward

An educational astronomy toolkit that shows its work.

```bash
pip install starward  # Python 3.9+
```

**Documentation**: [starward.dev](https://starward.dev)

Most astronomy software treats calculations as black boxes. **starward** is different—every calculation can show its work with `--verbose` mode, turning opaque computations into learning opportunities.

```
$ starward --verbose angle sep "10h00m +45d" "10h30m +46d"

╭─ Angular Separation ─────────────────────────────────────────────╮
│                                                                  │
│  Point 1:  RA 10h 00m 00.00s   Dec +45° 00' 00.0"                │
│  Point 2:  RA 10h 30m 00.00s   Dec +46° 00' 00.0"                │
│                                                                  │
├─ Step 1: Convert to radians ─────────────────────────────────────┤
│  α₁ = 2.617993877991494 rad    δ₁ = 0.785398163397448 rad        │
│  α₂ = 2.748893571891069 rad    δ₂ = 0.802851455917547 rad        │
│                                                                  │
├─ Step 2: Vincenty formula ───────────────────────────────────────┤
│  Δα = 0.130899693899575 rad                                      │
│  sin δ₁ = 0.707106781186548    cos δ₁ = 0.707106781186547        │
│  sin δ₂ = 0.719339800338651    cos δ₂ = 0.694658370458997        │
│                                                                  │
├─ Result ─────────────────────────────────────────────────────────┤
│  θ = 5.277003618837505°  =  5° 16' 37.21"                        │
│                                                                  │
╰──────────────────────────────────────────────────────────────────╯

Angular Separation: 5° 16' 37.21"
```

## Quick Start

### Time

```bash
# Current astronomical time
starward time now

# Convert Julian Date
starward time convert 2451545.0

# Sidereal time at longitude
starward time lst 2460000.5 -74.0
```

### Sun & Moon

```bash
# Solar position
starward sun position

# Sunrise and sunset
starward sun rise --lat 51.5 --lon -0.1
starward sun set --lat 51.5 --lon -0.1

# Twilight times
starward sun twilight astronomical --lat 51.5 --lon -0.1

# Current moon phase
starward moon phase

# Next full moon
starward moon next full

# Moonrise
starward moon rise --lat 40.7 --lon -74.0
```

### Planets

```bash
# Current position of a planet
starward planets position mars

# All planets summary
starward planets all

# Planet rise/set/transit
starward planets rise jupiter --lat 40.7 --lon -74.0
starward planets transit saturn --lat 40.7 --lon -74.0
```

### Coordinates

```bash
# Transform between coordinate systems
starward coord convert "18h36m56s +38d47m01s" galactic

# Angular separation
starward angle sep "00h42m44s +41d16m09s" "01h33m51s +30d39m37s"
```

### Visibility Planning

```bash
# Target altitude now
starward vis altitude "00h42m44s" "+41d16m09s" --lat 40.7 --lon -74.0

# Transit time
starward vis transit "00h42m44s" "+41d16m09s" --lat 40.7 --lon -74.0

# Airmass
starward vis airmass "00h42m44s" "+41d16m09s" --lat 40.7 --lon -74.0
```

### Observer Management

```bash
# Save your location
starward observer add "Home" 40.7128 -74.0060 --timezone "America/New_York"

# Set as default
starward observer default "Home"

# List saved observers
starward observer list
```

### Catalogs

```bash
# Look up Messier objects
starward messier M31

# Search NGC catalog
starward ngc 7000

# Hipparcos star lookup
starward hipparcos 32349
```

### Constants

```bash
# List all constants
starward const list

# Search constants
starward const search solar
```

---

## Features

### v0.1 "First Light"

| Module | Capabilities |
|--------|-------------|
| **Time** | Julian Date ↔ Calendar, GMST, LST, MJD |
| **Angles** | Parse/format DMS/HMS, separation, position angle |
| **Coordinates** | ICRS, Galactic, Horizontal transforms |
| **Constants** | 30+ IAU/CODATA constants with uncertainties |

### v0.2 "Steady Tracking"

| Module | Capabilities |
|--------|-------------|
| **Sun** | Position, rise/set, twilight (civil/nautical/astronomical), equation of time |
| **Moon** | Position, phase, illumination, rise/set, next phase prediction |
| **Observer** | Location management, TOML persistence, timezone support |
| **Visibility** | Airmass, transit, rise/set, moon separation, night detection |

### v0.3 "Planetary Motion"

| Module | Capabilities |
|--------|-------------|
| **Planets** | Mercury–Neptune positions, magnitude, elongation, rise/set/transit |

### v0.4 "Deep Sky"

| Module | Capabilities |
|--------|-------------|
| **Catalogs** | Messier (110), NGC (7,840), IC (5,386), Caldwell (109), Hipparcos (118,218) |
| **Search** | Cross-catalog search by name, type, magnitude |

### Coming Soon

- **v0.5**: IAU 2006 precession/nutation, aberration

---

## Python API

Use starward as a library in your Python projects:

```python
from starward.core.time import JulianDate, jd_now
from starward.core.coords import ICRSCoord
from starward.core.angles import Angle, angular_separation
from starward.core.sun import sun_position, sunrise, sunset
from starward.core.moon import moon_phase, next_phase, MoonPhase
from starward.core.observer import Observer
from starward.core.visibility import airmass, target_altitude, compute_visibility
from starward.core.planets import Planet, planet_position, all_planet_positions

# Time
jd = jd_now()
j2000 = JulianDate.j2000()
past = JulianDate.from_calendar(1969, 7, 20, 20, 17, 0)

# Coordinates
vega = ICRSCoord.parse("18h36m56.3s +38d47m01s")
m31 = ICRSCoord.from_degrees(10.684, 41.269)
galactic = vega.to_galactic()

# Angles
sep = angular_separation(vega.ra, vega.dec, m31.ra, m31.dec)
angle = Angle.parse("45d30m15.5s")

# Sun
pos = sun_position(jd)
greenwich = Observer.from_degrees("Greenwich", 51.4772, -0.0005)
rise = sunrise(greenwich, jd)

# Moon
phase = moon_phase(jd)
print(f"Moon: {phase.name}, {phase.percent_illuminated:.0f}% illuminated")
next_full = next_phase(jd, MoonPhase.FULL_MOON)

# Visibility
alt = target_altitude(m31, greenwich, jd)
X = airmass(alt)
vis = compute_visibility(m31, greenwich, jd)

# Planets
mars = planet_position(Planet.MARS, jd)
print(f"Mars: RA {mars.ra.format_hms()}, Mag {mars.magnitude:+.1f}")
all_planets = all_planet_positions(jd)
```

---

## Philosophy

### 1. **Transparency Over Magic**

Every function can explain itself. Use verbose mode to see the mathematics:

```python
from starward.verbose import VerboseContext

ctx = VerboseContext()
result = angular_separation(ra1, dec1, ra2, dec2, verbose=ctx)

for step in ctx.steps:
    print(step)
```

### 2. **Education First**

starward is designed for learning. The code is documented, the algorithms are cited, and the output explains itself.

### 3. **Precision Matters**

- Full IEEE 754 double precision throughout
- Tested against authoritative sources (USNO, JPL, IAU)
- Explicit uncertainty handling for constants

### 4. **Progressive Complexity**

Start simple, go deep when needed:

```bash
# Simple: just the answer
starward sun rise --lat 51.5 --lon -0.1

# Intermediate: JSON for scripting
starward --json sun rise --lat 51.5 --lon -0.1

# Advanced: show all work
starward --verbose sun rise --lat 51.5 --lon -0.1
```

---

## Documentation

Full documentation is available at [starward.dev](https://starward.dev), including:

- Getting started guide
- Module guides for time, coordinates, sun, moon, planets, and catalogs
- CLI reference
- Python API reference

---

## Command Shortcuts

For speed, starward supports command aliases:

| Full Command | Shortcut |
|--------------|----------|
| `starward time` | `starward t` |
| `starward angle` | `starward a` |
| `starward coord` | `starward c` |
| `starward const` | `starward k` |
| `starward sun` | `starward s` |
| `starward moon` | `starward m` |
| `starward planets` | `starward p` |
| `starward observer` | `starward o` |
| `starward vis` | `starward v` |

---

## Output Formats

```bash
# Human-readable (default)
starward time now

# JSON for scripting
starward --json time now

# LaTeX for publications
starward --output latex coord convert "18h36m56s +38d47m01s" galactic
```

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=starward

# Run specific module tests
pytest tests/core/test_sun.py

# Run only fast tests
pytest -m "not slow"
```

500+ tests validate calculations against authoritative sources including:
- US Naval Observatory
- JPL Horizons
- IAU SOFA library
- Astronomical Algorithms (Meeus)

---

## Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Acknowledgments

starward builds upon decades of astronomical research. Key references:

- Meeus, Jean. *Astronomical Algorithms* (2nd ed.)
- Urban & Seidelmann. *Explanatory Supplement to the Astronomical Almanac* (3rd ed.)
- IAU SOFA Collection
- JPL Solar System Dynamics

---

## License

MIT License. See [LICENSE](LICENSE) for details.
