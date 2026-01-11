"""
Planetary orbital elements and coefficients.

Data from Meeus, "Astronomical Algorithms", 2nd Edition.
Table 31.a: Elements of planetary orbits at J2000.0
Table 31.b: Rates of change per Julian century

These elements are mean values referred to the mean ecliptic and equinox
of J2000.0 (JDE 2451545.0).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class OrbitalElements:
    """
    Mean orbital elements at J2000.0 and their rates of change.

    All angles in degrees, distances in AU.
    Rates are per Julian century.
    """
    # Semi-major axis (AU)
    a0: float
    a_rate: float

    # Eccentricity
    e0: float
    e_rate: float

    # Inclination (degrees)
    i0: float
    i_rate: float

    # Longitude of ascending node (degrees)
    omega0: float  # Capital Omega
    omega_rate: float

    # Longitude of perihelion (degrees)
    pi0: float  # varpi = omega + Omega
    pi_rate: float

    # Mean longitude (degrees)
    L0: float
    L_rate: float


# Meeus Table 31.a and 31.b combined
# Elements referred to mean ecliptic and equinox of J2000.0
ORBITAL_ELEMENTS: Dict[str, OrbitalElements] = {
    "mercury": OrbitalElements(
        a0=0.38709927, a_rate=0.00000037,
        e0=0.20563593, e_rate=0.00001906,
        i0=7.00497902, i_rate=-0.00594749,
        omega0=48.33076593, omega_rate=-0.12534081,
        pi0=77.45779628, pi_rate=0.16047689,
        L0=252.25032350, L_rate=149472.67411175,
    ),
    "venus": OrbitalElements(
        a0=0.72333566, a_rate=0.00000390,
        e0=0.00677672, e_rate=-0.00004107,
        i0=3.39467605, i_rate=-0.00078890,
        omega0=76.67984255, omega_rate=-0.27769418,
        pi0=131.60246718, pi_rate=0.00268329,
        L0=181.97909950, L_rate=58517.81538729,
    ),
    "earth": OrbitalElements(
        a0=1.00000261, a_rate=0.00000562,
        e0=0.01671123, e_rate=-0.00004392,
        i0=-0.00001531, i_rate=-0.01294668,
        omega0=0.0, omega_rate=0.0,  # Reference plane
        pi0=102.93768193, pi_rate=0.32327364,
        L0=100.46457166, L_rate=35999.37244981,
    ),
    "mars": OrbitalElements(
        a0=1.52371034, a_rate=0.00001847,
        e0=0.09339410, e_rate=0.00007882,
        i0=1.84969142, i_rate=-0.00813131,
        omega0=49.55953891, omega_rate=-0.29257343,
        pi0=-23.94362959, pi_rate=0.44441088,
        L0=-4.55343205, L_rate=19140.30268499,
    ),
    "jupiter": OrbitalElements(
        a0=5.20288700, a_rate=-0.00011607,
        e0=0.04838624, e_rate=-0.00013253,
        i0=1.30439695, i_rate=-0.00183714,
        omega0=100.47390909, omega_rate=0.20469106,
        pi0=14.72847983, pi_rate=0.21252668,
        L0=34.39644051, L_rate=3034.74612775,
    ),
    "saturn": OrbitalElements(
        a0=9.53667594, a_rate=-0.00125060,
        e0=0.05386179, e_rate=-0.00050991,
        i0=2.48599187, i_rate=0.00193609,
        omega0=113.66242448, omega_rate=-0.28867794,
        pi0=92.59887831, pi_rate=-0.41897216,
        L0=49.95424423, L_rate=1222.49362201,
    ),
    "uranus": OrbitalElements(
        a0=19.18916464, a_rate=-0.00196176,
        e0=0.04725744, e_rate=-0.00004397,
        i0=0.77263783, i_rate=-0.00242939,
        omega0=74.01692503, omega_rate=0.04240589,
        pi0=170.95427630, pi_rate=0.40805281,
        L0=313.23810451, L_rate=428.48202785,
    ),
    "neptune": OrbitalElements(
        a0=30.06992276, a_rate=0.00026291,
        e0=0.00859048, e_rate=0.00005105,
        i0=1.77004347, i_rate=0.00035372,
        omega0=131.78422574, omega_rate=-0.00508664,
        pi0=44.96476227, pi_rate=-0.32241464,
        L0=-55.12002969, L_rate=218.45945325,
    ),
}


# Apparent magnitude parameters
# V(1,0) = absolute magnitude at 1 AU from Sun and Earth, phase angle 0
# Based on Meeus Ch. 41 and JPL data
@dataclass(frozen=True)
class MagnitudeParams:
    """Parameters for apparent magnitude calculation."""
    V0: float  # Absolute magnitude
    # Phase coefficients (magnitude increase per degree of phase)
    phase_coeff1: float  # Linear term
    phase_coeff2: float  # Quadratic term (for inner planets)


MAGNITUDE_PARAMS: Dict[str, MagnitudeParams] = {
    "mercury": MagnitudeParams(V0=-0.60, phase_coeff1=0.0380, phase_coeff2=0.000273),
    "venus": MagnitudeParams(V0=-4.47, phase_coeff1=0.0103, phase_coeff2=0.000057),
    "mars": MagnitudeParams(V0=-1.52, phase_coeff1=0.016, phase_coeff2=0.0),
    "jupiter": MagnitudeParams(V0=-9.40, phase_coeff1=0.005, phase_coeff2=0.0),
    "saturn": MagnitudeParams(V0=-8.88, phase_coeff1=0.044, phase_coeff2=0.0),
    "uranus": MagnitudeParams(V0=-7.19, phase_coeff1=0.002, phase_coeff2=0.0),
    "neptune": MagnitudeParams(V0=-6.87, phase_coeff1=0.001, phase_coeff2=0.0),
}


# Angular diameter at 1 AU (arcseconds)
ANGULAR_DIAMETER_1AU: Dict[str, float] = {
    "mercury": 6.74,
    "venus": 16.92,
    "mars": 9.36,
    "jupiter": 196.94,
    "saturn": 165.6,  # Equatorial, excluding rings
    "uranus": 70.48,
    "neptune": 68.30,
}
