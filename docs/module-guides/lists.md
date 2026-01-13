---
id: lists
title: Lists Module
sidebar_label: Lists
sidebar_position: 12
description: Python API for creating and managing custom observation lists.
---

# Lists Module

The lists module provides functions for creating and managing custom observation lists, allowing you to collect objects from any catalog for observation planning.

## Overview

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
```

Lists are stored in a local SQLite database and persist between sessions.

---

## Creating Lists

### create_list

Create a new observation list.

```python
from starward.core.lists import create_list

# Simple list
create_list("Tonight")

# List with description
create_list(
    "Messier Marathon",
    description="All 110 Messier objects in one night"
)

# Themed list
create_list(
    "Virgo Galaxies",
    description="Galaxy cluster targets for spring observing"
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | List name (must be unique) |
| `description` | str | Optional description |

**Raises:** `ValueError` if list name already exists.

---

## Adding Objects

### add_to_list

Add an astronomical object to a list.

```python
from starward.core.lists import add_to_list

# Messier objects
add_to_list("Tonight", "M31")
add_to_list("Tonight", "M 42", notes="Best after midnight")

# NGC objects
add_to_list("Tonight", "NGC7000")
add_to_list("Tonight", "NGC 891", notes="Edge-on galaxy")

# IC objects
add_to_list("Tonight", "IC434", notes="Need H-beta filter")

# Caldwell objects
add_to_list("Tonight", "C14")
add_to_list("Tonight", "Caldwell 65")

# Hipparcos stars
add_to_list("Tonight", "HIP32349", notes="Sirius - check for Pup")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `list_name` | str | Name of the list |
| `designation` | str | Object designation (see formats below) |
| `notes` | str | Optional notes about the object |

**Supported Designation Formats:**

| Format | Examples | Catalog |
|--------|----------|---------|
| `M##` or `M ##` | `M31`, `M 31` | Messier |
| `NGC####` or `NGC ####` | `NGC7000`, `NGC 7000` | NGC |
| `IC###` or `IC ###` | `IC434`, `IC 434` | IC |
| `C##` or `Caldwell ##` | `C14`, `Caldwell 14` | Caldwell |
| `HIP#####` | `HIP32349` | Hipparcos |

**Raises:**
- `ValueError` if list doesn't exist
- `ValueError` if object designation can't be resolved
- `ValueError` if object already in list

---

## Retrieving Lists

### list_all_lists

Get all observation lists.

```python
from starward.core.lists import list_all_lists

lists = list_all_lists()

for lst in lists:
    print(f"{lst.name}: {lst.item_count} objects")
    if lst.description:
        print(f"  {lst.description}")
```

**Returns:** List of `ObservationList` objects with properties:
- `name`: List name
- `description`: Description (may be None)
- `item_count`: Number of objects
- `created_at`: Creation timestamp

### get_list

Get the contents of a specific list.

```python
from starward.core.lists import get_list

items = get_list("Tonight")

for item in items:
    print(f"{item.designation}: {item.name}")
    print(f"  Type: {item.object_type}")
    print(f"  Constellation: {item.constellation}")
    print(f"  Magnitude: {item.magnitude}")
    if item.notes:
        print(f"  Notes: {item.notes}")
```

**Returns:** List of `ListItem` objects with properties:

| Property | Type | Description |
|----------|------|-------------|
| `designation` | str | Catalog designation (e.g., "M 31") |
| `name` | str | Object name |
| `object_type` | str | Type (galaxy, star, etc.) |
| `constellation` | str | IAU 3-letter code |
| `magnitude` | float | Visual magnitude |
| `ra_hours` | float | Right ascension |
| `dec_degrees` | float | Declination |
| `notes` | str | User notes (may be None) |

---

## Modifying Lists

### remove_from_list

Remove an object from a list.

```python
from starward.core.lists import remove_from_list

remove_from_list("Tonight", "M31")
remove_from_list("Tonight", "NGC7000")
```

### update_notes

Update notes for an object in a list.

```python
from starward.core.lists import update_notes

# Add or update notes
update_notes("Tonight", "M42", "Observed 22:15 - excellent seeing")

# Clear notes
update_notes("Tonight", "M42", "")
```

### clear_list

Remove all objects from a list (keeps the list itself).

```python
from starward.core.lists import clear_list

clear_list("Tonight")
```

### rename_list

Rename an observation list.

```python
from starward.core.lists import rename_list

rename_list("Tonight", "2024-01-15 Session")
```

### delete_list

Permanently delete an observation list.

```python
from starward.core.lists import delete_list

delete_list("Old Session")
```

---

## Exporting Lists

### export_list

Export a list to CSV or JSON format.

```python
from starward.core.lists import export_list

# Export to CSV string
csv_data = export_list("Tonight", format="csv")
print(csv_data)

# Export to JSON string
json_data = export_list("Tonight", format="json")
print(json_data)

# Write to file
with open("tonight.csv", "w") as f:
    f.write(export_list("Tonight", format="csv"))

with open("tonight.json", "w") as f:
    f.write(export_list("Tonight", format="json"))
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `list_name` | str | Name of the list |
| `format` | str | Export format: "csv" or "json" |

**CSV Output:**

```csv
designation,name,type,constellation,magnitude,ra_hours,dec_degrees,notes
M 31,Andromeda Galaxy,galaxy,And,3.4,0.7123,41.2692,
M 42,Orion Nebula,emission_nebula,Ori,4.0,5.5908,-5.3911,Best after midnight
```

**JSON Output:**

```json
{
  "name": "Tonight",
  "description": "Objects for tonight",
  "created": "2024-01-15T18:30:00Z",
  "objects": [
    {
      "designation": "M 31",
      "name": "Andromeda Galaxy",
      "type": "galaxy",
      "constellation": "And",
      "magnitude": 3.4,
      "ra_hours": 0.7123,
      "dec_degrees": 41.2692,
      "notes": null
    }
  ]
}
```

---

## Resolving Objects

### resolve_object

Resolve a designation string to a catalog object.

```python
from starward.core.lists import resolve_object

# Returns the actual catalog object
m31 = resolve_object("M31")
print(f"Name: {m31.name}")
print(f"Type: {m31.object_type}")

ngc7000 = resolve_object("NGC7000")
sirius = resolve_object("HIP32349")
```

**Returns:** The catalog object (MessierObject, NGCObject, ICObject, CaldwellObject, or HIPStar).

**Raises:** `ValueError` if designation can't be resolved.

---

## Example: Complete Workflow

```python
from starward.core.lists import (
    create_list, add_to_list, get_list,
    update_notes, export_list
)
from starward.core.finder import find_galaxies

# Create a new list
create_list("Virgo Cluster", description="Spring galaxy hunting")

# Find bright Virgo galaxies
galaxies = find_galaxies(max_magnitude=11.0, constellation="Vir")

# Add top 10 to list
for g in galaxies[:10]:
    if hasattr(g, 'messier_number') and g.messier_number:
        designation = f"M{g.messier_number}"
    else:
        designation = f"NGC{g.number}"
    add_to_list("Virgo Cluster", designation)

# Review the list
items = get_list("Virgo Cluster")
print(f"Added {len(items)} galaxies:")
for item in items:
    print(f"  {item.designation}: {item.name} (mag {item.magnitude})")

# After observing, update notes
update_notes("Virgo Cluster", "M87", "Jet visible in 12\" scope")
update_notes("Virgo Cluster", "NGC4472", "Large, bright core")

# Export for records
with open("virgo_session.json", "w") as f:
    f.write(export_list("Virgo Cluster", format="json"))
```

---

## Example: Building a Messier Marathon List

```python
from starward.core.lists import create_list, add_to_list
from starward.core.messier import MESSIER

# Create the list
create_list("Messier Marathon", description="All 110 objects")

# Add all Messier objects
for obj in MESSIER.list_all():
    add_to_list("Messier Marathon", f"M{obj.number}")

print("Added all 110 Messier objects to list")
```

---

## Example: Session Tracking

```python
from starward.core.lists import (
    create_list, add_to_list, update_notes,
    rename_list, get_list
)
from datetime import datetime

# Create tonight's list
date_str = datetime.now().strftime("%Y-%m-%d")
create_list("Tonight", description=f"Session {date_str}")

# Add targets
add_to_list("Tonight", "M31")
add_to_list("Tonight", "M33")
add_to_list("Tonight", "NGC891")

# During observation, update notes
update_notes("Tonight", "M31", "21:30 - dust lanes visible, 3 companions")
update_notes("Tonight", "M33", "22:00 - faint, needed averted vision")
update_notes("Tonight", "NGC891", "Skipped - too low")

# End of session - rename for records
rename_list("Tonight", f"Session {date_str}")

# Review
items = get_list(f"Session {date_str}")
observed = [i for i in items if i.notes and "Skipped" not in i.notes]
print(f"Observed {len(observed)} of {len(items)} targets")
```

---

## Error Handling

```python
from starward.core.lists import create_list, add_to_list, get_list

try:
    create_list("Tonight")
except ValueError as e:
    print(f"List already exists: {e}")

try:
    add_to_list("Tonight", "INVALID123")
except ValueError as e:
    print(f"Invalid designation: {e}")

try:
    items = get_list("Nonexistent")
except ValueError as e:
    print(f"List not found: {e}")
```

---

## See Also

- [Finder Module](/docs/module-guides/finder) — Find objects to add to lists
- [Catalog Modules](/docs/module-guides/catalogs) — Browse individual catalogs
- [CLI Lists Reference](/docs/cli-reference/lists) — Command-line interface
