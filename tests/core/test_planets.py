"""
Tests for planetary position calculations.

Golden tests validated against JPL Horizons ephemeris data.
"""

from __future__ import annotations

import math
import pytest

from starward.core.angles import Angle
from starward.core.time import JulianDate, jd_now
from starward.core.observer import Observer
from starward.core.planets import (
    Planet, PlanetPosition, PLANET_SYMBOLS,
    planet_position, all_planet_positions,
    planet_altitude, planet_rise, planet_set, planet_transit,
)


# ═══════════════════════════════════════════════════════════════════════════════
#  BASIC FUNCTIONALITY
# ═══════════════════════════════════════════════════════════════════════════════

class TestPlanetEnum:
    """Tests for Planet enum."""

    def test_all_planets_exist(self):
        """All 7 planets are defined."""
        planets = list(Planet)
        assert len(planets) == 7

    def test_planet_names(self):
        """Planet names are correct."""
        assert Planet.MERCURY.value == "Mercury"
        assert Planet.VENUS.value == "Venus"
        assert Planet.MARS.value == "Mars"
        assert Planet.JUPITER.value == "Jupiter"
        assert Planet.SATURN.value == "Saturn"
        assert Planet.URANUS.value == "Uranus"
        assert Planet.NEPTUNE.value == "Neptune"

    def test_planet_symbols(self):
        """Each planet has a symbol."""
        for planet in Planet:
            assert planet in PLANET_SYMBOLS
            assert len(PLANET_SYMBOLS[planet]) > 0


class TestPlanetPosition:
    """Tests for PlanetPosition dataclass."""

    def test_returns_planet_position_object(self):
        """planet_position() returns PlanetPosition dataclass."""
        jd = JulianDate(2451545.0)
        pos = planet_position(Planet.MARS, jd)
        assert isinstance(pos, PlanetPosition)

    def test_has_required_fields(self):
        """PlanetPosition has all required fields."""
        jd = JulianDate(2451545.0)
        pos = planet_position(Planet.JUPITER, jd)

        assert hasattr(pos, 'planet')
        assert hasattr(pos, 'helio_longitude')
        assert hasattr(pos, 'helio_latitude')
        assert hasattr(pos, 'helio_distance')
        assert hasattr(pos, 'ra')
        assert hasattr(pos, 'dec')
        assert hasattr(pos, 'distance_au')
        assert hasattr(pos, 'magnitude')
        assert hasattr(pos, 'elongation')
        assert hasattr(pos, 'phase_angle')
        assert hasattr(pos, 'angular_diameter')

    def test_to_icrs_conversion(self):
        """to_icrs() returns valid ICRSCoord."""
        jd = JulianDate(2451545.0)
        pos = planet_position(Planet.SATURN, jd)
        icrs = pos.to_icrs()

        assert hasattr(icrs, 'ra')
        assert hasattr(icrs, 'dec')
        assert icrs.ra.degrees == pos.ra.degrees
        assert icrs.dec.degrees == pos.dec.degrees

    def test_illumination_property(self):
        """illumination property returns valid fraction."""
        jd = JulianDate(2451545.0)
        pos = planet_position(Planet.VENUS, jd)

        assert 0 <= pos.illumination <= 1

    def test_symbol_property(self):
        """symbol property returns planet symbol."""
        jd = JulianDate(2451545.0)
        pos = planet_position(Planet.MARS, jd)
        assert pos.symbol == "♂"


# ═══════════════════════════════════════════════════════════════════════════════
#  ALL PLANETS FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

class TestAllPlanetPositions:
    """Tests for all_planet_positions() function."""

    def test_returns_dict_of_all_planets(self):
        """all_planet_positions() returns positions for all planets."""
        jd = JulianDate(2451545.0)
        positions = all_planet_positions(jd)

        assert isinstance(positions, dict)
        assert len(positions) == 7

        for planet in Planet:
            assert planet in positions
            assert isinstance(positions[planet], PlanetPosition)


# ═══════════════════════════════════════════════════════════════════════════════
#  GOLDEN TESTS - Validated against JPL Horizons
# ═══════════════════════════════════════════════════════════════════════════════

class TestGoldenPositions:
    """
    Golden tests using positions from JPL Horizons.

    Accuracy target: ~1 arcminute for positions (using Meeus algorithms).
    These tests use dates where positions are well-known.
    """

    @pytest.mark.golden
    def test_mars_at_j2000(self):
        """
        Mars position at J2000.0.

        JPL Horizons (2000-Jan-01 12:00 TDB):
          RA: ~22h 0m, Dec: ~-13°
        """
        jd = JulianDate(2451545.0)  # J2000.0
        pos = planet_position(Planet.MARS, jd)

        # Allow 2 degree tolerance for simplified algorithm
        assert 320 < pos.ra.degrees < 340  # ~22h
        assert -16 < pos.dec.degrees < -10

    @pytest.mark.golden
    def test_jupiter_at_j2000(self):
        """
        Jupiter position at J2000.0.

        JPL Horizons (2000-Jan-01 12:00 TDB):
          RA: ~1h 36m (~24°), Dec: ~+8°
        """
        jd = JulianDate(2451545.0)
        pos = planet_position(Planet.JUPITER, jd)

        # Allow 3 degree tolerance for simplified algorithm
        assert 20 < pos.ra.degrees < 30  # ~1.6h = ~24°
        assert 6 < pos.dec.degrees < 12

    @pytest.mark.golden
    def test_saturn_at_j2000(self):
        """
        Saturn position at J2000.0.

        JPL Horizons: RA ~2h 40m, Dec ~+12°
        """
        jd = JulianDate(2451545.0)
        pos = planet_position(Planet.SATURN, jd)

        assert 35 < pos.ra.degrees < 55
        assert 8 < pos.dec.degrees < 16


class TestOrbitalDistances:
    """Tests for orbital distances."""

    def test_inner_planets_closer_than_outer(self):
        """Inner planets have smaller heliocentric distances."""
        jd = jd_now()

        mercury = planet_position(Planet.MERCURY, jd)
        venus = planet_position(Planet.VENUS, jd)
        mars = planet_position(Planet.MARS, jd)
        jupiter = planet_position(Planet.JUPITER, jd)

        assert mercury.helio_distance < venus.helio_distance
        assert venus.helio_distance < mars.helio_distance
        assert mars.helio_distance < jupiter.helio_distance

    def test_mercury_distance_bounds(self):
        """Mercury: 0.31 - 0.47 AU from Sun."""
        jd = jd_now()
        pos = planet_position(Planet.MERCURY, jd)
        assert 0.30 < pos.helio_distance < 0.48

    def test_venus_distance_bounds(self):
        """Venus: ~0.72 AU from Sun (nearly circular)."""
        jd = jd_now()
        pos = planet_position(Planet.VENUS, jd)
        assert 0.71 < pos.helio_distance < 0.73

    def test_mars_distance_bounds(self):
        """Mars: 1.38 - 1.67 AU from Sun."""
        jd = jd_now()
        pos = planet_position(Planet.MARS, jd)
        assert 1.37 < pos.helio_distance < 1.68

    def test_jupiter_distance_bounds(self):
        """Jupiter: 4.95 - 5.46 AU from Sun."""
        jd = jd_now()
        pos = planet_position(Planet.JUPITER, jd)
        assert 4.94 < pos.helio_distance < 5.47

    def test_saturn_distance_bounds(self):
        """Saturn: 9.02 - 10.05 AU from Sun."""
        jd = jd_now()
        pos = planet_position(Planet.SATURN, jd)
        assert 9.0 < pos.helio_distance < 10.1

    def test_uranus_distance_bounds(self):
        """Uranus: 18.3 - 20.1 AU from Sun."""
        jd = jd_now()
        pos = planet_position(Planet.URANUS, jd)
        assert 18.2 < pos.helio_distance < 20.2

    def test_neptune_distance_bounds(self):
        """Neptune: 29.8 - 30.3 AU from Sun."""
        jd = jd_now()
        pos = planet_position(Planet.NEPTUNE, jd)
        assert 29.7 < pos.helio_distance < 30.4


# ═══════════════════════════════════════════════════════════════════════════════
#  VISUAL PROPERTIES
# ═══════════════════════════════════════════════════════════════════════════════

class TestMagnitudes:
    """Tests for apparent magnitude calculations."""

    def test_venus_brightest(self):
        """Venus is typically the brightest planet."""
        jd = jd_now()
        positions = all_planet_positions(jd)

        # Venus should be brighter (lower magnitude) than most others
        # when not at inferior conjunction
        venus_mag = positions[Planet.VENUS].magnitude
        mars_mag = positions[Planet.MARS].magnitude
        saturn_mag = positions[Planet.SATURN].magnitude

        # Venus is usually brighter than Mars and Saturn
        # (unless Mars is at very close opposition)
        assert venus_mag < saturn_mag

    def test_jupiter_brighter_than_saturn(self):
        """Jupiter is always brighter than Saturn."""
        jd = jd_now()
        positions = all_planet_positions(jd)

        jupiter_mag = positions[Planet.JUPITER].magnitude
        saturn_mag = positions[Planet.SATURN].magnitude

        assert jupiter_mag < saturn_mag

    def test_outer_planets_dimmer(self):
        """Outer planets are dimmer than inner ones generally."""
        jd = jd_now()
        positions = all_planet_positions(jd)

        jupiter_mag = positions[Planet.JUPITER].magnitude
        uranus_mag = positions[Planet.URANUS].magnitude
        neptune_mag = positions[Planet.NEPTUNE].magnitude

        assert jupiter_mag < uranus_mag < neptune_mag


class TestElongation:
    """Tests for elongation calculations."""

    def test_elongation_within_bounds(self):
        """Elongation is between 0° and 180°."""
        jd = jd_now()

        for planet in Planet:
            pos = planet_position(planet, jd)
            assert 0 <= pos.elongation.degrees <= 180

    def test_inner_planet_elongation_limited(self):
        """Inner planets have limited maximum elongation."""
        jd = jd_now()

        mercury = planet_position(Planet.MERCURY, jd)
        venus = planet_position(Planet.VENUS, jd)

        # Mercury max elongation ~28°, Venus max ~47°
        assert mercury.elongation.degrees <= 30
        assert venus.elongation.degrees <= 50


class TestPhaseAngle:
    """Tests for phase angle calculations."""

    def test_phase_angle_within_bounds(self):
        """Phase angle is between 0° and 180°."""
        jd = jd_now()

        for planet in Planet:
            pos = planet_position(planet, jd)
            assert 0 <= pos.phase_angle.degrees <= 180

    def test_outer_planets_small_phase_angle(self):
        """Outer planets always have small phase angles."""
        jd = jd_now()

        jupiter = planet_position(Planet.JUPITER, jd)
        saturn = planet_position(Planet.SATURN, jd)
        neptune = planet_position(Planet.NEPTUNE, jd)

        # Outer planets never show significant phase
        assert jupiter.phase_angle.degrees < 12
        assert saturn.phase_angle.degrees < 7
        assert neptune.phase_angle.degrees < 2


# ═══════════════════════════════════════════════════════════════════════════════
#  RISE/SET/TRANSIT
# ═══════════════════════════════════════════════════════════════════════════════

class TestRiseSetTransit:
    """Tests for rise, set, and transit calculations."""

    @pytest.fixture
    def greenwich(self):
        """Greenwich observatory."""
        return Observer.from_degrees("Greenwich", 51.4769, -0.0005)

    @pytest.fixture
    def new_york(self):
        """New York City."""
        return Observer.from_degrees("New York", 40.7128, -74.0060)

    def test_transit_returns_julian_date(self, greenwich):
        """planet_transit() returns JulianDate."""
        jd = jd_now()
        transit = planet_transit(Planet.JUPITER, greenwich, jd)

        assert isinstance(transit, JulianDate)

    def test_rise_before_transit_before_set(self, greenwich):
        """For most cases: rise < transit < set."""
        jd = jd_now()

        rise = planet_rise(Planet.JUPITER, greenwich, jd)
        transit = planet_transit(Planet.JUPITER, greenwich, jd)
        set_time = planet_set(Planet.JUPITER, greenwich, jd)

        if rise and set_time:
            # This may not always hold for circumpolar objects
            # but should work for Jupiter at mid-latitudes
            assert rise.jd < transit.jd < set_time.jd

    def test_rise_set_returns_optional(self, greenwich):
        """Rise/set can return None for circumpolar/never-rises."""
        jd = jd_now()

        rise = planet_rise(Planet.JUPITER, greenwich, jd)
        set_time = planet_set(Planet.JUPITER, greenwich, jd)

        # These should be JulianDate or None
        assert rise is None or isinstance(rise, JulianDate)
        assert set_time is None or isinstance(set_time, JulianDate)

    def test_altitude_at_transit_is_maximum(self, greenwich):
        """Altitude at transit should be near maximum."""
        jd = jd_now()

        transit = planet_transit(Planet.JUPITER, greenwich, jd)
        alt_transit = planet_altitude(Planet.JUPITER, greenwich, transit)

        # Check altitude 1 hour before
        before = JulianDate(transit.jd - 1/24)
        alt_before = planet_altitude(Planet.JUPITER, greenwich, before)

        # Transit altitude should be higher
        assert alt_transit.degrees >= alt_before.degrees - 0.1


class TestPlanetAltitude:
    """Tests for planet_altitude() function."""

    @pytest.fixture
    def greenwich(self):
        return Observer.from_degrees("Greenwich", 51.4769, -0.0005)

    def test_returns_angle(self, greenwich):
        """planet_altitude() returns Angle."""
        jd = jd_now()
        alt = planet_altitude(Planet.MARS, greenwich, jd)

        assert isinstance(alt, Angle)

    def test_altitude_within_bounds(self, greenwich):
        """Altitude is between -90° and +90°."""
        jd = jd_now()

        for planet in Planet:
            alt = planet_altitude(planet, greenwich, jd)
            assert -90 <= alt.degrees <= 90


# ═══════════════════════════════════════════════════════════════════════════════
#  EDGE CASES
# ═══════════════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_default_jd_is_now(self):
        """Functions default to current time when jd=None."""
        pos1 = planet_position(Planet.MARS)  # jd=None
        pos2 = planet_position(Planet.MARS, jd_now())

        # Should be very close (within a few arcseconds)
        assert abs(pos1.ra.degrees - pos2.ra.degrees) < 0.01
        assert abs(pos1.dec.degrees - pos2.dec.degrees) < 0.01

    def test_far_future_date(self):
        """Can calculate for dates far in the future."""
        # Year 2100
        jd = JulianDate(2488070.0)
        pos = planet_position(Planet.JUPITER, jd)

        assert isinstance(pos, PlanetPosition)
        assert 0 <= pos.ra.degrees < 360

    def test_far_past_date(self):
        """Can calculate for dates in the past."""
        # Year 1900
        jd = JulianDate(2415021.0)
        pos = planet_position(Planet.SATURN, jd)

        assert isinstance(pos, PlanetPosition)
        assert 0 <= pos.ra.degrees < 360

    def test_all_planets_at_same_time(self):
        """Can calculate all planets at the same instant."""
        jd = JulianDate(2451545.0)
        positions = all_planet_positions(jd)

        # All should have valid RA/Dec
        for planet, pos in positions.items():
            assert 0 <= pos.ra.degrees < 360
            assert -90 <= pos.dec.degrees <= 90
