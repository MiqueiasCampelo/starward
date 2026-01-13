---
slug: planetary-motion
title: "astr0 v0.3.0: Planetary Motion"
authors: [oddur]
tags: [release]
---

The planets join astr0 in version 0.3.0. From Mercury's swift orbit to Neptune's distant path, you can now track all eight planets with the same educational transparency that defines astr0.

<!-- truncate -->

## The Planets Module

### Position Calculations

Get the current position of any planet in multiple coordinate systems:

```bash
astr0 planets position mars
astr0 planets position jupiter --verbose
```

With `--verbose`, you'll see the orbital elements, heliocentric coordinates, and the step-by-step transformation to geocentric positions.

### Visual Magnitude

Know how bright a planet will appear:

```bash
astr0 planets magnitude venus
astr0 planets magnitude saturn --observer "Home"
```

Magnitude calculations account for the planet's distance from both the Sun and Earth, plus phase angle effects for the inner planets.

### Elongation

Track a planet's angular distance from the Sun — essential for observation planning:

```bash
astr0 planets elongation mercury
astr0 planets elongation venus --verbose
```

Mercury and Venus are best observed at maximum elongation. astr0 tells you when.

### Rise, Set, and Transit

Plan your observing sessions:

```bash
astr0 planets rise saturn --observer "Home"
astr0 planets transit jupiter
astr0 planets set mars
```

### Opposition and Conjunction

Find the best times to observe:

```bash
astr0 planets opposition mars
astr0 planets conjunction venus
```

Opposition is when an outer planet is closest to Earth and visible all night. astr0 calculates the next occurrence.

## Documentation Migration

This release also marks the migration to Docusaurus for documentation. The new site features:

- Improved navigation and search
- Better code examples with syntax highlighting
- Mobile-friendly responsive design
- Module-by-module guides

## Example Session

```bash
# Set up your location
astr0 observer add "Backyard" --lat 34.0522 --lon -118.2437 --tz "America/Los_Angeles"

# What planets are visible tonight?
astr0 planets position jupiter --observer "Backyard"
astr0 planets rise saturn --observer "Backyard"

# When's the next Mars opposition?
astr0 planets opposition mars --verbose
```

## Getting Started

```bash
pip install astr0
```

Explore the [planets module guide](/docs/module-guides/planets) for complete documentation.

## What's Next

Future releases will explore asteroids, comets, and deep-sky object catalogs. The mission remains the same: astronomy calculations that teach while they compute.
