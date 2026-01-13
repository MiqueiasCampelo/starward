---
id: lists
title: Observation Lists
sidebar_label: Observation Lists
sidebar_position: 9
description: Create and manage custom observation lists for planning observing sessions.
---

# Observation Lists

The `list` command lets you create custom observation lists for planning your observing sessions. Add objects from any catalog, attach notes, and export your lists for use in the field.

## Overview

Observation lists help you:

- **Plan sessions** — Collect targets for tonight's observing
- **Organize projects** — Group objects by theme or goal
- **Track progress** — Keep notes on each object
- **Export data** — Generate CSV or JSON for other software

Lists are stored locally in a SQLite database and persist between sessions.

---

## list create

Create a new observation list.

```bash
starward list create NAME [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `NAME` | Name for the list (quoted if contains spaces) |

**Options:**

| Option | Description |
|--------|-------------|
| `-d`, `--description TEXT` | Optional description for the list |

**Examples:**

```bash
# Simple list
starward list create "Tonight"

# List with description
starward list create "Messier Marathon" -d "All 110 Messier objects in one night"

# Themed list
starward list create "Virgo Galaxies" -d "Galaxy cluster targets for spring"
```

---

## list ls

List all observation lists.

```bash
starward list ls
```

**Output:**

```
Observation Lists
────────────────────────────────────────
  Tonight              3 objects    Created: 2024-01-15
  Messier Marathon   110 objects    Created: 2024-01-10
  Virgo Galaxies      12 objects    Created: 2024-01-08
────────────────────────────────────────
```

---

## list add

Add an object to a list.

```bash
starward list add NAME OBJECT [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `NAME` | List name |
| `OBJECT` | Catalog designation (see formats below) |

**Supported Object Formats:**

| Format | Example | Catalog |
|--------|---------|---------|
| `M##` or `M ##` | `M31`, `M 31` | Messier |
| `NGC####` or `NGC ####` | `NGC7000`, `NGC 7000` | NGC |
| `IC###` or `IC ###` | `IC434`, `IC 434` | IC |
| `C##` or `Caldwell ##` | `C14`, `Caldwell 14` | Caldwell |
| `HIP#####` | `HIP32349` | Hipparcos |

**Options:**

| Option | Description |
|--------|-------------|
| `-n`, `--notes TEXT` | Notes about this object |

**Examples:**

```bash
# Add Messier objects
starward list add "Tonight" M31
starward list add "Tonight" M42 --notes "Best after midnight"

# Add NGC objects
starward list add "Tonight" NGC7000
starward list add "Tonight" "NGC 891" -n "Edge-on galaxy"

# Add IC objects
starward list add "Tonight" IC434 --notes "Need H-beta filter"

# Add Caldwell objects
starward list add "Tonight" C14
starward list add "Tonight" "Caldwell 65"

# Add stars
starward list add "Tonight" HIP32349 --notes "Sirius - check double"
```

---

## list show

Display the contents of an observation list.

```bash
starward list show NAME
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `NAME` | List name |

**Example:**

```bash
starward list show "Tonight"
```

**Output:**

```
Tonight
────────────────────────────────────────
  Description: Objects for tonight's session

  Objects:
  ┌────────────┬────────────────────┬────────────┬──────┬─────────────────────┐
  │ Designation│ Name               │ Type       │ Mag  │ Notes               │
  ├────────────┼────────────────────┼────────────┼──────┼─────────────────────┤
  │ M 31       │ Andromeda Galaxy   │ galaxy     │ 3.4  │                     │
  │ M 42       │ Orion Nebula       │ em. nebula │ 4.0  │ Best after midnight │
  │ NGC 7000   │ North America Neb. │ em. nebula │ 4.0  │                     │
  │ HIP 32349  │ Sirius             │ star       │ −1.5 │ Check double        │
  └────────────┴────────────────────┴────────────┴──────┴─────────────────────┘

  Total: 4 objects
────────────────────────────────────────
```

---

## list remove

Remove an object from a list.

```bash
starward list remove NAME OBJECT
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `NAME` | List name |
| `OBJECT` | Catalog designation to remove |

**Examples:**

```bash
starward list remove "Tonight" M31
starward list remove "Tonight" NGC7000
```

---

## list note

Update notes for an object in a list.

```bash
starward list note NAME OBJECT NOTE
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `NAME` | List name |
| `OBJECT` | Catalog designation |
| `NOTE` | New note text (use "" to clear) |

**Examples:**

```bash
# Add or update a note
starward list note "Tonight" M42 "Observed - excellent seeing"

# Clear a note
starward list note "Tonight" M42 ""
```

---

## list clear

Remove all objects from a list (keeps the list itself).

```bash
starward list clear NAME
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `NAME` | List name |

**Example:**

```bash
starward list clear "Tonight"
```

---

## list rename

Rename an observation list.

```bash
starward list rename OLD_NAME NEW_NAME
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `OLD_NAME` | Current list name |
| `NEW_NAME` | New list name |

**Example:**

```bash
starward list rename "Tonight" "January 15 Session"
```

---

## list delete

Permanently delete an observation list.

```bash
starward list delete NAME
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `NAME` | List name to delete |

**Example:**

```bash
starward list delete "Old Session"
```

---

## list export

Export a list to CSV or JSON format.

```bash
starward list export NAME [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `NAME` | List name |

**Options:**

| Option | Description |
|--------|-------------|
| `-f`, `--format FORMAT` | Export format: `csv` (default) or `json` |
| `-o`, `--output PATH` | Output file (default: stdout) |

**Examples:**

```bash
# Export to CSV (stdout)
starward list export "Tonight"

# Export to CSV file
starward list export "Tonight" -o tonight.csv

# Export to JSON
starward list export "Tonight" --format json

# Export to JSON file
starward list export "Tonight" -f json -o tonight.json
```

**CSV Output:**

```csv
designation,name,type,constellation,magnitude,ra_hours,dec_degrees,notes
M 31,Andromeda Galaxy,galaxy,And,3.4,0.7123,41.2692,
M 42,Orion Nebula,emission_nebula,Ori,4.0,5.5908,-5.3911,Best after midnight
NGC 7000,North America Nebula,emission_nebula,Cyg,4.0,20.9881,44.5289,
HIP 32349,Sirius,star,CMa,-1.46,6.7525,-16.7161,Check double
```

**JSON Output:**

```json
{
  "name": "Tonight",
  "description": "Objects for tonight's session",
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
    },
    {
      "designation": "M 42",
      "name": "Orion Nebula",
      "type": "emission_nebula",
      "constellation": "Ori",
      "magnitude": 4.0,
      "ra_hours": 5.5908,
      "dec_degrees": -5.3911,
      "notes": "Best after midnight"
    }
  ]
}
```

---

## Workflow Examples

### Planning an Observing Session

```bash
# Create a list for tonight
starward list create "Jan 15 Session" -d "New moon, clear skies forecast"

# Find interesting objects
starward find galaxies --mag 11 --constellation Vir

# Add selected targets
starward list add "Jan 15 Session" M87 --notes "Check jet"
starward list add "Jan 15 Session" NGC4472
starward list add "Jan 15 Session" NGC4649

# Add some variety
starward list add "Jan 15 Session" M42 --notes "Start of session warmup"
starward list add "Jan 15 Session" M1 --notes "Supernova remnant"

# Review the list
starward list show "Jan 15 Session"

# Export for mobile app
starward list export "Jan 15 Session" -f json -o session.json
```

### Messier Marathon Preparation

```bash
# Create the list
starward list create "Messier Marathon" -d "All 110 objects"

# Add all Messier objects (scripted)
for i in $(seq 1 110); do
  starward list add "Messier Marathon" "M$i"
done

# Export for reference
starward list export "Messier Marathon" -o marathon.csv
```

### Tracking Observations

```bash
# Before observing
starward list show "Tonight"

# After observing each object, update notes
starward list note "Tonight" M31 "Observed 21:30 - dust lanes visible"
starward list note "Tonight" M42 "Observed 22:15 - trapezium resolved"
starward list note "Tonight" NGC7000 "Skipped - too low"

# Review session
starward list show "Tonight"

# Keep as record
starward list rename "Tonight" "2024-01-15 Session"
```

---

## Tips

### Object Designations

The parser is flexible with spacing:
- `M31` and `M 31` both work
- `NGC7000` and `NGC 7000` both work
- `IC434` and `IC 434` both work

### Managing Multiple Sessions

```bash
# Create dated lists
starward list create "2024-01-15"
starward list create "2024-01-22"

# Or themed lists
starward list create "Galaxy Project"
starward list create "Double Stars"
starward list create "Planetary Nebulae"
```

### Integration with Other Tools

Export JSON for:
- Planetarium software import
- Custom observation logging apps
- Telescope control software
- Spreadsheet analysis

```bash
# Pipe to other commands
starward list export "Tonight" -f json | jq '.objects[].designation'
```

---

## See Also

- [Object Finder](/docs/cli-reference/finder) — Find objects to add to lists
- [Deep-Sky Catalogs](/docs/cli-reference/deep-sky) — Browse individual catalogs
- [Star Catalog](/docs/cli-reference/stars) — Browse stars

---

*Next: [Full CLI Reference](/docs/cli-reference/reference) — Complete command reference*
