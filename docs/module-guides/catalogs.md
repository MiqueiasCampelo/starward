---
id: catalogs
title: Catalog Modules
sidebar_label: Catalogs
sidebar_position: 10
description: Python API for deep-sky and star catalogs including Messier, NGC, IC, Caldwell, and Hipparcos.
---

# Catalog Modules

starward provides Python access to major astronomical catalogs for deep-sky objects and bright stars.

## Available Catalogs

| Module | Catalog | Objects | Description |
|--------|---------|---------|-------------|
| `messier` | Messier | 110 | Classic deep-sky catalog |
| `ngc` | NGC | ~7,840 | New General Catalogue |
| `ic` | IC | ~5,386 | Index Catalogue |
| `caldwell` | Caldwell | 109 | Patrick Moore's catalog |
| `hipparcos` | Hipparcos | ~9,100 | Bright star catalog |

## Common Interface

All catalog modules share a consistent interface:

```python
# Singleton instance
CATALOG.get(number)           # Get object by number
CATALOG.list_all()            # List all objects
CATALOG.search(query)         # Search by text
CATALOG.filter_by_type(type)  # Filter by object type
CATALOG.filter_by_constellation(code)  # Filter by constellation
CATALOG.filter_by_magnitude(max_mag)   # Filter by brightness
CATALOG.stats()               # Catalog statistics

# Coordinate functions
catalog_coords(number)        # Get ICRSCoord
catalog_altitude(number, observer, jd)  # Current altitude
catalog_transit_altitude(number, observer)  # Transit altitude
```

---

## Messier Catalog

The 110 Messier objects—the finest deep-sky objects visible from mid-northern latitudes.

### Basic Usage

```python
from starward.core.messier import MESSIER, messier_coords

# Get the Andromeda Galaxy
m31 = MESSIER.get(31)
print(f"{m31.name}: {m31.object_type}")
print(f"Magnitude: {m31.magnitude}")
print(f"Constellation: {m31.constellation}")

# Get coordinates
coords = messier_coords(31)
print(f"RA: {coords.ra.hours:.4f}h")
print(f"Dec: {coords.dec.degrees:.4f}°")
```

### MessierObject Properties

| Property | Type | Description |
|----------|------|-------------|
| `number` | int | Messier number (1-110) |
| `name` | str | Common name |
| `object_type` | str | Type (galaxy, nebula, cluster, etc.) |
| `constellation` | str | IAU 3-letter code |
| `ra_hours` | float | Right ascension in hours |
| `dec_degrees` | float | Declination in degrees |
| `magnitude` | float | Visual magnitude |
| `size_arcmin` | float | Angular size in arcminutes |
| `distance_kly` | float | Distance in thousands of light-years |
| `ngc` | int | NGC catalog number |

### Searching and Filtering

```python
from starward.core.messier import MESSIER

# Search by name or description
results = MESSIER.search("orion")
results = MESSIER.search("ring nebula")

# Filter by type
galaxies = MESSIER.filter_by_type("galaxy")
globulars = MESSIER.filter_by_type("globular_cluster")
planetaries = MESSIER.filter_by_type("planetary_nebula")

# Filter by constellation
sgr_objects = MESSIER.filter_by_constellation("Sgr")

# Filter by brightness
naked_eye = MESSIER.filter_by_magnitude(6.0)
binocular = MESSIER.filter_by_magnitude(8.0)
```

### Visibility Calculations

```python
from starward.core.messier import messier_altitude, messier_transit_altitude
from starward.core.observer import Observer
from starward.core.time import jd_now

observer = Observer.from_degrees("Home", 40.7, -74.0)
jd = jd_now()

# Current altitude
alt = messier_altitude(31, observer, jd)
print(f"M31 altitude: {alt.degrees:.1f}°")

# Maximum altitude (at transit)
transit_alt = messier_transit_altitude(31, observer)
print(f"M31 transit altitude: {transit_alt.degrees:.1f}°")
```

---

## NGC Catalog

The New General Catalogue—the primary professional deep-sky reference.

### Basic Usage

```python
from starward.core.ngc import NGC, ngc_coords

# Get the North America Nebula
ngc7000 = NGC.get(7000)
print(f"{ngc7000.name}: {ngc7000.object_type}")

# Get M31 by NGC number
ngc224 = NGC.get(224)
print(f"NGC 224 is {ngc224.name}")

# Cross-reference Messier
m31_ngc = NGC.get_by_messier(31)
print(f"M31 = NGC {m31_ngc.number}")
```

### NGCObject Properties

| Property | Type | Description |
|----------|------|-------------|
| `number` | int | NGC number |
| `name` | str | Common name (if any) |
| `object_type` | str | Object type |
| `constellation` | str | IAU 3-letter code |
| `ra_hours` | float | Right ascension |
| `dec_degrees` | float | Declination |
| `magnitude` | float | Visual magnitude |
| `size_arcmin` | float | Angular size |
| `messier_number` | int | Messier number (if applicable) |

### Statistics

```python
from starward.core.ngc import NGC

stats = NGC.stats()
print(f"Total objects: {stats['total']}")
print(f"By type: {stats['by_type']}")
```

---

## IC Catalog

The Index Catalogue—a supplement to the NGC.

### Basic Usage

```python
from starward.core.ic import IC, ic_coords

# Get the Horsehead Nebula
ic434 = IC.get(434)
print(f"{ic434.name}: {ic434.object_type}")

# Famous IC objects
ic1805 = IC.get(1805)  # Heart Nebula
ic1848 = IC.get(1848)  # Soul Nebula
```

The IC module has the same interface as NGC.

---

## Caldwell Catalog

Sir Patrick Moore's 109 deep-sky objects not in the Messier catalog.

### Basic Usage

```python
from starward.core.caldwell import Caldwell, caldwell_coords

# Get the Double Cluster
c14 = Caldwell.get(14)
print(f"{c14.name}: NGC {c14.ngc_number}")

# Get the Sculptor Galaxy
c65 = Caldwell.get(65)
print(f"{c65.name} in {c65.constellation}")
```

### CaldwellObject Properties

| Property | Type | Description |
|----------|------|-------------|
| `number` | int | Caldwell number (1-109) |
| `name` | str | Common name |
| `object_type` | str | Object type |
| `constellation` | str | IAU 3-letter code |
| `ngc_number` | int | NGC cross-reference |
| `magnitude` | float | Visual magnitude |

---

## Hipparcos Star Catalog

Bright stars with precise astrometric data from ESA's Hipparcos satellite.

### Basic Usage

```python
from starward.core.hipparcos import Hipparcos, star_coords

# Get Sirius
sirius = Hipparcos.get(32349)
print(f"{sirius.name}: {sirius.spectral_type}")
print(f"Magnitude: {sirius.magnitude}")
print(f"Distance: {sirius.parallax_mas} mas")

# Find by name
vega = Hipparcos.get_by_name("Vega")
polaris = Hipparcos.get_by_name("Polaris")

# Find by Bayer designation
betelgeuse = Hipparcos.get_by_bayer("Alpha Orionis")
```

### HIPStar Properties

| Property | Type | Description |
|----------|------|-------------|
| `hip_number` | int | Hipparcos catalog number |
| `name` | str | Common name |
| `bayer` | str | Bayer designation (e.g., "Alpha Lyrae") |
| `constellation` | str | IAU 3-letter code |
| `ra_hours` | float | Right ascension |
| `dec_degrees` | float | Declination |
| `magnitude` | float | Visual magnitude |
| `spectral_type` | str | Full spectral type (e.g., "A0V") |
| `spectral_class` | str | Spectral class letter (e.g., "A") |
| `bv_color` | float | B-V color index |
| `parallax_mas` | float | Parallax in milliarcseconds |

### Filtering by Spectral Type

```python
from starward.core.hipparcos import Hipparcos

# Hot blue stars
b_stars = Hipparcos.filter_by_spectral_class("B")
a_stars = Hipparcos.filter_by_spectral_class("A")

# Cool red giants
k_giants = Hipparcos.filter_by_spectral_class("K")
m_giants = Hipparcos.filter_by_spectral_class("M")

# Named stars only
named = Hipparcos.filter_named()
```

---

## Object Types

### Deep-Sky Object Types

| Type | Description |
|------|-------------|
| `galaxy` | Spiral, elliptical, irregular galaxies |
| `globular_cluster` | Dense spherical star clusters |
| `open_cluster` | Loose stellar associations |
| `planetary_nebula` | Shells from dying stars |
| `emission_nebula` | Glowing gas clouds |
| `reflection_nebula` | Dust reflecting starlight |
| `dark_nebula` | Opaque dust clouds |
| `supernova_remnant` | Stellar explosion debris |
| `star_cloud` | Dense Milky Way regions |

### Spectral Classes

| Class | Color | Temperature | Examples |
|-------|-------|-------------|----------|
| O | Blue | >30,000 K | Very rare |
| B | Blue-white | 10,000-30,000 K | Rigel, Spica |
| A | White | 7,500-10,000 K | Vega, Sirius |
| F | Yellow-white | 6,000-7,500 K | Procyon |
| G | Yellow | 5,200-6,000 K | Sun |
| K | Orange | 3,700-5,200 K | Arcturus |
| M | Red | 2,400-3,700 K | Betelgeuse |

---

## Working with Coordinates

All catalog modules provide coordinate functions returning `ICRSCoord`:

```python
from starward.core.messier import messier_coords
from starward.core.ngc import ngc_coords
from starward.core.hipparcos import star_coords

# Get coordinates
m31_coords = messier_coords(31)
ngc7000_coords = ngc_coords(7000)
sirius_coords = star_coords(32349)

# Use with other calculations
from starward.core.angles import angular_separation

sep = angular_separation(
    m31_coords.ra, m31_coords.dec,
    sirius_coords.ra, sirius_coords.dec
)
print(f"Separation: {sep.degrees:.1f}°")
```

---

## Example: Building an Observing List

```python
from starward.core.messier import MESSIER, messier_altitude
from starward.core.observer import Observer
from starward.core.time import jd_now

observer = Observer.from_degrees("Home", 40.7, -74.0)
jd = jd_now()

# Find galaxies above 30° altitude
print("Galaxies visible tonight:")
for obj in MESSIER.filter_by_type("galaxy"):
    alt = messier_altitude(obj.number, observer, jd)
    if alt.degrees > 30:
        print(f"  M{obj.number}: {obj.name} ({alt.degrees:.0f}°)")
```

---

## See Also

- [Finder Module](/docs/module-guides/finder) — Cross-catalog search
- [Lists Module](/docs/module-guides/lists) — Observation list management
- [Visibility Module](/docs/module-guides/visibility) — Visibility calculations
