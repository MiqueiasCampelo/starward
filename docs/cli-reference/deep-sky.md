---
id: deep-sky
title: Deep-Sky Catalogs
sidebar_label: Deep-Sky Catalogs
sidebar_position: 6
description: Browse and search Messier, NGC, IC, and Caldwell deep-sky object catalogs.
---

# Deep-Sky Catalogs

starward provides access to four major deep-sky object catalogs containing galaxies, nebulae, star clusters, and other non-stellar objects.

## Catalog Overview

| Catalog | Command | Objects | Description |
|---------|---------|---------|-------------|
| Messier | `messier` | 110 | Classic catalog by Charles Messier |
| NGC | `ngc` | ~7,840 | New General Catalogue |
| IC | `ic` | ~5,386 | Index Catalogue (NGC supplement) |
| Caldwell | `caldwell` | 109 | Patrick Moore's complement to Messier |

## Object Types

All catalogs categorize objects by type:

| Type | Description |
|------|-------------|
| `galaxy` | Spiral, elliptical, irregular galaxies |
| `globular_cluster` | Dense spherical star clusters |
| `open_cluster` | Loose stellar associations |
| `planetary_nebula` | Shells ejected by dying stars |
| `emission_nebula` | Gas clouds glowing from stellar radiation |
| `reflection_nebula` | Dust clouds reflecting starlight |
| `dark_nebula` | Opaque dust clouds |
| `supernova_remnant` | Expanding debris from stellar explosions |
| `star_cloud` | Dense regions of the Milky Way |

---

## messier — Messier Catalog

The 110 Messier objects cataloged by Charles Messier in the 18th century, comprising the finest deep-sky objects visible from mid-northern latitudes.

### messier list

List Messier objects with optional filters.

```bash
starward messier list [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--type TYPE` | Filter by object type |
| `--constellation CODE` | Filter by constellation (3-letter code) |
| `--magnitude MAG` | Show objects brighter than magnitude |

**Examples:**

```bash
# List all Messier objects
starward messier list

# List only galaxies
starward messier list --type galaxy

# Objects in Sagittarius
starward messier list --constellation Sgr

# Bright objects (mag < 6)
starward messier list --magnitude 6

# Combine filters
starward messier list --type globular_cluster --magnitude 7
```

### messier show

Display detailed information about a Messier object.

```bash
starward messier show NUMBER
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `NUMBER` | Messier number (1-110) |

**Example:**

```bash
starward messier show 31
```

**Output:**

```
M 31 — Andromeda Galaxy
────────────────────────────────────────
  Type            galaxy
  Constellation   And
  Coordinates     00h 42m 44.3s  +41° 16′ 09″
  Magnitude       3.4
  Size            178.0′ × 63.0′
  Distance        2.54 Mly
  NGC             224
────────────────────────────────────────
```

### messier search

Search Messier objects by name, type, or constellation.

```bash
starward messier search QUERY [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `QUERY` | Search term (case-insensitive) |

**Options:**

| Option | Description |
|--------|-------------|
| `--limit N` | Maximum results (default: 25) |

**Examples:**

```bash
# Search by common name
starward messier search "orion"
starward messier search "ring"

# Search by type
starward messier search "galaxy"

# Search by constellation
starward messier search "Sgr"
```

### messier altitude

Calculate the current altitude of a Messier object.

```bash
starward messier altitude NUMBER [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--lat FLOAT` | Observer latitude (degrees) |
| `--lon FLOAT` | Observer longitude (degrees) |
| `--observer NAME` | Use named observer profile |
| `--jd FLOAT` | Julian Date (default: now) |

**Example:**

```bash
starward messier altitude 31 --lat 40.7 --lon -74.0
```

### messier rise / transit / set

Calculate rise, transit, or set times for a Messier object.

```bash
starward messier rise NUMBER [OPTIONS]
starward messier transit NUMBER [OPTIONS]
starward messier set NUMBER [OPTIONS]
```

**Options:** Same as `altitude` command.

**Example:**

```bash
starward messier transit 42 --observer greenwich
```

---

## ngc — NGC Catalog

The New General Catalogue containing approximately 7,840 deep-sky objects, the primary professional reference catalog.

### ngc list

List NGC objects with optional filters.

```bash
starward ngc list [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--type TYPE` | Filter by object type |
| `--constellation CODE` | Filter by constellation |
| `--magnitude MAG` | Show objects brighter than magnitude |
| `--limit N` | Maximum results |

**Examples:**

```bash
# List NGC objects (default limit applies)
starward ngc list

# Planetary nebulae
starward ngc list --type planetary_nebula

# Bright galaxies in Virgo
starward ngc list --type galaxy --constellation Vir --magnitude 11
```

### ngc show

Display detailed information about an NGC object.

```bash
starward ngc show NUMBER
```

**Example:**

```bash
starward ngc show 7000
```

**Output:**

```
NGC 7000 — North America Nebula
────────────────────────────────────────
  Type            emission_nebula
  Constellation   Cyg
  Coordinates     20h 59m 17.1s  +44° 31′ 44″
  Magnitude       4.0
  Size            120.0′ × 100.0′
  Messier         —
────────────────────────────────────────
```

### ngc search

Search NGC objects by name, type, or constellation.

```bash
starward ngc search QUERY [OPTIONS]
```

**Examples:**

```bash
starward ngc search "veil"
starward ngc search "cygnus"
starward ngc search "galaxy"
```

### ngc stats

Display catalog statistics.

```bash
starward ngc stats
```

**Output:**

```
NGC Catalog Statistics
────────────────────────────────────────
  Total objects     7,840

  By Type:
    galaxy              5,234
    open_cluster          632
    globular_cluster      152
    planetary_nebula      245
    emission_nebula       412
    ...
────────────────────────────────────────
```

### ngc altitude / rise / transit / set

Calculate visibility for NGC objects. Same options as Messier commands.

```bash
starward ngc altitude 7000 --lat 51.5 --lon 0
starward ngc transit 224 --observer greenwich
```

---

## ic — IC Catalog

The Index Catalogue containing approximately 5,386 objects, serving as a supplement to the NGC.

### ic list

List IC objects with optional filters.

```bash
starward ic list [OPTIONS]
```

**Options:** Same as `ngc list`.

**Examples:**

```bash
# Dark nebulae
starward ic list --type dark_nebula

# Objects in Orion
starward ic list --constellation Ori
```

### ic show

Display detailed information about an IC object.

```bash
starward ic show NUMBER
```

**Example:**

```bash
starward ic show 434
```

**Output:**

```
IC 434 — Horsehead Nebula
────────────────────────────────────────
  Type            dark_nebula
  Constellation   Ori
  Coordinates     05h 40m 59.0s  −02° 27′ 30″
  Magnitude       —
  Size            60.0′ × 10.0′
────────────────────────────────────────
```

### ic search / stats / altitude / rise / transit / set

Same interface as NGC commands.

```bash
starward ic search "horsehead"
starward ic stats
starward ic altitude 434 --lat 40.7 --lon -74.0
```

---

## caldwell — Caldwell Catalog

The 109 Caldwell objects compiled by Sir Patrick Moore, featuring deep-sky objects not included in the Messier catalog.

### caldwell list

List Caldwell objects with optional filters.

```bash
starward caldwell list [OPTIONS]
```

**Options:** Same as other catalogs.

**Examples:**

```bash
# List all Caldwell objects
starward caldwell list

# Southern hemisphere objects
starward caldwell list --constellation Car

# Bright galaxies
starward caldwell list --type galaxy --magnitude 9
```

### caldwell show

Display detailed information about a Caldwell object.

```bash
starward caldwell show NUMBER
```

**Example:**

```bash
starward caldwell show 14
```

**Output:**

```
C 14 — Double Cluster
────────────────────────────────────────
  Type            open_cluster
  Constellation   Per
  Coordinates     02h 20m 00.0s  +57° 08′ 00″
  Magnitude       4.3
  Size            60.0′
  NGC             869
────────────────────────────────────────
```

### caldwell search / stats / altitude / rise / transit / set

Same interface as other catalog commands.

```bash
starward caldwell search "sculptor"
starward caldwell stats
starward caldwell transit 14 --observer greenwich
```

---

## Cross-References

Many objects appear in multiple catalogs. The `show` command displays cross-references:

```bash
starward messier show 31    # Shows NGC 224
starward ngc show 224       # Shows M 31
starward caldwell show 14   # Shows NGC 869
```

For searching across all catalogs simultaneously, use the [`find`](/docs/cli-reference/finder) command.

---

## JSON Output

All commands support JSON output for scripting:

```bash
starward --json messier show 31
starward --json ngc list --type galaxy --limit 10
starward --json caldwell stats
```

**Example JSON:**

```json
{
  "number": 31,
  "name": "Andromeda Galaxy",
  "type": "galaxy",
  "constellation": "And",
  "ra_hours": 0.7123,
  "dec_degrees": 41.2692,
  "magnitude": 3.4,
  "ngc_number": 224
}
```

---

## Tips

### Finding Objects

```bash
# Find an object by common name
starward messier search "whirlpool"
starward ngc search "ring nebula"

# Find all objects in a constellation
starward ngc list --constellation Ori
starward messier list --constellation Sgr
```

### Planning Observations

```bash
# Check if object is above horizon
starward messier altitude 42 --lat 40.7 --lon -74.0

# Find transit time (best viewing)
starward ngc transit 7000 --lat 51.5 --lon 0

# List bright objects for tonight
starward messier list --magnitude 8
```

### Scripting

```bash
# Get coordinates for planetarium software
starward --json messier show 31 | jq '{ra: .ra_hours, dec: .dec_degrees}'

# Export list of galaxies
starward --json ngc list --type galaxy --magnitude 12 > galaxies.json
```

---

*Next: [Star Catalog](/docs/cli-reference/stars) — Hipparcos bright stars*
