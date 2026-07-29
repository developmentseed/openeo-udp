"""Canonical collections, bands, and the shared endpoint parameter mapper.

This module is the single source of truth for the *canonical* collection ids and
band names that ``*.params.py`` files use. Each endpoint declares an explicit
mapping table from these canonical identifiers to its backend-native ids
(see ``openeo_udp/endpoints/*.py``) and delegates to :func:`make_mapper`.

Canonical identifiers follow lowercase STAC-style conventions:

- collections: ``sentinel-2-l2a``, ``sentinel-1-grd``
- bands: ``b01``..``b12``, ``b8a``, ``scl`` (Sentinel-2); ``vh``, ``vv`` (Sentinel-1)

Anything an endpoint has no explicit mapping for raises
:class:`UnsupportedCollectionError` or :class:`UnsupportedBandError` rather than
being silently guessed or passed through.
"""

from enum import Enum
from typing import Any, Callable, Dict, List

from openeo.api.process import Parameter


class Collection(str, Enum):
    """Canonical collection identifiers used in ``*.params.py`` defaults."""

    SENTINEL2_L2A = "sentinel-2-l2a"
    SENTINEL1_GRD = "sentinel-1-grd"


# Canonical band sets per collection (lowercase STAC-style). Used for
# documentation and validation; endpoint band tables are keyed by these names.
CANONICAL_BANDS: Dict[Collection, List[str]] = {
    Collection.SENTINEL2_L2A: [
        "b01", "b02", "b03", "b04", "b05", "b06", "b07",
        "b08", "b8a", "b09", "b10", "b11", "b12", "scl",
        # Viewing-/sun-angle metadata bands.
        "viewzenithmean", "viewazimuthmean",
        "sunzenithangles", "sunazimuthangles",
    ],
    Collection.SENTINEL1_GRD: ["vh", "vv"],
}


# Explicit, non-fuzzy aliases so pre-existing graphs that still carry the old
# uppercase collection strings keep resolving. Anything not listed here (and not
# already a canonical value) raises UnsupportedCollectionError.
_COLLECTION_ALIASES: Dict[str, Collection] = {
    "sentinel2_l2a": Collection.SENTINEL2_L2A,
    "sentinel-2-l2a": Collection.SENTINEL2_L2A,
    "sentinel1_grd": Collection.SENTINEL1_GRD,
    "sentinel-1-grd": Collection.SENTINEL1_GRD,
}


class UnsupportedCollectionError(ValueError):
    """Raised when an endpoint has no mapping for a requested canonical collection."""


class UnsupportedBandError(ValueError):
    """Raised when an endpoint has no mapping for a requested canonical band."""


def resolve_canonical(collection_id: str) -> Collection:
    """Resolve a collection string to its canonical :class:`Collection`.

    Accepts the canonical lowercase ids and a small set of explicit aliases
    (e.g. the legacy uppercase ``SENTINEL2_L2A``). Raises
    :class:`UnsupportedCollectionError` for anything unrecognized — no fuzzy
    substring guessing.
    """
    key = str(collection_id).strip().lower()
    if key in _COLLECTION_ALIASES:
        return _COLLECTION_ALIASES[key]
    raise UnsupportedCollectionError(
        f"Unknown collection '{collection_id}'. Known canonical collections: "
        f"{[c.value for c in Collection]}"
    )


def _rebuild_parameter(param: Parameter, default: Any) -> Parameter:
    """Return a copy of ``param`` with a new default, preserving name/description."""
    return Parameter(
        param.name,
        description=(
            param.description if hasattr(param, "description") else param.name
        ),
        default=default,
    )


def make_mapper(
    endpoint_config: Dict[str, Any],
    collections: Dict[Collection, Dict[str, Any]],
) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """Build an endpoint ``map_parameters`` function from a config + mapping table.

    Args:
        endpoint_config: The endpoint's ``ENDPOINT_CONFIG`` (provides the
            backend-intrinsic ``reflectance_scale`` / ``bands_dimension`` /
            ``time_dimension`` attributes propagated to ``current_params``).
        collections: Mapping of canonical :class:`Collection` to a spec dict with
            ``"collection_id"`` (native id) and ``"bands"`` (canonical -> native
            band name dict).

    Returns:
        A ``map_parameters(params) -> mapped_params`` function that rewrites the
        ``collection`` and ``bands`` Parameters to backend-native values and
        raises on anything it cannot map.
    """
    endpoint_name = endpoint_config.get("name", "<unknown>")

    def map_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
        mapped = params.copy()

        # Propagate backend-intrinsic attributes into current_params so notebooks
        # can read them as plain scalars.
        mapped["reflectance_scale"] = endpoint_config["reflectance_scale"]
        mapped["bands_dimension"] = endpoint_config["bands_dimension"]
        mapped["time_dimension"] = endpoint_config["time_dimension"]

        collection_param = params.get("collection")
        if not isinstance(collection_param, Parameter):
            # No collection to map (e.g. param sets without a collection).
            return mapped

        canonical = resolve_canonical(collection_param.default)
        if canonical not in collections:
            raise UnsupportedCollectionError(
                f"Endpoint '{endpoint_name}' has no mapping for collection "
                f"'{canonical.value}'."
            )
        spec = collections[canonical]

        # Map the collection id to the backend-native value.
        mapped["collection"] = _rebuild_parameter(
            collection_param, spec["collection_id"]
        )

        # Map each requested band; unknown bands are an error, not a passthrough.
        bands_param = params.get("bands")
        if isinstance(bands_param, Parameter) and isinstance(bands_param.default, list):
            band_map = spec["bands"]
            mapped_bands = []
            for band in bands_param.default:
                key = str(band).lower()
                if key not in band_map:
                    raise UnsupportedBandError(
                        f"Endpoint '{endpoint_name}' has no mapping for band "
                        f"'{band}' of collection '{canonical.value}'. "
                        f"Available bands: {sorted(band_map)}"
                    )
                mapped_bands.append(band_map[key])
            mapped["bands"] = _rebuild_parameter(bands_param, mapped_bands)

        return mapped

    return map_parameters
