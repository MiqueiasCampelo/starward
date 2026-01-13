"""
Finder CLI commands for cross-catalog object search.
"""

from __future__ import annotations

import click
from typing import Optional

from starward.core.finder import (
    find,
    find_by_type,
    find_by_category,
    find_in_constellation,
    find_bright,
    CatalogSource,
    ObjectCategory,
    CATEGORY_TYPES,
)


# Valid categories for CLI
_CATEGORIES = ["galaxy", "nebula", "cluster", "star"]

# All object types for CLI
_OBJECT_TYPES = [
    "galaxy", "galaxy_pair", "galaxy_group",
    "globular_cluster", "open_cluster", "star_cluster", "cluster_nebula",
    "planetary_nebula", "emission_nebula", "reflection_nebula",
    "hii_region", "supernova_remnant", "dark_nebula",
    "star", "double_star", "asterism",
]

# Catalog choices
_CATALOGS = ["ngc", "ic", "caldwell", "hipparcos", "all"]


def _parse_catalogs(catalog_str: Optional[str]) -> Optional[list]:
    """Parse catalog filter string."""
    if catalog_str is None or catalog_str == "all":
        return None

    catalog_map = {
        "ngc": CatalogSource.NGC,
        "ic": CatalogSource.IC,
        "caldwell": CatalogSource.CALDWELL,
        "hipparcos": CatalogSource.HIPPARCOS,
        "hip": CatalogSource.HIPPARCOS,
    }

    catalogs = []
    for c in catalog_str.lower().split(","):
        c = c.strip()
        if c in catalog_map:
            catalogs.append(catalog_map[c])

    return catalogs if catalogs else None


@click.group(name='find')
def find_group():
    """
    Cross-catalog object finder.

    \b
    Search for deep sky objects across NGC, IC, Caldwell, and Hipparcos catalogs.

    \b
    Examples:
        starward find search orion              # Search by name
        starward find galaxies --mag 10         # Find galaxies brighter than mag 10
        starward find nebulae --constellation Cyg   # Nebulae in Cygnus
        starward find in Ori                    # All objects in Orion
        starward find bright                    # Naked-eye objects
    """
    pass


@find_group.command(name='search')
@click.argument('query')
@click.option('--catalog', type=str, help='Catalogs to search (ngc,ic,caldwell,hipparcos or all)')
@click.option('--limit', type=int, default=25, help='Maximum results (default: 25)')
@click.pass_context
def search_cmd(ctx, query: str, catalog: Optional[str], limit: int):
    """Search for objects by name or description."""
    output_fmt = ctx.obj.get('output', 'plain')

    catalogs = _parse_catalogs(catalog)
    results = find(query, catalogs=catalogs, limit=limit)

    if not results:
        click.echo(f"No objects match '{query}'")
        return

    if output_fmt == 'json':
        import json
        data = {
            'query': query,
            'count': len(results),
            'results': [
                {
                    'catalog': r.catalog.value,
                    'designation': r.designation,
                    'name': r.name,
                    'type': r.object_type,
                    'category': r.category.value,
                    'ra_hours': r.ra_hours,
                    'dec_degrees': r.dec_degrees,
                    'magnitude': r.magnitude,
                    'constellation': r.constellation,
                    'cross_refs': r.cross_refs,
                }
                for r in results
            ]
        }
        click.echo(json.dumps(data, indent=2))
    else:
        from starward.output.console import print_finder_table
        print_finder_table(f'Search: "{query}"', results)


@find_group.command(name='galaxies')
@click.option('--mag', 'max_magnitude', type=float, help='Maximum magnitude')
@click.option('--constellation', type=str, help='Filter by constellation (3-letter code)')
@click.option('--catalog', type=str, help='Catalogs to search (ngc,ic,caldwell or all)')
@click.option('--limit', type=int, default=25, help='Maximum results (default: 25)')
@click.pass_context
def galaxies_cmd(ctx, max_magnitude: Optional[float], constellation: Optional[str],
                 catalog: Optional[str], limit: int):
    """Find galaxies."""
    output_fmt = ctx.obj.get('output', 'plain')

    catalogs = _parse_catalogs(catalog)
    results = find_by_category(
        ObjectCategory.GALAXY,
        constellation=constellation,
        max_magnitude=max_magnitude,
        catalogs=catalogs,
        limit=limit,
    )

    if not results:
        click.echo("No galaxies match the criteria")
        return

    if output_fmt == 'json':
        import json
        data = {
            'category': 'galaxy',
            'count': len(results),
            'results': [
                {
                    'catalog': r.catalog.value,
                    'designation': r.designation,
                    'name': r.name,
                    'type': r.object_type,
                    'magnitude': r.magnitude,
                    'constellation': r.constellation,
                }
                for r in results
            ]
        }
        click.echo(json.dumps(data, indent=2))
    else:
        title = "Galaxies"
        if constellation:
            title += f" in {constellation.upper()}"
        if max_magnitude:
            title += f" (mag <= {max_magnitude:.1f})"
        from starward.output.console import print_finder_table
        print_finder_table(title, results)


@find_group.command(name='nebulae')
@click.option('--mag', 'max_magnitude', type=float, help='Maximum magnitude')
@click.option('--constellation', type=str, help='Filter by constellation (3-letter code)')
@click.option('--type', 'nebula_type', type=click.Choice([
    'planetary_nebula', 'emission_nebula', 'reflection_nebula',
    'hii_region', 'supernova_remnant', 'dark_nebula'
], case_sensitive=False), help='Specific nebula type')
@click.option('--catalog', type=str, help='Catalogs to search (ngc,ic,caldwell or all)')
@click.option('--limit', type=int, default=25, help='Maximum results (default: 25)')
@click.pass_context
def nebulae_cmd(ctx, max_magnitude: Optional[float], constellation: Optional[str],
                nebula_type: Optional[str], catalog: Optional[str], limit: int):
    """Find nebulae."""
    output_fmt = ctx.obj.get('output', 'plain')

    catalogs = _parse_catalogs(catalog)

    if nebula_type:
        results = find_by_type(
            nebula_type,
            constellation=constellation,
            max_magnitude=max_magnitude,
            catalogs=catalogs,
            limit=limit,
        )
    else:
        results = find_by_category(
            ObjectCategory.NEBULA,
            constellation=constellation,
            max_magnitude=max_magnitude,
            catalogs=catalogs,
            limit=limit,
        )

    if not results:
        click.echo("No nebulae match the criteria")
        return

    if output_fmt == 'json':
        import json
        data = {
            'category': 'nebula',
            'type': nebula_type,
            'count': len(results),
            'results': [
                {
                    'catalog': r.catalog.value,
                    'designation': r.designation,
                    'name': r.name,
                    'type': r.object_type,
                    'magnitude': r.magnitude,
                    'constellation': r.constellation,
                }
                for r in results
            ]
        }
        click.echo(json.dumps(data, indent=2))
    else:
        title = nebula_type.replace("_", " ").title() if nebula_type else "Nebulae"
        if constellation:
            title += f" in {constellation.upper()}"
        if max_magnitude:
            title += f" (mag <= {max_magnitude:.1f})"
        from starward.output.console import print_finder_table
        print_finder_table(title, results)


@find_group.command(name='clusters')
@click.option('--mag', 'max_magnitude', type=float, help='Maximum magnitude')
@click.option('--constellation', type=str, help='Filter by constellation (3-letter code)')
@click.option('--type', 'cluster_type', type=click.Choice([
    'globular_cluster', 'open_cluster', 'star_cluster', 'cluster_nebula'
], case_sensitive=False), help='Specific cluster type')
@click.option('--catalog', type=str, help='Catalogs to search (ngc,ic,caldwell or all)')
@click.option('--limit', type=int, default=25, help='Maximum results (default: 25)')
@click.pass_context
def clusters_cmd(ctx, max_magnitude: Optional[float], constellation: Optional[str],
                 cluster_type: Optional[str], catalog: Optional[str], limit: int):
    """Find star clusters."""
    output_fmt = ctx.obj.get('output', 'plain')

    catalogs = _parse_catalogs(catalog)

    if cluster_type:
        results = find_by_type(
            cluster_type,
            constellation=constellation,
            max_magnitude=max_magnitude,
            catalogs=catalogs,
            limit=limit,
        )
    else:
        results = find_by_category(
            ObjectCategory.CLUSTER,
            constellation=constellation,
            max_magnitude=max_magnitude,
            catalogs=catalogs,
            limit=limit,
        )

    if not results:
        click.echo("No clusters match the criteria")
        return

    if output_fmt == 'json':
        import json
        data = {
            'category': 'cluster',
            'type': cluster_type,
            'count': len(results),
            'results': [
                {
                    'catalog': r.catalog.value,
                    'designation': r.designation,
                    'name': r.name,
                    'type': r.object_type,
                    'magnitude': r.magnitude,
                    'constellation': r.constellation,
                }
                for r in results
            ]
        }
        click.echo(json.dumps(data, indent=2))
    else:
        title = cluster_type.replace("_", " ").title() if cluster_type else "Star Clusters"
        if constellation:
            title += f" in {constellation.upper()}"
        if max_magnitude:
            title += f" (mag <= {max_magnitude:.1f})"
        from starward.output.console import print_finder_table
        print_finder_table(title, results)


@find_group.command(name='stars')
@click.option('--mag', 'max_magnitude', type=float, help='Maximum magnitude')
@click.option('--constellation', type=str, help='Filter by constellation (3-letter code)')
@click.option('--spectral', type=str, help='Spectral class prefix (e.g., A, K, M)')
@click.option('--limit', type=int, default=25, help='Maximum results (default: 25)')
@click.pass_context
def stars_cmd(ctx, max_magnitude: Optional[float], constellation: Optional[str],
              spectral: Optional[str], limit: int):
    """Find stars from Hipparcos catalog."""
    output_fmt = ctx.obj.get('output', 'plain')

    from starward.core.catalog_db import get_catalog_db
    from starward.core.hipparcos_types import HIPStar
    from starward.core.finder import _hipparcos_to_result

    db = get_catalog_db()
    filter_kwargs = {"limit": limit}
    if constellation:
        filter_kwargs["constellation"] = constellation
    if max_magnitude is not None:
        filter_kwargs["max_magnitude"] = max_magnitude
    if spectral:
        filter_kwargs["spectral_class"] = spectral

    results = []
    for data in db.filter_hipparcos(**filter_kwargs):
        star = HIPStar.from_dict(data)
        results.append(_hipparcos_to_result(star))

    if not results:
        click.echo("No stars match the criteria")
        return

    if output_fmt == 'json':
        import json
        data = {
            'category': 'star',
            'count': len(results),
            'results': [
                {
                    'designation': r.designation,
                    'name': r.name,
                    'magnitude': r.magnitude,
                    'constellation': r.constellation,
                    'cross_refs': r.cross_refs,
                }
                for r in results
            ]
        }
        click.echo(json.dumps(data, indent=2))
    else:
        title = "Stars"
        if spectral:
            title = f"Class {spectral.upper()} Stars"
        if constellation:
            title += f" in {constellation.upper()}"
        if max_magnitude:
            title += f" (mag <= {max_magnitude:.1f})"
        from starward.output.console import print_finder_table
        print_finder_table(title, results)


@find_group.command(name='in')
@click.argument('constellation')
@click.option('--category', type=click.Choice(_CATEGORIES, case_sensitive=False),
              help='Filter by category')
@click.option('--mag', 'max_magnitude', type=float, help='Maximum magnitude')
@click.option('--catalog', type=str, help='Catalogs to search')
@click.option('--limit', type=int, default=25, help='Maximum results (default: 25)')
@click.pass_context
def in_constellation_cmd(ctx, constellation: str, category: Optional[str],
                         max_magnitude: Optional[float], catalog: Optional[str], limit: int):
    """Find all objects in a constellation."""
    output_fmt = ctx.obj.get('output', 'plain')

    catalogs = _parse_catalogs(catalog)
    cat_enum = ObjectCategory(category) if category else None

    results = find_in_constellation(
        constellation,
        category=cat_enum,
        max_magnitude=max_magnitude,
        catalogs=catalogs,
        limit=limit,
    )

    if not results:
        click.echo(f"No objects found in {constellation.upper()}")
        return

    if output_fmt == 'json':
        import json
        data = {
            'constellation': constellation.upper(),
            'category': category,
            'count': len(results),
            'results': [
                {
                    'catalog': r.catalog.value,
                    'designation': r.designation,
                    'name': r.name,
                    'type': r.object_type,
                    'category': r.category.value,
                    'magnitude': r.magnitude,
                }
                for r in results
            ]
        }
        click.echo(json.dumps(data, indent=2))
    else:
        title = f"Objects in {constellation.upper()}"
        if category:
            title = f"{category.title()}s in {constellation.upper()}"
        if max_magnitude:
            title += f" (mag <= {max_magnitude:.1f})"
        from starward.output.console import print_finder_table
        print_finder_table(title, results)


@find_group.command(name='bright')
@click.option('--mag', 'max_magnitude', type=float, default=6.0,
              help='Maximum magnitude (default: 6.0 for naked eye)')
@click.option('--category', type=click.Choice(_CATEGORIES, case_sensitive=False),
              help='Filter by category')
@click.option('--catalog', type=str, help='Catalogs to search')
@click.option('--limit', type=int, default=25, help='Maximum results (default: 25)')
@click.pass_context
def bright_cmd(ctx, max_magnitude: float, category: Optional[str],
               catalog: Optional[str], limit: int):
    """Find bright objects visible to naked eye or binoculars."""
    output_fmt = ctx.obj.get('output', 'plain')

    catalogs = _parse_catalogs(catalog)
    cat_enum = ObjectCategory(category) if category else None

    results = find_bright(
        max_magnitude=max_magnitude,
        category=cat_enum,
        catalogs=catalogs,
        limit=limit,
    )

    if not results:
        click.echo(f"No objects brighter than magnitude {max_magnitude}")
        return

    if output_fmt == 'json':
        import json
        data = {
            'max_magnitude': max_magnitude,
            'category': category,
            'count': len(results),
            'results': [
                {
                    'catalog': r.catalog.value,
                    'designation': r.designation,
                    'name': r.name,
                    'type': r.object_type,
                    'magnitude': r.magnitude,
                    'constellation': r.constellation,
                }
                for r in results
            ]
        }
        click.echo(json.dumps(data, indent=2))
    else:
        title = f"Bright Objects (mag <= {max_magnitude:.1f})"
        if category:
            title = f"Bright {category.title()}s (mag <= {max_magnitude:.1f})"
        from starward.output.console import print_finder_table
        print_finder_table(title, results)


@find_group.command(name='type')
@click.argument('object_type', type=click.Choice(_OBJECT_TYPES, case_sensitive=False))
@click.option('--mag', 'max_magnitude', type=float, help='Maximum magnitude')
@click.option('--constellation', type=str, help='Filter by constellation (3-letter code)')
@click.option('--catalog', type=str, help='Catalogs to search')
@click.option('--limit', type=int, default=25, help='Maximum results (default: 25)')
@click.pass_context
def type_cmd(ctx, object_type: str, max_magnitude: Optional[float],
             constellation: Optional[str], catalog: Optional[str], limit: int):
    """Find objects by specific type."""
    output_fmt = ctx.obj.get('output', 'plain')

    catalogs = _parse_catalogs(catalog)
    results = find_by_type(
        object_type,
        constellation=constellation,
        max_magnitude=max_magnitude,
        catalogs=catalogs,
        limit=limit,
    )

    if not results:
        click.echo(f"No {object_type.replace('_', ' ')}s found")
        return

    if output_fmt == 'json':
        import json
        data = {
            'type': object_type,
            'count': len(results),
            'results': [
                {
                    'catalog': r.catalog.value,
                    'designation': r.designation,
                    'name': r.name,
                    'magnitude': r.magnitude,
                    'constellation': r.constellation,
                }
                for r in results
            ]
        }
        click.echo(json.dumps(data, indent=2))
    else:
        title = object_type.replace("_", " ").title() + "s"
        if constellation:
            title += f" in {constellation.upper()}"
        if max_magnitude:
            title += f" (mag <= {max_magnitude:.1f})"
        from starward.output.console import print_finder_table
        print_finder_table(title, results)
