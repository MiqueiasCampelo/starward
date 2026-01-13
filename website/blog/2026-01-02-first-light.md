---
slug: first-light
title: "astr0 v0.1.0: First Light"
authors: [oddur]
tags: [release]
---

Today marks the first release of astr0, an educational astronomy calculation toolkit for Python. The name comes from the astronomical tradition of "first light" — the moment a new telescope captures its first image of the sky.

<!-- truncate -->

## Why astr0?

Most astronomy software treats calculations as black boxes. You put in a date and location, and out comes an answer. But for students learning celestial mechanics, amateur astronomers wanting to understand the sky, or anyone curious about how these calculations actually work — that opacity is a barrier.

astr0 is built differently. Every calculation can show its work with `--verbose` mode, revealing the step-by-step mathematics behind the results.

## What's in v0.1.0

### Time Module

The foundation of any astronomical calculation is time. astr0's time module handles:

- Julian Date conversions (the astronomer's universal time system)
- Modified Julian Date (MJD)
- Greenwich Mean Sidereal Time (GMST)
- Local Sidereal Time (LST)

```bash
astr0 time jd --verbose
```

### Coordinates Module

Transform between the major astronomical coordinate systems:

- ICRS (International Celestial Reference System)
- Galactic coordinates
- Horizontal (altitude/azimuth)

### Angles Module

Parse and format angles in standard astronomical notation:

- Degrees, minutes, seconds (DMS)
- Hours, minutes, seconds (HMS)
- Angular separation between points

## Getting Started

```bash
pip install astr0
```

Then try:

```bash
astr0 time now
astr0 coords parse "12h 30m 45s, +45° 15' 30\""
```

## What's Next

v0.2.0 will add the Sun and Moon modules, bringing rise/set times, twilight calculations, and lunar phases. The goal is to build a complete toolkit for observation planning — one that teaches while it computes.
