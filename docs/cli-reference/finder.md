---
id: finder
title: Object Finder
sidebar_label: Object Finder
sidebar_position: 8
description: Search for astronomical objects across multiple catalogs simultaneously.
---

# Object Finder

The `find` command provides cross-catalog search capabilities, allowing you to search for deep-sky objects and stars across NGC, IC, Caldwell, and Hipparcos catalogs simultaneously.

## Overview

Instead of searching each catalog individually, the finder lets you:

- **Search by name** across all catalogs at once
- **Filter by object type** (galaxies, nebulae, clusters)
- **Find objects by constellation**
- **Discover bright objects** for visual observation

---

## find search

Search for objects by name or description across all catalogs.

```bash
starward find search QUERY [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `QUERY` | Search term (case-insensitive) |

**Options:**

| Option | Description |
|--------|-------------|
| `--catalog LIST` | Catalogs to search: `ngc`, `ic`, `caldwell`, `hipparcos`, or `all` (default: all) |
| `--limit N` | Maximum results (default: 25) |

**Examples:**

```bash
# Search all catalogs for "orion"
starward find search orion

# Search only NGC and IC catalogs
starward find search "veil nebula" --catalog ngc,ic

# Search with higher limit
starward find search "ring" --limit 50
```

**Output:**

```
Cross-Catalog Search: "orion"
────────────────────────────────────────
  NGC 1976    Orion Nebula           emission_nebula    Ori   4.0
  NGC 1977    Running Man Nebula     reflection_nebula  Ori   7.0
  NGC 2024    Flame Nebula           emission_nebula    Ori   —
  IC 434      Horsehead Nebula       dark_nebula        Ori   —
  HIP 27989   Betelgeuse             star               Ori   0.42
  HIP 24436   Rigel                  star               Ori   0.13
  ...
────────────────────────────────────────
```

---

## find galaxies

Find galaxies across deep-sky catalogs.

```bash
starward find galaxies [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--mag FLOAT` | Maximum magnitude (brighter than) |
| `--constellation CODE` | Filter by constellation |
| `--catalog LIST` | Catalogs to search: `ngc`, `ic`, `caldwell`, or `all` |
| `--limit N` | Maximum results (default: 25) |

**Examples:**

```bash
# Find all galaxies
starward find galaxies

# Bright galaxies (mag < 10)
starward find galaxies --mag 10

# Galaxies in Virgo Cluster
starward find galaxies --constellation Vir --mag 12

# Search only Caldwell catalog
starward find galaxies --catalog caldwell
```

**Output:**

```
Galaxies (mag ≤ 10.0)
────────────────────────────────────────
  NGC 224     Andromeda Galaxy       And   3.4    178.0′
  NGC 598     Triangulum Galaxy      Tri   5.7    73.0′
  NGC 253     Sculptor Galaxy        Scl   7.1    27.5′
  NGC 4472    M49                    Vir   8.4    10.2′
  NGC 4486    Virgo A (M87)          Vir   8.6    8.3′
  ...
────────────────────────────────────────
```

---

## find nebulae

Find nebulae (emission, reflection, planetary, dark, supernova remnants).

```bash
starward find nebulae [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--mag FLOAT` | Maximum magnitude |
| `--constellation CODE` | Filter by constellation |
| `--catalog LIST` | Catalogs to search |
| `--limit N` | Maximum results |

**Examples:**

```bash
# Find all nebulae
starward find nebulae

# Bright nebulae
starward find nebulae --mag 8

# Nebulae in Cygnus
starward find nebulae --constellation Cyg
```

---

## find clusters

Find star clusters (open and globular).

```bash
starward find clusters [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--mag FLOAT` | Maximum magnitude |
| `--constellation CODE` | Filter by constellation |
| `--catalog LIST` | Catalogs to search |
| `--limit N` | Maximum results |

**Examples:**

```bash
# Find all star clusters
starward find clusters

# Bright clusters for binoculars
starward find clusters --mag 6

# Clusters in Perseus
starward find clusters --constellation Per
```

---

## find stars

Find stars from the Hipparcos catalog.

```bash
starward find stars [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--mag FLOAT` | Maximum magnitude |
| `--constellation CODE` | Filter by constellation |
| `--spectral CLASS` | Filter by spectral class |
| `--limit N` | Maximum results |

**Examples:**

```bash
# Bright stars
starward find stars --mag 2

# Red giants in Orion
starward find stars --constellation Ori --spectral M

# All named stars
starward find stars --mag 4
```

---

## find type

Find objects by specific type across all catalogs.

```bash
starward find type TYPE [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `TYPE` | Object type (see table below) |

**Available Types:**

| Type | Description |
|------|-------------|
| `galaxy` | All galaxy types |
| `spiral_galaxy` | Spiral galaxies |
| `elliptical_galaxy` | Elliptical galaxies |
| `globular_cluster` | Globular clusters |
| `open_cluster` | Open clusters |
| `planetary_nebula` | Planetary nebulae |
| `emission_nebula` | Emission nebulae |
| `reflection_nebula` | Reflection nebulae |
| `dark_nebula` | Dark nebulae |
| `supernova_remnant` | Supernova remnants |

**Options:**

| Option | Description |
|--------|-------------|
| `--mag FLOAT` | Maximum magnitude |
| `--constellation CODE` | Filter by constellation |
| `--catalog LIST` | Catalogs to search |
| `--limit N` | Maximum results |

**Examples:**

```bash
# Find planetary nebulae
starward find type planetary_nebula

# Bright globular clusters
starward find type globular_cluster --mag 7

# Supernova remnants
starward find type supernova_remnant
```

---

## find in

Find all cataloged objects in a constellation.

```bash
starward find in CONSTELLATION [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `CONSTELLATION` | Constellation code (3-letter IAU abbreviation) |

**Options:**

| Option | Description |
|--------|-------------|
| `--mag FLOAT` | Maximum magnitude |
| `--catalog LIST` | Catalogs to search |
| `--limit N` | Maximum results |

**Examples:**

```bash
# All objects in Orion
starward find in Ori

# Bright objects in Sagittarius
starward find in Sgr --mag 8

# Objects in Cygnus from NGC only
starward find in Cyg --catalog ngc
```

**Output:**

```
Objects in Orion (Ori)
────────────────────────────────────────
Stars:
  HIP 24436   Rigel              B8Ia    0.13
  HIP 27989   Betelgeuse         M1Ia    0.42
  HIP 26727   Bellatrix          B2III   1.64
  ...

Deep-Sky Objects:
  NGC 1976    Orion Nebula       emission_nebula    4.0
  NGC 1977    Running Man        reflection_nebula  7.0
  NGC 2024    Flame Nebula       emission_nebula    —
  IC 434      Horsehead          dark_nebula        —
  ...
────────────────────────────────────────
```

---

## find bright

Find bright objects suitable for naked-eye or binocular observation.

```bash
starward find bright [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--mag FLOAT` | Maximum magnitude (default: 6.0 for naked eye) |
| `--constellation CODE` | Filter by constellation |
| `--catalog LIST` | Catalogs to search |
| `--limit N` | Maximum results |

**Examples:**

```bash
# Naked-eye objects (mag ≤ 6)
starward find bright

# Binocular objects (mag ≤ 8)
starward find bright --mag 8

# Bright objects in current season's constellations
starward find bright --constellation Ori
starward find bright --constellation Cyg
```

**Output:**

```
Bright Objects (mag ≤ 6.0)
────────────────────────────────────────
Stars:
  Sirius          CMa   −1.46
  Canopus         Car   −0.74
  Arcturus        Boo   −0.05
  Vega            Lyr    0.03
  ...

Deep-Sky Objects:
  M 31    Andromeda Galaxy    And   3.4
  M 42    Orion Nebula        Ori   4.0
  M 45    Pleiades            Tau   1.6
  M 44    Beehive Cluster     Cnc   3.7
  ...
────────────────────────────────────────
```

---

## JSON Output

All commands support JSON output:

```bash
starward --json find search "orion"
starward --json find galaxies --mag 10
starward --json find in Cyg
```

**Example JSON:**

```json
{
  "query": "orion",
  "results": [
    {
      "catalog": "NGC",
      "number": 1976,
      "name": "Orion Nebula",
      "type": "emission_nebula",
      "constellation": "Ori",
      "magnitude": 4.0,
      "ra_hours": 5.5908,
      "dec_degrees": -5.3911
    },
    {
      "catalog": "HIP",
      "number": 27989,
      "name": "Betelgeuse",
      "type": "star",
      "constellation": "Ori",
      "magnitude": 0.42,
      "spectral_type": "M1Ia"
    }
  ]
}
```

---

## Constellation Codes

Common constellation codes for filtering:

| Code | Name | Notable Objects |
|------|------|-----------------|
| `And` | Andromeda | M31, NGC 752 |
| `Cyg` | Cygnus | NGC 7000, M29 |
| `Ori` | Orion | M42, NGC 2024, Betelgeuse |
| `Sgr` | Sagittarius | M8, M20, M22 |
| `Vir` | Virgo | M87, galaxy cluster |
| `UMa` | Ursa Major | M81, M82, M101 |
| `Cas` | Cassiopeia | NGC 457, M52 |
| `Per` | Perseus | Double Cluster, M34 |
| `Tau` | Taurus | M45, M1, Aldebaran |
| `Sco` | Scorpius | M4, M7, Antares |

---

## Tips

### Quick Discovery

```bash
# What's bright in tonight's sky?
starward find bright --constellation Ori

# Find something interesting to observe
starward find galaxies --mag 10 --limit 10

# Discover nebulae in summer constellations
starward find nebulae --constellation Cyg
starward find nebulae --constellation Sgr
```

### Building Observation Lists

```bash
# Find targets, then add to a list
starward find galaxies --mag 11 --constellation Vir
starward list add "Virgo Galaxies" NGC4472
starward list add "Virgo Galaxies" NGC4486
```

### Scripting

```bash
# Get all Messier-equivalent bright objects
starward --json find bright --mag 8 | jq '.results | length'

# Export constellation objects for planning
starward --json find in Ori > orion_objects.json
```

---

## See Also

- [Deep-Sky Catalogs](/docs/cli-reference/deep-sky) — Individual catalog commands
- [Star Catalog](/docs/cli-reference/stars) — Hipparcos catalog
- [Observation Lists](/docs/cli-reference/lists) — Saving found objects

---

*Next: [Observation Lists](/docs/cli-reference/lists) — Managing custom lists*
