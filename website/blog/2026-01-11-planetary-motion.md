---
slug: planetary-motion
title: "starward v0.3.0: Planetary Motion"
authors: [oddur]
tags: [release]
---

The planets join starward in version 0.3.0. From Mercury's swift orbit to Neptune's distant path, you can now track all eight planets with the same educational transparency that defines starward.

<!-- truncate -->

## The Planets Module

### Position Calculations

Get the current position of any planet in multiple coordinate systems:

```bash
starward planets position mars
starward planets position jupiter --verbose
```

With `--verbose`, you'll see the orbital elements, heliocentric coordinates, and the step-by-step transformation to geocentric positions.

### Visual Magnitude

Know how bright a planet will appear:

```bash
starward planets magnitude venus
starward planets magnitude saturn --observer "Home"
```

Magnitude calculations account for the planet's distance from both the Sun and Earth, plus phase angle effects for the inner planets.

### Elongation

Track a planet's angular distance from the Sun — essential for observation planning:

```bash
starward planets elongation mercury
starward planets elongation venus --verbose
```

Mercury and Venus are best observed at maximum elongation. starward tells you when.

### Rise, Set, and Transit

Plan your observing sessions:

```bash
starward planets rise saturn --observer "Home"
starward planets transit jupiter
starward planets set mars
```

### Opposition and Conjunction

Find the best times to observe:

```bash
starward planets opposition mars
starward planets conjunction venus
```

Opposition is when an outer planet is closest to Earth and visible all night. starward calculates the next occurrence.

## Documentation Migration

This release also marks the migration to Docusaurus for documentation. The new site features:

- Improved navigation and search
- Better code examples with syntax highlighting
- Mobile-friendly responsive design
- Module-by-module guides

## Example Session

```bash
# Set up your location
starward observer add "Backyard" --lat 34.0522 --lon -118.2437 --tz "America/Los_Angeles"

# What planets are visible tonight?
starward planets position jupiter --observer "Backyard"
starward planets rise saturn --observer "Backyard"

# When's the next Mars opposition?
starward planets opposition mars --verbose
```

## Getting Started

```bash
pip install starward
```

Explore the [planets module guide](/docs/module-guides/planets) for complete documentation.

## What's Next

Future releases will explore asteroids, comets, and deep-sky object catalogs. The mission remains the same: astronomy calculations that teach while they compute.
