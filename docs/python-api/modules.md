---
id: modules
title: Core Modules
sidebar_label: Core Modules
sidebar_position: 3
---

# Core Modules

Detailed documentation for starward's core calculation modules.

## starward.core.time

Julian Date and time conversions.

### JulianDate

```python
from starward.core.time import JulianDate, jd_now

# Current time
now = jd_now()

# From Julian Date number
jd = JulianDate(2451545.0)  # J2000.0

# Properties
jd.jd           # Julian Date as float
jd.mjd          # Modified Julian Date
jd.t_j2000      # Julian centuries since J2000.0
jd.to_datetime() # Convert to Python datetime
```

### Conversion Functions

```python
from starward.core.time import utc_to_jd, jd_to_utc
from datetime import datetime

jd = utc_to_jd(datetime(2024, 6, 21, 12, 0, 0))
dt = jd_to_utc(jd)
```

## starward.core.angles

Angular quantities and calculations.

### Angle

```python
from starward.core.angles import Angle

# Create from degrees
a = Angle(degrees=45.5)

# Create from radians
a = Angle(radians=0.7854)

# Properties
a.degrees    # As degrees
a.radians    # As radians
a.hours      # As hours (for RA)

# Formatting
a.format_dms()   # "+45° 30′ 00.00″"
a.format_hms()   # "3h 02m 00.00s"
a.to_dms()       # Human-readable DMS
a.to_hms()       # Human-readable HMS

# Normalization
a.normalize()    # Wrap to [0, 360)
```

### Angular Separation

```python
from starward.core.angles import angular_separation, position_angle

# Separation between two points
sep = angular_separation(ra1, dec1, ra2, dec2)

# Position angle
pa = position_angle(ra1, dec1, ra2, dec2)
```

## starward.core.coords

Coordinate systems and transformations.

### ICRSCoord

```python
from starward.core.coords import ICRSCoord

# Parse from string
coord = ICRSCoord.parse("18h36m56s +38d47m01s")

# From degrees
coord = ICRSCoord.from_degrees(ra=278.956, dec=38.784)

# Access components
coord.ra      # Angle
coord.dec     # Angle

# Transform
galactic = coord.to_galactic()
horizontal = coord.to_horizontal(jd, lat, lon)
```

### GalacticCoord

```python
from starward.core.coords import GalacticCoord

coord = GalacticCoord.from_degrees(l=120.0, b=30.0)
icrs = coord.to_icrs()
```

## starward.core.sun

Solar calculations.

```python
from starward.core.sun import (
    sun_position,
    sunrise, sunset, solar_noon,
    solar_altitude, day_length,
    civil_twilight, nautical_twilight, astronomical_twilight,
)

# Position
sun = sun_position()
sun.ra          # Right ascension
sun.dec         # Declination
sun.distance_au # Distance in AU

# Events (require Observer)
rise = sunrise(observer)
set_time = sunset(observer)
length = day_length(observer)
```

## starward.core.moon

Lunar calculations.

```python
from starward.core.moon import (
    moon_position,
    moon_phase, MoonPhase,
    moonrise, moonset,
    next_phase,
)

# Position
moon = moon_position()
moon.ra
moon.dec
moon.distance_km
moon.angular_diameter

# Phase
phase = moon_phase()
phase.phase_name       # MoonPhase enum
phase.illumination     # 0-1
phase.age_days         # Days since new moon

# Next full moon
full = next_phase(MoonPhase.FULL_MOON)
```

## starward.core.planets

Planetary calculations.

```python
from starward.core.planets import (
    Planet,
    planet_position,
    all_planet_positions,
    planet_rise, planet_set, planet_transit,
    planet_altitude,
)

# Position
pos = planet_position(Planet.JUPITER)
pos.ra
pos.dec
pos.distance_au      # From Earth
pos.helio_distance   # From Sun
pos.magnitude
pos.elongation
pos.phase_angle

# All planets
positions = all_planet_positions()

# Events
rise = planet_rise(Planet.MARS, observer)
```

## starward.core.observer

Observer location management.

```python
from starward.core.observer import Observer, get_observer

# Create observer
obs = Observer.from_degrees("NYC", latitude=40.7, longitude=-74.0)

# Properties
obs.latitude   # Angle
obs.longitude  # Angle
obs.lat_deg    # Degrees
obs.lon_deg    # Degrees

# Load saved observer
home = get_observer("home")
```

## starward.core.visibility

Visibility calculations for observing planning.

```python
from starward.core.visibility import (
    compute_visibility,
    airmass,
    target_altitude,
    transit_time,
)

# Comprehensive visibility
vis = compute_visibility(target_coord, observer, jd)
vis.current_altitude
vis.transit_time
vis.moon_separation

# Airmass
X = airmass(altitude)
```

---

## starward.core.messier

Messier deep-sky catalog (110 objects).

```python
from starward.core.messier import (
    MESSIER,           # Singleton catalog instance
    MessierCatalog,    # Catalog class
    messier_coords,    # Get coordinates
    messier_altitude,  # Current altitude
    messier_transit_altitude,  # Transit altitude
)

# Get an object
m31 = MESSIER.get(31)
m31.number          # 31
m31.name            # "Andromeda Galaxy"
m31.object_type     # "galaxy"
m31.constellation   # "And"
m31.ra_hours        # Right ascension in hours
m31.dec_degrees     # Declination in degrees
m31.magnitude       # Visual magnitude
m31.ngc             # NGC number (224)

# List all objects
all_objects = MESSIER.list_all()

# Search
results = MESSIER.search("orion")
results = MESSIER.search("galaxy", limit=10)

# Filter
galaxies = MESSIER.filter_by_type("galaxy")
sgr_objects = MESSIER.filter_by_constellation("Sgr")
bright = MESSIER.filter_by_magnitude(6.0)

# Coordinates
coords = messier_coords(31)  # Returns ICRSCoord

# Visibility
alt = messier_altitude(31, observer, jd)
transit = messier_transit_altitude(31, observer)
```

## starward.core.ngc

NGC deep-sky catalog (~7,840 objects).

```python
from starward.core.ngc import (
    NGC,               # Singleton catalog instance
    NGCCatalog,        # Catalog class
    ngc_coords,        # Get coordinates
    ngc_altitude,      # Current altitude
    ngc_transit_altitude,  # Transit altitude
)

# Get an object
ngc7000 = NGC.get(7000)
ngc7000.number          # 7000
ngc7000.name            # "North America Nebula"
ngc7000.object_type     # "emission_nebula"
ngc7000.constellation   # "Cyg"
ngc7000.magnitude       # Visual magnitude
ngc7000.messier_number  # Messier number if applicable

# List and filter
all_objects = NGC.list_all()
nebulae = NGC.filter_by_type("planetary_nebula")
virgo = NGC.filter_by_constellation("Vir")
bright = NGC.filter_by_magnitude(10.0)

# Search
results = NGC.search("veil nebula")

# Cross-reference
m31_ngc = NGC.get_by_messier(31)  # Returns NGC 224

# Statistics
stats = NGC.stats()
```

## starward.core.ic

IC (Index Catalogue) deep-sky catalog (~5,386 objects).

```python
from starward.core.ic import (
    IC,                # Singleton catalog instance
    ICCatalog,         # Catalog class
    ic_coords,         # Get coordinates
    ic_altitude,       # Current altitude
    ic_transit_altitude,  # Transit altitude
)

# Get an object
ic434 = IC.get(434)
ic434.name            # "Horsehead Nebula"
ic434.object_type     # "dark_nebula"

# Same interface as NGC
nebulae = IC.filter_by_type("emission_nebula")
results = IC.search("horsehead")
stats = IC.stats()
```

## starward.core.caldwell

Caldwell deep-sky catalog (109 objects).

```python
from starward.core.caldwell import (
    Caldwell,          # Singleton catalog instance
    CaldwellCatalog,   # Catalog class
    caldwell_coords,   # Get coordinates
    caldwell_altitude, # Current altitude
    caldwell_transit_altitude,  # Transit altitude
)

# Get an object
c14 = Caldwell.get(14)
c14.name              # "Double Cluster"
c14.ngc_number        # 869

# Same interface as other catalogs
galaxies = Caldwell.filter_by_type("galaxy")
results = Caldwell.search("sculptor")
stats = Caldwell.stats()
```

## starward.core.hipparcos

Hipparcos bright star catalog.

```python
from starward.core.hipparcos import (
    Hipparcos,         # Singleton catalog instance
    HipparcosCatalog,  # Catalog class
    star_coords,       # Get coordinates
    star_altitude,     # Current altitude
    star_transit_altitude,  # Transit altitude
)

# Get a star
sirius = Hipparcos.get(32349)
sirius.hip_number       # 32349
sirius.name             # "Sirius"
sirius.bayer            # "Alpha Canis Majoris"
sirius.constellation    # "CMa"
sirius.magnitude        # -1.46
sirius.spectral_type    # "A1V"
sirius.spectral_class   # "A"
sirius.bv_color         # B-V color index
sirius.parallax_mas     # Parallax in milliarcseconds

# Search
vega = Hipparcos.get_by_name("Vega")
betel = Hipparcos.get_by_bayer("Alpha Orionis")
results = Hipparcos.search("alpha")

# Filter
orion = Hipparcos.filter_by_constellation("Ori")
bright = Hipparcos.filter_by_magnitude(2.0)
red_giants = Hipparcos.filter_by_spectral_class("K")

# Statistics
stats = Hipparcos.stats()
```

## starward.core.finder

Cross-catalog object search.

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

# Search by name across all catalogs
results = find_by_name("orion")

# Find specific object types
galaxies = find_galaxies(max_magnitude=10.0, constellation="Vir")
nebulae = find_nebulae(max_magnitude=8.0)
clusters = find_clusters(constellation="Per")

# Find by type
planetary = find_by_type("planetary_nebula", max_magnitude=12.0)

# Find all objects in a constellation
orion_objects = find_in_constellation("Ori")

# Find bright objects (naked eye / binoculars)
bright = find_bright(max_magnitude=6.0)
```

## starward.core.lists

Custom observation list management.

```python
from starward.core.lists import (
    create_list,
    delete_list,
    list_all_lists,
    get_list,
    add_to_list,
    remove_from_list,
    update_notes,
    clear_list,
    rename_list,
    export_list,
    resolve_object,
)

# Create a list
create_list("Tonight", description="Objects for tonight")

# Add objects (various formats)
add_to_list("Tonight", "M31", notes="Check dust lanes")
add_to_list("Tonight", "NGC 7000")
add_to_list("Tonight", "IC434")
add_to_list("Tonight", "C14")
add_to_list("Tonight", "HIP32349")

# Get list contents
items = get_list("Tonight")
for item in items:
    print(f"{item.designation}: {item.name} - {item.notes}")

# Update notes
update_notes("Tonight", "M31", "Observed at 21:30")

# Remove an object
remove_from_list("Tonight", "IC434")

# Export
csv_data = export_list("Tonight", format="csv")
json_data = export_list("Tonight", format="json")

# List management
all_lists = list_all_lists()
rename_list("Tonight", "2024-01-15 Session")
clear_list("Tonight")  # Remove all items
delete_list("Tonight")  # Delete the list

# Resolve object designation
obj = resolve_object("M31")  # Returns MessierObject
obj = resolve_object("NGC7000")  # Returns NGCObject
obj = resolve_object("HIP32349")  # Returns HIPStar
```
