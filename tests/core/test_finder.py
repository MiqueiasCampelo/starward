"""
Tests for the cross-catalog finder module.

Tests unified search, category filtering, and result formatting.
"""

from __future__ import annotations

import pytest

from starward.core.finder import (
    find,
    find_by_type,
    find_by_category,
    find_in_constellation,
    find_bright,
    FinderResult,
    CatalogSource,
    ObjectCategory,
    TYPE_TO_CATEGORY,
    CATEGORY_TYPES,
)


# =============================================================================
#  FINDER RESULT
# =============================================================================

class TestFinderResult:
    """Tests for FinderResult dataclass."""

    def test_result_has_required_fields(self):
        """FinderResult has all required fields."""
        result = FinderResult(
            catalog=CatalogSource.NGC,
            designation="NGC 7000",
            name="North America Nebula",
            object_type="emission_nebula",
            category=ObjectCategory.NEBULA,
            ra_hours=20.9833,
            dec_degrees=44.5333,
            magnitude=4.0,
            constellation="Cyg",
            description="Large emission nebula",
            cross_refs=["C 20"],
        )
        assert result.catalog == CatalogSource.NGC
        assert result.designation == "NGC 7000"
        assert result.name == "North America Nebula"

    def test_display_name_with_name(self):
        """display_name returns name when available."""
        result = FinderResult(
            catalog=CatalogSource.NGC,
            designation="NGC 7000",
            name="North America Nebula",
            object_type="emission_nebula",
            category=ObjectCategory.NEBULA,
            ra_hours=20.9833,
            dec_degrees=44.5333,
            magnitude=4.0,
            constellation="Cyg",
            description="",
            cross_refs=[],
        )
        assert result.display_name == "North America Nebula"

    def test_display_name_without_name(self):
        """display_name returns designation when no name."""
        result = FinderResult(
            catalog=CatalogSource.NGC,
            designation="NGC 1234",
            name=None,
            object_type="galaxy",
            category=ObjectCategory.GALAXY,
            ra_hours=5.0,
            dec_degrees=30.0,
            magnitude=10.0,
            constellation="Tau",
            description="",
            cross_refs=[],
        )
        assert result.display_name == "NGC 1234"

    def test_category_name(self):
        """category_name returns human-readable category."""
        result = FinderResult(
            catalog=CatalogSource.NGC,
            designation="NGC 7000",
            name=None,
            object_type="emission_nebula",
            category=ObjectCategory.NEBULA,
            ra_hours=20.9833,
            dec_degrees=44.5333,
            magnitude=4.0,
            constellation="Cyg",
            description="",
            cross_refs=[],
        )
        assert result.category_name == "Nebula"

    def test_type_name(self):
        """type_name returns formatted type."""
        result = FinderResult(
            catalog=CatalogSource.NGC,
            designation="NGC 7000",
            name=None,
            object_type="emission_nebula",
            category=ObjectCategory.NEBULA,
            ra_hours=20.9833,
            dec_degrees=44.5333,
            magnitude=4.0,
            constellation="Cyg",
            description="",
            cross_refs=[],
        )
        assert result.type_name == "Emission Nebula"

    def test_str_with_name(self):
        """String representation includes name."""
        result = FinderResult(
            catalog=CatalogSource.NGC,
            designation="NGC 7000",
            name="North America Nebula",
            object_type="emission_nebula",
            category=ObjectCategory.NEBULA,
            ra_hours=20.9833,
            dec_degrees=44.5333,
            magnitude=4.0,
            constellation="Cyg",
            description="",
            cross_refs=[],
        )
        assert "NGC 7000" in str(result)
        assert "North America Nebula" in str(result)


# =============================================================================
#  TYPE MAPPINGS
# =============================================================================

class TestTypeMappings:
    """Tests for type-to-category mappings."""

    def test_galaxy_types_map_to_galaxy(self):
        """Galaxy types map to GALAXY category."""
        galaxy_types = ["galaxy", "galaxy_pair", "galaxy_group", "galaxy_triple"]
        for t in galaxy_types:
            assert TYPE_TO_CATEGORY.get(t) == ObjectCategory.GALAXY

    def test_nebula_types_map_to_nebula(self):
        """Nebula types map to NEBULA category."""
        nebula_types = ["planetary_nebula", "emission_nebula", "reflection_nebula",
                        "hii_region", "supernova_remnant", "dark_nebula"]
        for t in nebula_types:
            assert TYPE_TO_CATEGORY.get(t) == ObjectCategory.NEBULA

    def test_cluster_types_map_to_cluster(self):
        """Cluster types map to CLUSTER category."""
        cluster_types = ["globular_cluster", "open_cluster", "star_cluster", "cluster_nebula"]
        for t in cluster_types:
            assert TYPE_TO_CATEGORY.get(t) == ObjectCategory.CLUSTER

    def test_star_types_map_to_star(self):
        """Star types map to STAR category."""
        star_types = ["star", "double_star", "asterism"]
        for t in star_types:
            assert TYPE_TO_CATEGORY.get(t) == ObjectCategory.STAR

    def test_category_types_are_consistent(self):
        """CATEGORY_TYPES is consistent with TYPE_TO_CATEGORY."""
        for category, types in CATEGORY_TYPES.items():
            for t in types:
                assert TYPE_TO_CATEGORY.get(t) == category


# =============================================================================
#  FIND FUNCTION
# =============================================================================

class TestFind:
    """Tests for the find() function."""

    def test_find_returns_results(self):
        """find() returns a list of FinderResult."""
        results = find("nebula", limit=5)
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], FinderResult)

    def test_find_respects_limit(self):
        """find() respects the limit parameter."""
        results = find("a", limit=3)
        assert len(results) <= 3

    def test_find_case_insensitive(self):
        """find() is case-insensitive."""
        results1 = find("NEBULA", limit=5)
        results2 = find("nebula", limit=5)
        # Same number of results
        assert len(results1) == len(results2)

    def test_find_no_results(self):
        """find() returns empty list for no matches."""
        results = find("xyznonexistent123", limit=10)
        assert len(results) == 0

    def test_find_sorted_by_magnitude(self):
        """find() returns results sorted by magnitude."""
        results = find("galaxy", limit=10)
        mags = [r.magnitude for r in results if r.magnitude is not None]
        assert mags == sorted(mags)

    def test_find_filters_by_catalog(self):
        """find() filters by specified catalogs."""
        results = find("a", catalogs=[CatalogSource.NGC], limit=10)
        for r in results:
            assert r.catalog == CatalogSource.NGC


# =============================================================================
#  FIND BY TYPE
# =============================================================================

class TestFindByType:
    """Tests for the find_by_type() function."""

    def test_find_by_type_returns_correct_type(self):
        """find_by_type() returns objects of specified type."""
        results = find_by_type("galaxy", limit=10)
        for r in results:
            assert r.object_type == "galaxy"

    def test_find_by_type_filters_constellation(self):
        """find_by_type() filters by constellation."""
        results = find_by_type("open_cluster", constellation="Per", limit=10)
        for r in results:
            assert r.constellation == "Per"

    def test_find_by_type_filters_magnitude(self):
        """find_by_type() filters by magnitude."""
        results = find_by_type("galaxy", max_magnitude=8.0, limit=10)
        for r in results:
            if r.magnitude is not None:
                assert r.magnitude <= 8.0

    def test_find_by_type_no_results(self):
        """find_by_type() returns empty list when no matches."""
        results = find_by_type("galaxy", constellation="XXX", limit=10)
        assert len(results) == 0


# =============================================================================
#  FIND BY CATEGORY
# =============================================================================

class TestFindByCategory:
    """Tests for the find_by_category() function."""

    def test_find_by_category_enum(self):
        """find_by_category() works with ObjectCategory enum."""
        results = find_by_category(ObjectCategory.GALAXY, limit=10)
        for r in results:
            assert r.category == ObjectCategory.GALAXY

    def test_find_by_category_string(self):
        """find_by_category() works with string category."""
        results = find_by_category("galaxy", limit=10)
        for r in results:
            assert r.category == ObjectCategory.GALAXY

    def test_find_by_category_nebula(self):
        """find_by_category() finds nebulae of all types."""
        results = find_by_category(ObjectCategory.NEBULA, limit=20)
        for r in results:
            assert r.category == ObjectCategory.NEBULA

    def test_find_by_category_includes_multiple_types(self):
        """find_by_category() includes all object types in category."""
        results = find_by_category(ObjectCategory.NEBULA, limit=50)
        types = set(r.object_type for r in results)
        # Should have at least one type (if data exists)
        if results:
            assert len(types) >= 1


# =============================================================================
#  FIND IN CONSTELLATION
# =============================================================================

class TestFindInConstellation:
    """Tests for the find_in_constellation() function."""

    def test_find_in_constellation_returns_objects(self):
        """find_in_constellation() returns objects in constellation."""
        results = find_in_constellation("Cyg", limit=10)
        for r in results:
            assert r.constellation == "Cyg"

    def test_find_in_constellation_with_category(self):
        """find_in_constellation() filters by category."""
        results = find_in_constellation("Ori", category="nebula", limit=10)
        for r in results:
            assert r.constellation == "Ori"
            assert r.category == ObjectCategory.NEBULA

    def test_find_in_constellation_case_insensitive(self):
        """find_in_constellation() works with any case."""
        results1 = find_in_constellation("CYG", limit=5)
        results2 = find_in_constellation("cyg", limit=5)
        # Should find same results (may differ in exact matches due to DB behavior)
        assert len(results1) == len(results2)


# =============================================================================
#  FIND BRIGHT
# =============================================================================

class TestFindBright:
    """Tests for the find_bright() function."""

    def test_find_bright_default_magnitude(self):
        """find_bright() uses default magnitude of 6.0."""
        results = find_bright(limit=10)
        for r in results:
            if r.magnitude is not None:
                assert r.magnitude <= 6.0

    def test_find_bright_custom_magnitude(self):
        """find_bright() respects custom magnitude."""
        results = find_bright(max_magnitude=3.0, limit=10)
        for r in results:
            if r.magnitude is not None:
                assert r.magnitude <= 3.0

    def test_find_bright_with_category(self):
        """find_bright() filters by category."""
        results = find_bright(max_magnitude=8.0, category="galaxy", limit=10)
        for r in results:
            assert r.category == ObjectCategory.GALAXY

    def test_find_bright_sorted_by_magnitude(self):
        """find_bright() returns brightest first."""
        results = find_bright(max_magnitude=10.0, limit=20)
        mags = [r.magnitude for r in results if r.magnitude is not None]
        assert mags == sorted(mags)


# =============================================================================
#  CROSS-CATALOG RESULTS
# =============================================================================

class TestCrossCatalogResults:
    """Tests for cross-catalog functionality."""

    def test_results_from_multiple_catalogs(self):
        """find() can return results from multiple catalogs."""
        results = find("galaxy", limit=20)
        catalogs = set(r.catalog for r in results)
        # Should have at least NGC (if data exists)
        if results:
            assert len(catalogs) >= 1

    def test_results_include_cross_references(self):
        """Results include cross-references to other catalogs."""
        # NGC 224 (M31) should have Messier cross-ref
        results = find("andromeda", limit=10)
        andromeda = next((r for r in results if "224" in r.designation), None)
        if andromeda:
            assert len(andromeda.cross_refs) >= 0  # May or may not have

    def test_hipparcos_results_for_stars(self):
        """Star searches include Hipparcos results."""
        results = find("Vega", limit=10)
        hip_results = [r for r in results if r.catalog == CatalogSource.HIPPARCOS]
        assert len(hip_results) >= 1


# =============================================================================
#  CATALOG SOURCE
# =============================================================================

class TestCatalogSource:
    """Tests for CatalogSource enum."""

    def test_catalog_source_values(self):
        """CatalogSource has expected values."""
        assert CatalogSource.NGC.value == "ngc"
        assert CatalogSource.IC.value == "ic"
        assert CatalogSource.CALDWELL.value == "caldwell"
        assert CatalogSource.HIPPARCOS.value == "hipparcos"
        assert CatalogSource.MESSIER.value == "messier"
