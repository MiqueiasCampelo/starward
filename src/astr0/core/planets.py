"""
Planetary position calculations.

Implements planetary positions using algorithms from Meeus, "Astronomical Algorithms".
Provides geocentric positions for Mercury through Neptune.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Tuple

from astr0.core.angles import Angle, angular_separation
from astr0.core.time import JulianDate, jd_now
from astr0.core.coords import ICRSCoord
from astr0.core.observer import Observer
from astr0.core.sun import sun_position, mean_obliquity, true_obliquity
from astr0.core.planets_data import (
    ORBITAL_ELEMENTS,
    MAGNITUDE_PARAMS,
    ANGULAR_DIAMETER_1AU,
)
from astr0.verbose import VerboseContext, step


class Planet(Enum):
    """Solar system planets."""
    MERCURY = "Mercury"
    VENUS = "Venus"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "Uranus"
    NEPTUNE = "Neptune"


# Planet symbols for display
PLANET_SYMBOLS: Dict[Planet, str] = {
    Planet.MERCURY: "☿",
    Planet.VENUS: "♀",
    Planet.MARS: "♂",
    Planet.JUPITER: "♃",
    Planet.SATURN: "♄",
    Planet.URANUS: "⛢",
    Planet.NEPTUNE: "♆",
}


@dataclass(frozen=True)
class PlanetPosition:
    """Planetary position at a given instant."""

    # Planet identity
    planet: Planet

    # Heliocentric ecliptic coordinates
    helio_longitude: Angle  # Heliocentric ecliptic longitude
    helio_latitude: Angle   # Heliocentric ecliptic latitude
    helio_distance: float   # Distance from Sun in AU

    # Geocentric equatorial coordinates (what observers usually want)
    ra: Angle               # Right Ascension
    dec: Angle              # Declination

    # Distance from Earth
    distance_au: float      # Distance in AU

    # Visual properties
    magnitude: float        # Apparent visual magnitude
    elongation: Angle       # Angular distance from Sun
    phase_angle: Angle      # Sun-Planet-Earth angle

    # Angular size
    angular_diameter: Angle  # Apparent angular diameter

    def to_icrs(self) -> ICRSCoord:
        """Convert to ICRS coordinate."""
        return ICRSCoord(ra=self.ra, dec=self.dec)

    @property
    def symbol(self) -> str:
        """Return the astronomical symbol for this planet."""
        return PLANET_SYMBOLS.get(self.planet, "?")

    @property
    def illumination(self) -> float:
        """Return the illuminated fraction (0-1)."""
        # Phase angle 0 = full, 180 = new
        return (1 + math.cos(self.phase_angle.radians)) / 2


def _normalize_angle(degrees: float) -> float:
    """Normalize angle to [0, 360) range."""
    result = degrees % 360.0
    if result < 0:
        result += 360.0
    return result


def _heliocentric_position(
    planet: Planet,
    jd: JulianDate,
    verbose: Optional[VerboseContext] = None
) -> Tuple[Angle, Angle, float]:
    """
    Calculate heliocentric ecliptic coordinates.

    Uses mean orbital elements from Meeus Table 31.a with
    time-dependent variations.

    Args:
        planet: Planet to calculate
        jd: Julian Date
        verbose: Optional verbose context

    Returns:
        Tuple of (longitude, latitude, distance in AU)
    """
    T = jd.t_j2000  # Julian centuries since J2000.0

    # Get orbital elements
    name = planet.value.lower()
    elem = ORBITAL_ELEMENTS[name]

    # Calculate current orbital elements
    a = elem.a0 + elem.a_rate * T
    e = elem.e0 + elem.e_rate * T
    i = elem.i0 + elem.i_rate * T
    omega = elem.omega0 + elem.omega_rate * T  # Longitude of ascending node
    pi = elem.pi0 + elem.pi_rate * T           # Longitude of perihelion
    L = elem.L0 + elem.L_rate * T              # Mean longitude

    # Mean anomaly
    M = _normalize_angle(L - pi)

    step(verbose, f"Orbital elements for {planet.value}",
         f"T = {T:.10f} centuries since J2000.0\n"
         f"a = {a:.9f} AU\n"
         f"e = {e:.9f}\n"
         f"i = {i:.6f}°\n"
         f"Ω = {omega:.6f}°\n"
         f"ϖ = {pi:.6f}°\n"
         f"L = {_normalize_angle(L):.6f}°\n"
         f"M = {M:.6f}°")

    # Solve Kepler's equation: E - e*sin(E) = M
    # Using Newton-Raphson iteration
    M_rad = math.radians(M)
    E = M_rad  # Initial guess

    for _ in range(10):
        E_new = E + (M_rad - E + e * math.sin(E)) / (1 - e * math.cos(E))
        if abs(E_new - E) < 1e-12:
            break
        E = E_new

    step(verbose, "Kepler's equation",
         f"M = {M:.6f}° = {M_rad:.9f} rad\n"
         f"E = {math.degrees(E):.6f}° (eccentric anomaly)")

    # True anomaly
    v = 2 * math.atan2(
        math.sqrt(1 + e) * math.sin(E / 2),
        math.sqrt(1 - e) * math.cos(E / 2)
    )
    v_deg = math.degrees(v)

    # Distance from Sun
    r = a * (1 - e * math.cos(E))

    step(verbose, "Position in orbit",
         f"v = {v_deg:.6f}° (true anomaly)\n"
         f"r = {r:.9f} AU")

    # Heliocentric ecliptic coordinates
    # Argument of perihelion
    omega_small = pi - omega  # ω = ϖ - Ω

    omega_rad = math.radians(omega)
    omega_small_rad = math.radians(omega_small)
    i_rad = math.radians(i)

    # Position in orbital plane
    x_orbit = r * math.cos(v)
    y_orbit = r * math.sin(v)

    # Rotate to ecliptic frame
    cos_omega = math.cos(omega_rad)
    sin_omega = math.sin(omega_rad)
    cos_i = math.cos(i_rad)
    sin_i = math.sin(i_rad)
    cos_w = math.cos(omega_small_rad)
    sin_w = math.sin(omega_small_rad)

    # Heliocentric ecliptic rectangular coordinates
    x_ecl = (cos_omega * cos_w - sin_omega * sin_w * cos_i) * x_orbit + \
            (-cos_omega * sin_w - sin_omega * cos_w * cos_i) * y_orbit

    y_ecl = (sin_omega * cos_w + cos_omega * sin_w * cos_i) * x_orbit + \
            (-sin_omega * sin_w + cos_omega * cos_w * cos_i) * y_orbit

    z_ecl = (sin_w * sin_i) * x_orbit + (cos_w * sin_i) * y_orbit

    # Convert to spherical
    lon = math.degrees(math.atan2(y_ecl, x_ecl))
    lat = math.degrees(math.asin(z_ecl / r))

    lon = _normalize_angle(lon)

    step(verbose, "Heliocentric ecliptic coordinates",
         f"x = {x_ecl:.9f} AU\n"
         f"y = {y_ecl:.9f} AU\n"
         f"z = {z_ecl:.9f} AU\n"
         f"λ = {lon:.6f}°\n"
         f"β = {lat:.6f}°\n"
         f"r = {r:.9f} AU")

    return Angle(degrees=lon), Angle(degrees=lat), r


def _earth_heliocentric(
    jd: JulianDate,
    verbose: Optional[VerboseContext] = None
) -> Tuple[float, float, float]:
    """
    Calculate Earth's heliocentric position.

    Returns rectangular ecliptic coordinates (x, y, z) in AU.
    """
    T = jd.t_j2000
    elem = ORBITAL_ELEMENTS["earth"]

    # Calculate current orbital elements
    a = elem.a0 + elem.a_rate * T
    e = elem.e0 + elem.e_rate * T
    pi = elem.pi0 + elem.pi_rate * T
    L = elem.L0 + elem.L_rate * T

    M = _normalize_angle(L - pi)
    M_rad = math.radians(M)

    # Solve Kepler's equation
    E = M_rad
    for _ in range(10):
        E_new = E + (M_rad - E + e * math.sin(E)) / (1 - e * math.cos(E))
        if abs(E_new - E) < 1e-12:
            break
        E = E_new

    # True anomaly and distance
    v = 2 * math.atan2(
        math.sqrt(1 + e) * math.sin(E / 2),
        math.sqrt(1 - e) * math.cos(E / 2)
    )
    r = a * (1 - e * math.cos(E))

    # Earth's ecliptic longitude (heliocentric)
    earth_lon = v + math.radians(pi)

    # Rectangular coordinates (Earth in ecliptic plane, so z ≈ 0)
    x = r * math.cos(earth_lon)
    y = r * math.sin(earth_lon)
    z = 0.0  # Earth defines the ecliptic plane

    step(verbose, "Earth heliocentric position",
         f"L = {_normalize_angle(L):.6f}°\n"
         f"r = {r:.9f} AU\n"
         f"x = {x:.9f}, y = {y:.9f}, z = {z:.9f} AU")

    return x, y, z


def _heliocentric_to_geocentric(
    planet_lon: Angle,
    planet_lat: Angle,
    planet_r: float,
    earth_x: float,
    earth_y: float,
    earth_z: float,
    verbose: Optional[VerboseContext] = None
) -> Tuple[Angle, Angle, float]:
    """
    Convert heliocentric to geocentric ecliptic coordinates.

    Args:
        planet_lon: Heliocentric ecliptic longitude
        planet_lat: Heliocentric ecliptic latitude
        planet_r: Heliocentric distance (AU)
        earth_x, earth_y, earth_z: Earth's heliocentric rectangular coords

    Returns:
        Tuple of (geocentric longitude, latitude, distance)
    """
    # Planet rectangular heliocentric coordinates
    lon_rad = planet_lon.radians
    lat_rad = planet_lat.radians

    x_p = planet_r * math.cos(lat_rad) * math.cos(lon_rad)
    y_p = planet_r * math.cos(lat_rad) * math.sin(lon_rad)
    z_p = planet_r * math.sin(lat_rad)

    # Geocentric rectangular (planet - earth)
    x_g = x_p - earth_x
    y_g = y_p - earth_y
    z_g = z_p - earth_z

    # Convert to spherical
    delta = math.sqrt(x_g**2 + y_g**2 + z_g**2)
    geo_lon = math.degrees(math.atan2(y_g, x_g))
    geo_lat = math.degrees(math.asin(z_g / delta))

    geo_lon = _normalize_angle(geo_lon)

    step(verbose, "Geocentric conversion",
         f"Planet heliocentric: x={x_p:.6f}, y={y_p:.6f}, z={z_p:.6f}\n"
         f"Geocentric: x={x_g:.6f}, y={y_g:.6f}, z={z_g:.6f}\n"
         f"λ_geo = {geo_lon:.6f}°\n"
         f"β_geo = {geo_lat:.6f}°\n"
         f"Δ = {delta:.9f} AU")

    return Angle(degrees=geo_lon), Angle(degrees=geo_lat), delta


def _ecliptic_to_equatorial(
    lon: Angle,
    lat: Angle,
    obliquity: Angle,
    verbose: Optional[VerboseContext] = None
) -> Tuple[Angle, Angle]:
    """
    Convert ecliptic coordinates to equatorial (RA/Dec).

    Args:
        lon: Ecliptic longitude
        lat: Ecliptic latitude
        obliquity: Obliquity of the ecliptic

    Returns:
        Tuple of (right ascension, declination)
    """
    lon_rad = lon.radians
    lat_rad = lat.radians
    eps_rad = obliquity.radians

    # Right ascension
    ra_rad = math.atan2(
        math.sin(lon_rad) * math.cos(eps_rad) - math.tan(lat_rad) * math.sin(eps_rad),
        math.cos(lon_rad)
    )

    # Declination
    dec_rad = math.asin(
        math.sin(lat_rad) * math.cos(eps_rad) +
        math.cos(lat_rad) * math.sin(eps_rad) * math.sin(lon_rad)
    )

    ra = Angle(radians=ra_rad).normalize()
    dec = Angle(radians=dec_rad)

    step(verbose, "Ecliptic to equatorial",
         f"ε = {obliquity.degrees:.6f}°\n"
         f"α = {ra.to_hms()}\n"
         f"δ = {dec.to_dms()}")

    return ra, dec


def _apparent_magnitude(
    planet: Planet,
    distance_au: float,
    sun_distance_au: float,
    phase_angle: Angle
) -> float:
    """
    Calculate apparent visual magnitude.

    Uses magnitude parameters from Meeus Ch. 41.
    """
    name = planet.value.lower()
    params = MAGNITUDE_PARAMS[name]

    # Phase angle in degrees
    i = phase_angle.degrees

    # Distance factor: 5 * log10(r * delta)
    dist_factor = 5 * math.log10(sun_distance_au * distance_au)

    # Phase correction
    phase_correction = params.phase_coeff1 * i + params.phase_coeff2 * i * i

    magnitude = params.V0 + dist_factor + phase_correction

    return magnitude


def _calculate_phase_angle(
    planet_helio_r: float,
    earth_sun_r: float,
    planet_earth_delta: float
) -> Angle:
    """
    Calculate the phase angle (Sun-Planet-Earth angle).

    Uses the law of cosines in the Sun-Planet-Earth triangle.
    """
    # Law of cosines: cos(i) = (r² + Δ² - R²) / (2rΔ)
    # where r = planet-sun, Δ = planet-earth, R = earth-sun
    r = planet_helio_r
    delta = planet_earth_delta
    R = earth_sun_r

    cos_i = (r**2 + delta**2 - R**2) / (2 * r * delta)

    # Clamp to [-1, 1] for numerical stability
    cos_i = max(-1.0, min(1.0, cos_i))

    phase_angle = math.degrees(math.acos(cos_i))
    return Angle(degrees=phase_angle)


def planet_position(
    planet: Planet,
    jd: Optional[JulianDate] = None,
    verbose: Optional[VerboseContext] = None
) -> PlanetPosition:
    """
    Calculate the geocentric position of a planet.

    Args:
        planet: Planet to calculate
        jd: Julian Date (default: now)
        verbose: Optional verbose context

    Returns:
        PlanetPosition with all planetary parameters
    """
    if jd is None:
        jd = jd_now()

    step(verbose, f"{planet.value} position calculation",
         f"JD = {jd.jd:.6f}\n"
         f"T = {jd.t_j2000:.10f} centuries since J2000.0")

    # Get heliocentric position of planet
    helio_lon, helio_lat, helio_r = _heliocentric_position(planet, jd, verbose)

    # Get Earth's heliocentric position
    earth_x, earth_y, earth_z = _earth_heliocentric(jd, verbose)
    earth_r = math.sqrt(earth_x**2 + earth_y**2 + earth_z**2)

    # Convert to geocentric
    geo_lon, geo_lat, delta = _heliocentric_to_geocentric(
        helio_lon, helio_lat, helio_r,
        earth_x, earth_y, earth_z,
        verbose
    )

    # Light-time correction (approximate - iterative would be more precise)
    light_time_days = delta * 0.0057755183  # AU to days (light travel time)
    step(verbose, "Light-time correction",
         f"Δ = {delta:.9f} AU\n"
         f"Light time = {light_time_days * 24 * 60:.2f} minutes")

    # Convert to equatorial coordinates
    obliquity = true_obliquity(jd, verbose)
    ra, dec = _ecliptic_to_equatorial(geo_lon, geo_lat, obliquity, verbose)

    # Calculate phase angle
    phase_angle = _calculate_phase_angle(helio_r, earth_r, delta)

    # Calculate elongation (angular distance from Sun)
    sun = sun_position(jd)
    elongation = angular_separation(ra, dec, sun.ra, sun.dec)

    step(verbose, "Physical ephemeris",
         f"Phase angle = {phase_angle.degrees:.2f}°\n"
         f"Elongation = {elongation.degrees:.2f}°")

    # Calculate apparent magnitude
    magnitude = _apparent_magnitude(planet, delta, helio_r, phase_angle)

    # Angular diameter
    name = planet.value.lower()
    base_diameter = ANGULAR_DIAMETER_1AU.get(name, 0)
    ang_diameter = Angle(degrees=base_diameter / delta / 3600)  # arcsec to degrees

    step(verbose, "Visual properties",
         f"Magnitude = {magnitude:+.2f}\n"
         f"Angular diameter = {ang_diameter.degrees * 3600:.2f}\"")

    return PlanetPosition(
        planet=planet,
        helio_longitude=helio_lon,
        helio_latitude=helio_lat,
        helio_distance=helio_r,
        ra=ra,
        dec=dec,
        distance_au=delta,
        magnitude=magnitude,
        elongation=elongation,
        phase_angle=phase_angle,
        angular_diameter=ang_diameter,
    )


def all_planet_positions(
    jd: Optional[JulianDate] = None,
    verbose: Optional[VerboseContext] = None
) -> Dict[Planet, PlanetPosition]:
    """
    Calculate positions of all planets.

    Args:
        jd: Julian Date (default: now)
        verbose: Optional verbose context

    Returns:
        Dict mapping Planet to PlanetPosition
    """
    if jd is None:
        jd = jd_now()

    return {p: planet_position(p, jd, verbose) for p in Planet}


def planet_altitude(
    planet: Planet,
    observer: Observer,
    jd: Optional[JulianDate] = None,
    verbose: Optional[VerboseContext] = None
) -> Angle:
    """
    Calculate the altitude of a planet for an observer.

    Args:
        planet: Planet to calculate
        observer: Observer location
        jd: Julian Date (default: now)
        verbose: Optional verbose context

    Returns:
        Altitude as Angle
    """
    if jd is None:
        jd = jd_now()

    pos = planet_position(planet, jd, verbose)
    coord = pos.to_icrs()

    horiz = coord.to_horizontal(
        jd,
        observer.latitude,
        observer.longitude,
        verbose
    )

    return horiz.alt


def _hour_angle_rise_set(
    dec: Angle,
    latitude: Angle,
    altitude: float,
    verbose: Optional[VerboseContext] = None
) -> Optional[Angle]:
    """
    Calculate the hour angle when an object is at a given altitude.
    """
    lat_rad = latitude.radians
    dec_rad = dec.radians
    alt_rad = math.radians(altitude)

    cos_H = (math.sin(alt_rad) - math.sin(lat_rad) * math.sin(dec_rad)) / (
        math.cos(lat_rad) * math.cos(dec_rad)
    )

    # Check if object never rises or never sets
    if cos_H < -1:
        return None  # Always above altitude (circumpolar)
    if cos_H > 1:
        return None  # Never reaches altitude

    H = math.degrees(math.acos(cos_H))
    return Angle(degrees=H)


def _planet_transit(
    planet: Planet,
    observer: Observer,
    jd: JulianDate,
    verbose: Optional[VerboseContext] = None
) -> JulianDate:
    """
    Calculate approximate transit time for a planet.
    """
    # Get integer JD at 0h UT
    jd0 = JulianDate(math.floor(jd.jd - 0.5) + 0.5)

    # Planet position
    pos = planet_position(planet, jd0)

    # Sidereal time at Greenwich at 0h UT
    # Approximate: transit when local sidereal time = RA
    # LST = GST + longitude
    # Transit fraction = (RA - GST - lon) / 360

    T = jd0.t_j2000
    # Greenwich Mean Sidereal Time at 0h UT (in degrees)
    GMST = 280.46061837 + 360.98564736629 * (jd0.jd - 2451545.0)
    GMST = _normalize_angle(GMST)

    # Transit time (fraction of day)
    transit_frac = (pos.ra.degrees - GMST - observer.lon_deg) / 360.0

    # Normalize to [0, 1)
    while transit_frac < 0:
        transit_frac += 1
    while transit_frac >= 1:
        transit_frac -= 1

    result = JulianDate(jd0.jd + transit_frac)

    step(verbose, f"{planet.value} transit",
         f"RA = {pos.ra.degrees:.4f}°\n"
         f"GMST = {GMST:.4f}°\n"
         f"Transit fraction = {transit_frac:.6f}\n"
         f"Transit JD = {result.jd:.6f}")

    return result


def planet_transit(
    planet: Planet,
    observer: Observer,
    jd: Optional[JulianDate] = None,
    verbose: Optional[VerboseContext] = None
) -> JulianDate:
    """
    Calculate the meridian transit time for a planet.

    Args:
        planet: Planet to calculate
        observer: Observer location
        jd: Julian Date (default: today)
        verbose: Optional verbose context

    Returns:
        JD of transit
    """
    if jd is None:
        jd = jd_now()

    return _planet_transit(planet, observer, jd, verbose)


def planet_rise(
    planet: Planet,
    observer: Observer,
    jd: Optional[JulianDate] = None,
    verbose: Optional[VerboseContext] = None
) -> Optional[JulianDate]:
    """
    Calculate the rise time for a planet.

    Args:
        planet: Planet to calculate
        observer: Observer location
        jd: Julian Date (default: today)
        verbose: Optional verbose context

    Returns:
        JD of rise, or None if planet doesn't rise
    """
    if jd is None:
        jd = jd_now()

    step(verbose, f"{planet.value} rise calculation",
         f"Observer: {observer.name}\n"
         f"Latitude: {observer.lat_deg:.4f}°")

    # Get transit time
    transit = _planet_transit(planet, observer, jd, verbose)

    # Planet position at transit
    pos = planet_position(planet, transit)

    # Hour angle at rise (standard altitude for stars/planets = -0.5667°)
    # This accounts for refraction
    rise_altitude = -0.5667
    H = _hour_angle_rise_set(pos.dec, observer.latitude, rise_altitude, verbose)

    if H is None:
        step(verbose, "Result", f"{planet.value} does not rise from this location")
        return None

    # Rise is transit minus hour angle
    H_days = H.degrees / 360
    result = JulianDate(transit.jd - H_days)

    step(verbose, f"{planet.value} rise result",
         f"Transit: JD {transit.jd:.6f}\n"
         f"H = {H.degrees:.4f}°\n"
         f"Rise: JD {result.jd:.6f}")

    return result


def planet_set(
    planet: Planet,
    observer: Observer,
    jd: Optional[JulianDate] = None,
    verbose: Optional[VerboseContext] = None
) -> Optional[JulianDate]:
    """
    Calculate the set time for a planet.

    Args:
        planet: Planet to calculate
        observer: Observer location
        jd: Julian Date (default: today)
        verbose: Optional verbose context

    Returns:
        JD of set, or None if planet doesn't set
    """
    if jd is None:
        jd = jd_now()

    step(verbose, f"{planet.value} set calculation",
         f"Observer: {observer.name}")

    # Get transit time
    transit = _planet_transit(planet, observer, jd, verbose)

    # Planet position at transit
    pos = planet_position(planet, transit)

    # Hour angle at set
    rise_altitude = -0.5667
    H = _hour_angle_rise_set(pos.dec, observer.latitude, rise_altitude, verbose)

    if H is None:
        step(verbose, "Result", f"{planet.value} does not set from this location")
        return None

    # Set is transit plus hour angle
    H_days = H.degrees / 360
    result = JulianDate(transit.jd + H_days)

    step(verbose, f"{planet.value} set result",
         f"Transit: JD {transit.jd:.6f}\n"
         f"H = {H.degrees:.4f}°\n"
         f"Set: JD {result.jd:.6f}")

    return result
