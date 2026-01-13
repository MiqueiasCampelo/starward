---
id: reference
title: CLI Reference
sidebar_label: Full Reference
sidebar_position: 2
---

# CLI Reference

Complete reference for all starward command-line commands.

---

## Global Options

These options apply to all commands and must appear **before** the subcommand:

| Option | Alias | Description |
|--------|-------|-------------|
| `--verbose` | `-v` | Show calculation steps |
| `--output` | `-o` | Output format: `plain` (default), `json`, or `latex` |
| `--json` | | Shortcut for `--output json` |
| `--precision` | `-p` | Output precision level (see below) |
| `--version` | | Show version and exit |
| `--help` | | Show help and exit |

⚠️ **Important**: Global options must come **before** the subcommand:
```bash
# ✓ Correct
starward --json time now
starward --verbose sun position
starward -p full time now

# ✗ Wrong (won't work)
starward time now --json
```

**Example**:
```bash
starward --verbose --output json time now
starward --json sun rise --lat 40.7 --lon -74.0
starward -p high angle sep "10h +30d" "11h +31d"
```

---

## Precision Levels

Control the display precision of numerical output. **All internal calculations use full IEEE 754 double precision** — this only affects how results are displayed.

| Level | Decimals | Use Case |
|-------|----------|----------|
| `compact` | 2 | Quick reference, minimal output |
| `display` | 4 | Human-readable, casual use |
| `standard` | 6 | Default precision for most work |
| `high` | 10 | Research applications |
| `full` | 15 | Maximum IEEE 754 precision |

```bash
# Compact: 0.26
starward -p compact time now

# Standard (default): 0.260077
starward time now

# Full precision: 0.260076993954923
starward -p full time now
```

You can also set precision via environment variable:
```bash
export ASTR0_PRECISION=high
starward time now  # Uses high precision
```

---

## Command Aliases

For faster typing, commands have short aliases:

| Command | Aliases |
|---------|---------|
| `time` | `t` |
| `coords` | `c`, `coord` |
| `angles` | `a`, `angle` |
| `constants` | `const` |

**Example**: `starward t now` is equivalent to `starward time now`

---

## time — Time Commands

Time conversions and astronomical time calculations.

### time now

Display current time in all astronomical formats.

```bash
starward time now
```

**Output includes**:
- UTC date and time
- Julian Date
- Modified Julian Date
- T (Julian centuries since J2000.0)
- Greenwich Mean Sidereal Time

---

### time convert

Convert Julian Date or MJD to calendar date.

```bash
starward time convert VALUE [--from FORMAT]
```

**Arguments**:
| Argument | Description |
|----------|-------------|
| `VALUE` | The Julian Date or MJD value |

**Options**:
| Option | Default | Description |
|--------|---------|-------------|
| `--from` | `jd` | Input format: `jd` or `mjd` |

**Examples**:
```bash
starward time convert 2460000.5
starward time convert 60000 --from mjd
```

---

### time jd

Convert calendar date to Julian Date.

```bash
starward time jd YEAR MONTH DAY [HOUR] [MINUTE] [SECOND]
```

**Arguments**:
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `YEAR` | Yes | — | Year (e.g., 2024) |
| `MONTH` | Yes | — | Month (1-12) |
| `DAY` | Yes | — | Day (1-31) |
| `HOUR` | No | 0 | Hour (0-23) |
| `MINUTE` | No | 0 | Minute (0-59) |
| `SECOND` | No | 0 | Second (0-59) |

**Example**:
```bash
starward time jd 2024 7 4 12 0 0
```

---

### time lst

Calculate Local Sidereal Time for a longitude.

```bash
starward time lst LONGITUDE [--jd JD]
```

**Arguments**:
| Argument | Description |
|----------|-------------|
| `LONGITUDE` | Observer longitude in degrees (positive East) |

**Options**:
| Option | Default | Description |
|--------|---------|-------------|
| `--jd` | Current time | Julian Date for calculation |

**Examples**:
```bash
starward time lst -- -118.25          # Los Angeles (note: -- before negative)
starward time lst 0                   # Greenwich
starward time lst 139.69 --jd 2460000.5  # Tokyo at specific JD
```

**Note**: Use `--` before negative longitudes to prevent them being interpreted as flags.

---

## coords — Coordinate Commands

Coordinate parsing and transformations.

### coords transform

Transform coordinates between systems.

```bash
starward coords transform COORDINATES --to SYSTEM [options]
```

**Arguments**:
| Argument | Description |
|----------|-------------|
| `COORDINATES` | Input coordinates (see format below) |

**Options**:
| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--to` | Yes | — | Target system: `icrs`, `galactic`, `altaz`, `horizontal` |
| `--from` | No | `icrs` | Source system: `icrs`, `galactic` |
| `--lat` | For altaz | — | Observer latitude (degrees) |
| `--lon` | For altaz | — | Observer longitude (degrees) |
| `--jd` | No | Current | Julian Date (for altaz) |

**Coordinate formats accepted**:
```text
"12h30m45s +45d30m00s"    # HMS/DMS
"12:30:45 +45:30:00"      # Colon notation
"187.6875 45.5"           # Decimal degrees
"l=135.0 b=71.6"          # Galactic (with --from galactic)
```

**Examples**:
```bash
# ICRS to Galactic
starward coords transform "12h30m +45d" --to galactic

# ICRS to Horizontal (requires location)
starward coords transform "12h30m +45d" --to altaz --lat 34.05 --lon -118.25

# Galactic to ICRS
starward coords transform "l=0 b=0" --from galactic --to icrs
```

---

### coords parse

Parse and display coordinate components.

```bash
starward coords parse COORDINATES
```

**Arguments**:
| Argument | Description |
|----------|-------------|
| `COORDINATES` | Coordinate string to parse |

**Example**:
```bash
starward coords parse "12h30m45.2s -45d30m15s"
```

**Output**:
```text
Parsed Coordinates:
  RA:  12h 30m 45.20s = 187.6883°
  Dec: -45° 30′ 15.00″ = -45.5042°
```

---

## angles — Angular Calculations

Angular measurements and calculations.

### angles sep

Calculate angular separation between two points.

```bash
starward angles sep COORD1 COORD2
```

**Arguments**:
| Argument | Description |
|----------|-------------|
| `COORD1` | First coordinate |
| `COORD2` | Second coordinate |

**Example**:
```bash
starward angles sep "10h30m +30d" "10h35m +31d"
```

**Output**:
```text
Angular Separation:
  1° 17′ 12.34″
  = 1.28676°
  = 77.206′
  = 4632.34″
```

**With verbose mode**:
```bash
starward --verbose angles sep "10h +30d" "11h +31d"
```
Shows the complete Vincenty formula calculation.

---

### angles pa

Calculate position angle from point 1 to point 2.

```bash
starward angles pa COORD1 COORD2
```

**Arguments**:
| Argument | Description |
|----------|-------------|
| `COORD1` | Reference point |
| `COORD2` | Target point |

**Example**:
```bash
starward angles pa "10h30m +30d" "10h35m +31d"
```

**Output**:
```text
Position Angle: 32.45° (N through E)
```

Position angle is measured from North (0°) through East (90°).

---

### angles convert

Convert an angle between units.

```bash
starward angles convert VALUE [--from UNIT]
```

**Arguments**:
| Argument | Description |
|----------|-------------|
| `VALUE` | Numeric value to convert |

**Options**:
| Option | Default | Description |
|--------|---------|-------------|
| `--from` | `deg` | Input unit: `deg`, `rad`, `hours`, `arcmin`, `arcsec` |

**Examples**:
```bash
starward angles convert 45.5 --from deg
starward angles convert 3.14159 --from rad
starward angles convert 12.5 --from hours
```

---

## constants — Astronomical Constants

Access to authoritative astronomical constants.

### constants list

List all available constants.

```bash
starward constants list
```

Displays all constants with their values, units, and references.

---

### constants search

Search for constants by name.

```bash
starward constants search QUERY
```

**Arguments**:
| Argument | Description |
|----------|-------------|
| `QUERY` | Search term (case-insensitive) |

**Examples**:
```bash
starward constants search solar
starward constants search earth
starward constants search julian
```

---

### constants show

Display a specific constant.

```bash
starward constants show NAME
```

**Arguments**:
| Argument | Description |
|----------|-------------|
| `NAME` | Constant attribute name |

**Available constants**:
- `c` — Speed of light
- `G` — Gravitational constant
- `AU` — Astronomical Unit
- `JD_J2000` — Julian Date of J2000.0
- `MJD_OFFSET` — Modified JD offset
- `julian_year` — Julian year in days
- `julian_century` — Julian century in days
- `arcsec_per_rad` — Arcseconds per radian
- `earth_radius_eq` — Earth equatorial radius
- `earth_flattening` — Earth flattening
- `earth_rotation_rate` — Earth rotation rate
- `obliquity_j2000` — Mean obliquity at J2000.0
- `ra_ngp` — RA of North Galactic Pole
- `dec_ngp` — Dec of North Galactic Pole
- `l_ncp` — Galactic longitude of NCP
- `M_sun` — Solar mass
- `R_sun` — Solar radius
- `L_sun` — Solar luminosity

**Example**:
```bash
starward constants show c
```

---

## about

Display information about starward.

```bash
starward about
```

Shows the ASCII banner, version, license, and motto.

---

## Output Formats

### Plain (Default)

Human-readable formatted output with Unicode characters.

```bash
starward time now
```

### JSON

Machine-readable JSON output.

```bash
starward --output json time now
```

```json
{
  "utc": "2026-01-03T00:15:00.000000+00:00",
  "julian_date": 2461043.5104166665,
  "modified_jd": 61043.01041666651,
  "j2000_centuries": 0.26005504109589043,
  "gmst_hours": 7.093055555555556
}
```

JSON output is useful for:
- Scripting and automation
- Piping to `jq` for processing
- Integration with other tools

---

## messier — Messier Catalog

Browse the 110 Messier deep-sky objects.

### messier list

```bash
starward messier list [--type TYPE] [--constellation CODE] [--magnitude MAG]
```

| Option | Description |
|--------|-------------|
| `--type` | Filter by type: `galaxy`, `globular_cluster`, `open_cluster`, `planetary_nebula`, `emission_nebula`, `reflection_nebula`, `supernova_remnant` |
| `--constellation` | Filter by constellation (3-letter code) |
| `--magnitude` | Show objects brighter than magnitude |

### messier show

```bash
starward messier show NUMBER
```

### messier search

```bash
starward messier search QUERY [--limit N]
```

### messier altitude / rise / transit / set

```bash
starward messier altitude NUMBER [--lat FLOAT] [--lon FLOAT] [--observer NAME] [--jd FLOAT]
starward messier rise NUMBER [OPTIONS]
starward messier transit NUMBER [OPTIONS]
starward messier set NUMBER [OPTIONS]
```

---

## ngc — NGC Catalog

Browse approximately 7,840 NGC deep-sky objects.

### ngc list

```bash
starward ngc list [--type TYPE] [--constellation CODE] [--magnitude MAG] [--limit N]
```

### ngc show

```bash
starward ngc show NUMBER
```

### ngc search

```bash
starward ngc search QUERY [--limit N]
```

### ngc stats

```bash
starward ngc stats
```

### ngc altitude / rise / transit / set

```bash
starward ngc altitude NUMBER [--lat FLOAT] [--lon FLOAT] [--observer NAME] [--jd FLOAT]
```

---

## ic — IC Catalog

Browse approximately 5,386 IC (Index Catalogue) objects.

### ic list / show / search / stats

Same interface as NGC commands.

```bash
starward ic list [--type TYPE] [--constellation CODE] [--magnitude MAG]
starward ic show NUMBER
starward ic search QUERY
starward ic stats
```

### ic altitude / rise / transit / set

```bash
starward ic altitude NUMBER [--lat FLOAT] [--lon FLOAT] [--observer NAME] [--jd FLOAT]
```

---

## caldwell — Caldwell Catalog

Browse the 109 Caldwell deep-sky objects.

### caldwell list / show / search / stats

Same interface as NGC commands.

```bash
starward caldwell list [--type TYPE] [--constellation CODE] [--magnitude MAG]
starward caldwell show NUMBER
starward caldwell search QUERY
starward caldwell stats
```

### caldwell altitude / rise / transit / set

```bash
starward caldwell altitude NUMBER [--lat FLOAT] [--lon FLOAT] [--observer NAME] [--jd FLOAT]
```

---

## stars — Hipparcos Star Catalog

Browse the Hipparcos bright star catalog.

### stars list

```bash
starward stars list [--constellation CODE] [--magnitude MAG] [--spectral CLASS] [--limit N]
```

| Option | Description |
|--------|-------------|
| `--constellation` | Filter by constellation |
| `--magnitude` | Show stars brighter than magnitude |
| `--spectral` | Filter by spectral class: O, B, A, F, G, K, M |
| `--limit` | Maximum results |

### stars show

```bash
starward stars show HIP_NUMBER
```

### stars search

```bash
starward stars search QUERY [--limit N]
```

Search by name, Bayer designation, spectral type, or constellation.

### stars stats

```bash
starward stars stats
```

### stars altitude / rise / transit / set

```bash
starward stars altitude HIP_NUMBER [--lat FLOAT] [--lon FLOAT] [--observer NAME] [--jd FLOAT]
```

---

## find — Cross-Catalog Search

Search for objects across all catalogs simultaneously.

### find search

```bash
starward find search QUERY [--catalog LIST] [--limit N]
```

| Option | Description |
|--------|-------------|
| `--catalog` | Catalogs to search: `ngc`, `ic`, `caldwell`, `hipparcos`, or `all` |
| `--limit` | Maximum results |

### find galaxies / nebulae / clusters / stars

```bash
starward find galaxies [--mag FLOAT] [--constellation CODE] [--catalog LIST] [--limit N]
starward find nebulae [OPTIONS]
starward find clusters [OPTIONS]
starward find stars [--spectral CLASS] [OPTIONS]
```

### find type

```bash
starward find type TYPE [--mag FLOAT] [--constellation CODE] [--catalog LIST] [--limit N]
```

Types: `galaxy`, `globular_cluster`, `open_cluster`, `planetary_nebula`, `emission_nebula`, `reflection_nebula`, `dark_nebula`, `supernova_remnant`

### find in

```bash
starward find in CONSTELLATION [--mag FLOAT] [--catalog LIST] [--limit N]
```

Find all objects in a constellation.

### find bright

```bash
starward find bright [--mag FLOAT] [--constellation CODE] [--catalog LIST]
```

Find bright objects suitable for naked-eye or binocular observation (default mag ≤ 6.0).

---

## list — Observation Lists

Create and manage custom observation lists.

### list create

```bash
starward list create NAME [-d DESCRIPTION]
```

### list ls

```bash
starward list ls
```

List all observation lists.

### list add

```bash
starward list add NAME OBJECT [-n NOTES]
```

Add an object to a list. Object formats:
- Messier: `M31`, `M 31`
- NGC: `NGC7000`, `NGC 7000`
- IC: `IC434`, `IC 434`
- Caldwell: `C14`, `Caldwell 14`
- Hipparcos: `HIP32349`

### list show

```bash
starward list show NAME
```

### list remove

```bash
starward list remove NAME OBJECT
```

### list note

```bash
starward list note NAME OBJECT NOTE
```

Update notes for an object (use "" to clear).

### list clear

```bash
starward list clear NAME
```

Remove all objects from a list.

### list rename

```bash
starward list rename OLD_NAME NEW_NAME
```

### list delete

```bash
starward list delete NAME
```

### list export

```bash
starward list export NAME [-f FORMAT] [-o FILE]
```

| Option | Description |
|--------|-------------|
| `-f`, `--format` | Export format: `csv` (default) or `json` |
| `-o`, `--output` | Output file (default: stdout) |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Command line usage error |

---

## Environment Variables

Currently, starward does not use environment variables. Future versions may support:
- `ASTR0_DEFAULT_FORMAT` — Default output format
- `ASTR0_OBSERVER_LAT` / `ASTR0_OBSERVER_LON` — Default observer location

---

## Tips

### Handling Negative Numbers

Use `--` to separate options from arguments with negative values:

```bash
starward time lst -- -118.25
```

### Combining Options

```bash
starward -v -o json coords transform "12h +45d" --to galactic
```

### Chaining with Other Tools

```bash
# Get just the Julian Date
starward --output json time now | jq '.julian_date'

# Store result in a variable
JD=$(starward --output json time now | jq -r '.julian_date')
```

---

*Next: [Python API](/docs/python-api/reference) — Using starward as a library*
