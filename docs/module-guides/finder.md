---
id: finder
title: Finder Module
sidebar_label: Finder
sidebar_position: 11
description: Python API for cross-catalog search across NGC, IC, Caldwell, and Hipparcos catalogs.
---

# Finder Module

The finder module provides cross-catalog search capabilities, allowing you to search for astronomical objects across multiple catalogs simultaneously.

## Overview

Instead of querying each catalog separately, the finder provides unified search functions:

```python
from starward.core.finder import (
    find_by_name,
    find_galaxies,
    find_nebulae,
    find_clusters,
    find_stars,
    find_by_type,
    find_in_constellation,
    find_bright,
)
```

---

## find_by_name

Search for objects by name or description across all catalogs.

```python
from starward.core.finder import find_by_name

# Search all catalogs
results = find_by_name("orion")

for obj in results:
    print(f"{obj.catalog} {obj.number}: {obj.name}")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | str | Search term (case-insensitive) |
| `catalogs` | list | Catalogs to search (default: all) |
| `limit` | int | Maximum results (default: 25) |

**Returns:** List of catalog objects (mixed types).

### Example

```python
# Search for "ring" across all catalogs
results = find_by_name("ring")

# Results include:
# - M57 (Ring Nebula) from Messier
# - NGC 6720 (Ring Nebula) from NGC
# - Various other "ring" matches
```

---

## find_galaxies

Find galaxies across deep-sky catalogs.

```python
from starward.core.finder import find_galaxies

# All galaxies brighter than magnitude 10
galaxies = find_galaxies(max_magnitude=10.0)

# Galaxies in Virgo
virgo_galaxies = find_galaxies(
    max_magnitude=12.0,
    constellation="Vir"
)

for g in virgo_galaxies[:5]:
    print(f"{g.catalog} {g.number}: {g.name} (mag {g.magnitude})")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_magnitude` | float | Maximum visual magnitude |
| `constellation` | str | Filter by constellation code |
| `catalogs` | list | Catalogs to search (default: ngc, ic, caldwell) |
| `limit` | int | Maximum results |

---

## find_nebulae

Find nebulae of all types (emission, reflection, planetary, dark, supernova remnants).

```python
from starward.core.finder import find_nebulae

# Bright nebulae
nebulae = find_nebulae(max_magnitude=8.0)

# Nebulae in Cygnus
cyg_nebulae = find_nebulae(constellation="Cyg")

for n in nebulae:
    print(f"{n.catalog} {n.number}: {n.name} ({n.object_type})")
```

**Parameters:** Same as `find_galaxies`.

---

## find_clusters

Find star clusters (open and globular).

```python
from starward.core.finder import find_clusters

# All bright clusters
clusters = find_clusters(max_magnitude=7.0)

# Clusters in Perseus (includes Double Cluster)
per_clusters = find_clusters(constellation="Per")
```

**Parameters:** Same as `find_galaxies`.

---

## find_stars

Find stars from the Hipparcos catalog.

```python
from starward.core.finder import find_stars

# Bright stars
bright = find_stars(max_magnitude=2.0)

# Red giants in Orion
orion_red = find_stars(
    constellation="Ori",
    spectral_class="M"
)

for s in bright[:5]:
    print(f"HIP {s.hip_number}: {s.name} ({s.spectral_type})")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_magnitude` | float | Maximum visual magnitude |
| `constellation` | str | Filter by constellation |
| `spectral_class` | str | Filter by spectral class (O, B, A, F, G, K, M) |
| `limit` | int | Maximum results |

---

## find_by_type

Find objects by specific type across all catalogs.

```python
from starward.core.finder import find_by_type

# Planetary nebulae
planetaries = find_by_type("planetary_nebula", max_magnitude=12.0)

# Globular clusters
globulars = find_by_type("globular_cluster", max_magnitude=8.0)

# Supernova remnants
snr = find_by_type("supernova_remnant")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `object_type` | str | Type to search for |
| `max_magnitude` | float | Maximum visual magnitude |
| `constellation` | str | Filter by constellation |
| `catalogs` | list | Catalogs to search |
| `limit` | int | Maximum results |

**Available Types:**

- `galaxy`
- `globular_cluster`
- `open_cluster`
- `planetary_nebula`
- `emission_nebula`
- `reflection_nebula`
- `dark_nebula`
- `supernova_remnant`

---

## find_in_constellation

Find all cataloged objects in a constellation.

```python
from starward.core.finder import find_in_constellation

# Everything in Orion
orion = find_in_constellation("Ori")

print(f"Found {len(orion)} objects in Orion")

# Separate by category
stars = [o for o in orion if hasattr(o, 'hip_number')]
deep_sky = [o for o in orion if not hasattr(o, 'hip_number')]

print(f"Stars: {len(stars)}, Deep-sky: {len(deep_sky)}")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `constellation` | str | IAU 3-letter constellation code |
| `max_magnitude` | float | Maximum visual magnitude |
| `catalogs` | list | Catalogs to search |
| `limit` | int | Maximum results |

---

## find_bright

Find bright objects suitable for naked-eye or binocular observation.

```python
from starward.core.finder import find_bright

# Naked-eye objects (mag ≤ 6.0)
naked_eye = find_bright()

# Binocular objects (mag ≤ 8.0)
binocular = find_bright(max_magnitude=8.0)

# Bright objects in current season's sky
summer = find_bright(
    max_magnitude=6.0,
    constellation="Cyg"
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_magnitude` | float | Maximum magnitude (default: 6.0) |
| `constellation` | str | Filter by constellation |
| `catalogs` | list | Catalogs to search |
| `limit` | int | Maximum results |

---

## Working with Results

Finder functions return mixed object types. Check the type or use attributes:

```python
from starward.core.finder import find_by_name
from starward.core.messier_types import MessierObject
from starward.core.ngc_types import NGCObject
from starward.core.hipparcos_types import HIPStar

results = find_by_name("orion")

for obj in results:
    if isinstance(obj, HIPStar):
        print(f"Star: {obj.name} ({obj.spectral_type})")
    elif isinstance(obj, MessierObject):
        print(f"Messier: M{obj.number} - {obj.name}")
    elif isinstance(obj, NGCObject):
        print(f"NGC: NGC {obj.number} - {obj.name}")
    else:
        print(f"Object: {obj}")
```

Or use duck typing:

```python
for obj in results:
    # All objects have these
    print(f"Constellation: {obj.constellation}")
    print(f"Magnitude: {obj.magnitude}")

    # Stars have spectral_type
    if hasattr(obj, 'spectral_type'):
        print(f"Spectral: {obj.spectral_type}")

    # Deep-sky have object_type
    if hasattr(obj, 'object_type'):
        print(f"Type: {obj.object_type}")
```

---

## Example: Tonight's Best Objects

```python
from starward.core.finder import find_bright, find_in_constellation
from starward.core.observer import Observer
from starward.core.time import jd_now
from starward.core.messier import messier_altitude
from starward.core.ngc import ngc_altitude
from starward.core.hipparcos import star_altitude

observer = Observer.from_degrees("Home", 40.7, -74.0)
jd = jd_now()

# Find bright objects
objects = find_bright(max_magnitude=6.0)

# Filter to those above 30°
visible = []
for obj in objects:
    # Get altitude based on catalog type
    if hasattr(obj, 'hip_number'):
        alt = star_altitude(obj.hip_number, observer, jd)
    elif hasattr(obj, 'number'):
        if hasattr(obj, 'ngc'):  # Messier
            alt = messier_altitude(obj.number, observer, jd)
        else:  # NGC
            alt = ngc_altitude(obj.number, observer, jd)

    if alt.degrees > 30:
        visible.append((obj, alt.degrees))

# Sort by altitude
visible.sort(key=lambda x: x[1], reverse=True)

print("Best objects tonight:")
for obj, alt in visible[:10]:
    name = getattr(obj, 'name', f"Object {obj.number}")
    print(f"  {name}: {alt:.0f}° altitude")
```

---

## See Also

- [Catalog Modules](/docs/module-guides/catalogs) — Individual catalog documentation
- [Lists Module](/docs/module-guides/lists) — Save found objects to lists
- [Visibility Module](/docs/module-guides/visibility) — Detailed visibility calculations
