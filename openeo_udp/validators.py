"""Parameter validation module for OpenEO UDP notebooks.

Provides validation functions for spatial extents, temporal ranges, band lists,
and other common parameter types used in OpenEO processing workflows.
"""

import re
from datetime import datetime, date
from typing import Dict, List, Any, Union, Optional


class ValidationError(Exception):
    """Custom exception for parameter validation errors."""

    pass


class SpatialValidator:
    """Validator for spatial extent parameters."""

    @staticmethod
    def validate_bbox(bbox: Dict[str, float], strict: bool = True) -> bool:
        """Validate spatial bounding box.

        Args:
            bbox: Dictionary with 'west', 'east', 'north', 'south' keys
            strict: If True, raises ValidationError on failure. If False, returns bool.

        Returns:
            True if valid (when strict=False)

        Raises:
            ValidationError: If bbox is invalid and strict=True
        """
        try:
            # Check required keys
            required_keys = ["west", "east", "north", "south"]
            if not all(key in bbox for key in required_keys):
                raise ValidationError(
                    f"Missing required keys. Expected: {required_keys}"
                )

            # Extract values
            west, east, north, south = (
                bbox["west"],
                bbox["east"],
                bbox["north"],
                bbox["south"],
            )

            # Check types
            if not all(
                isinstance(val, (int, float)) for val in [west, east, north, south]
            ):
                raise ValidationError("All bbox values must be numeric")

            # Check longitude bounds
            if not (-180 <= west <= 180 and -180 <= east <= 180):
                raise ValidationError("Longitude values must be between -180 and 180")

            # Check latitude bounds
            if not (-90 <= south <= 90 and -90 <= north <= 90):
                raise ValidationError("Latitude values must be between -90 and 90")

            # Check logical consistency
            if west >= east:
                raise ValidationError(f"West ({west}) must be less than East ({east})")

            if south >= north:
                raise ValidationError(
                    f"South ({south}) must be less than North ({north})"
                )

            return True

        except ValidationError:
            if strict:
                raise
            return False

    @staticmethod
    def validate_area_size(
        bbox: Dict[str, float], max_area_km2: Optional[float] = None
    ) -> bool:
        """Validate that bounding box area is within limits.

        Args:
            bbox: Spatial bounding box
            max_area_km2: Maximum allowed area in square kilometers

        Returns:
            True if area is acceptable

        Raises:
            ValidationError: If area exceeds limits
        """
        if max_area_km2 is None:
            return True

        # Rough area calculation (degrees to km conversion)
        width_deg = bbox["east"] - bbox["west"]
        height_deg = bbox["north"] - bbox["south"]

        # Approximate conversion: 1 degree ≈ 111 km at equator
        area_km2 = width_deg * height_deg * 111 * 111

        if area_km2 > max_area_km2:
            raise ValidationError(
                f"Area too large: {area_km2:.1f} km² exceeds limit of {max_area_km2} km²"
            )

        return True


class TemporalValidator:
    """Validator for temporal extent parameters."""

    @staticmethod
    def validate_date_string(date_str: str) -> bool:
        """Validate date string format (ISO 8601: YYYY-MM-DD).

        Args:
            date_str: Date string to validate

        Returns:
            True if valid format

        Raises:
            ValidationError: If date format is invalid
        """
        iso_pattern = r"^\d{4}-\d{2}-\d{2}$"

        if not re.match(iso_pattern, date_str):
            raise ValidationError(
                f"Invalid date format: {date_str}. Expected YYYY-MM-DD"
            )

        try:
            datetime.fromisoformat(date_str)
            return True
        except ValueError as e:
            raise ValidationError(f"Invalid date value: {date_str} - {e}")

    @staticmethod
    def validate_temporal_range(
        temporal_extent: List[str], max_duration_days: Optional[int] = None
    ) -> bool:
        """Validate temporal extent range.

        Args:
            temporal_extent: List of [start_date, end_date] strings
            max_duration_days: Maximum allowed duration in days

        Returns:
            True if valid

        Raises:
            ValidationError: If temporal range is invalid
        """
        if not isinstance(temporal_extent, list) or len(temporal_extent) != 2:
            raise ValidationError(
                "Temporal extent must be a list of [start_date, end_date]"
            )

        start_str, end_str = temporal_extent

        # Validate individual dates
        TemporalValidator.validate_date_string(start_str)
        TemporalValidator.validate_date_string(end_str)

        # Check temporal order
        start_date = datetime.fromisoformat(start_str).date()
        end_date = datetime.fromisoformat(end_str).date()

        if start_date > end_date:
            raise ValidationError(
                f"Start date ({start_str}) must be before end date ({end_str})"
            )

        # Check duration limits
        if max_duration_days is not None:
            duration = (end_date - start_date).days
            if duration > max_duration_days:
                raise ValidationError(
                    f"Duration too long: {duration} days exceeds limit of {max_duration_days} days"
                )

        # Check for reasonable date range (not too far in future)
        today = date.today()
        if start_date > today:
            # Allow some future dates for planning, but warn for very distant futures
            days_in_future = (start_date - today).days
            if days_in_future > 365:
                raise ValidationError(
                    f"Start date is {days_in_future} days in the future"
                )

        return True


class BandValidator:
    """Validator for spectral band parameters."""

    # Standard Sentinel-2 band definitions
    SENTINEL2_BANDS = {
        "B01": {"name": "Coastal aerosol", "center_wavelength": 443, "resolution": 60},
        "B02": {"name": "Blue", "center_wavelength": 490, "resolution": 10},
        "B03": {"name": "Green", "center_wavelength": 560, "resolution": 10},
        "B04": {"name": "Red", "center_wavelength": 665, "resolution": 10},
        "B05": {"name": "Red Edge 1", "center_wavelength": 705, "resolution": 20},
        "B06": {"name": "Red Edge 2", "center_wavelength": 740, "resolution": 20},
        "B07": {"name": "Red Edge 3", "center_wavelength": 783, "resolution": 20},
        "B08": {"name": "NIR", "center_wavelength": 842, "resolution": 10},
        "B8A": {"name": "NIR Narrow", "center_wavelength": 865, "resolution": 20},
        "B09": {"name": "Water vapour", "center_wavelength": 945, "resolution": 60},
        "B10": {"name": "SWIR Cirrus", "center_wavelength": 1375, "resolution": 60},
        "B11": {"name": "SWIR 1", "center_wavelength": 1610, "resolution": 20},
        "B12": {"name": "SWIR 2", "center_wavelength": 2190, "resolution": 20},
    }

    @staticmethod
    def normalize_band_name(band: str) -> str:
        """Normalize band name to standard format (e.g., 'b02' -> 'B02').

        Args:
            band: Band name in any case/format

        Returns:
            Normalized band name
        """
        # Handle reflectance format: "reflectance|b02" -> "B02"
        if "|" in band:
            band = band.split("|")[-1]

        # Convert to uppercase and ensure B prefix
        band = band.upper()
        if not band.startswith("B"):
            band = "B" + band

        return band

    @staticmethod
    def validate_band_list(
        bands: List[str],
        required_bands: Optional[List[str]] = None,
        algorithm_name: Optional[str] = None,
    ) -> bool:
        """Validate list of spectral bands.

        Args:
            bands: List of band names to validate
            required_bands: List of bands that must be present
            algorithm_name: Name of algorithm for error context

        Returns:
            True if valid

        Raises:
            ValidationError: If band list is invalid
        """
        if not isinstance(bands, list) or not bands:
            raise ValidationError("Bands must be a non-empty list")

        # Normalize and validate each band
        normalized_bands = []
        for band in bands:
            if not isinstance(band, str):
                raise ValidationError(f"Band names must be strings, got: {type(band)}")

            # Handle different formats
            if "|" in band:
                # Reflectance format: validate the band part
                _, band_part = band.split("|", 1)
                normalized_band = BandValidator.normalize_band_name(band_part)
            else:
                normalized_band = BandValidator.normalize_band_name(band)

            # Check if band exists in Sentinel-2
            if normalized_band not in BandValidator.SENTINEL2_BANDS:
                available = list(BandValidator.SENTINEL2_BANDS.keys())
                raise ValidationError(
                    f"Unknown band: {band} (normalized: {normalized_band}). "
                    f"Available Sentinel-2 bands: {available}"
                )

            normalized_bands.append(normalized_band)

        # Check for required bands
        if required_bands:
            required_normalized = [
                BandValidator.normalize_band_name(b) for b in required_bands
            ]
            missing_bands = set(required_normalized) - set(normalized_bands)

            if missing_bands:
                context = f" for {algorithm_name}" if algorithm_name else ""
                raise ValidationError(
                    f"Missing required bands{context}: {list(missing_bands)}. "
                    f"Required: {required_bands}, Provided: {bands}"
                )

        return True

    @staticmethod
    def get_band_info(band: str) -> Dict[str, Any]:
        """Get information about a specific band.

        Args:
            band: Band name

        Returns:
            Dictionary with band information
        """
        normalized_band = BandValidator.normalize_band_name(band)

        if normalized_band not in BandValidator.SENTINEL2_BANDS:
            raise ValidationError(f"Unknown band: {band}")

        return BandValidator.SENTINEL2_BANDS[normalized_band]


def validate_parameter_value(
    param_type: str, value: Any, validation_rules: Optional[Dict] = None
) -> bool:
    """Validate a parameter value based on its type and rules.

    Args:
        param_type: Type of parameter ('spatial_bbox', 'temporal_range', 'band_list', etc.)
        value: Value to validate
        validation_rules: Optional validation rules dictionary

    Returns:
        True if valid

    Raises:
        ValidationError: If validation fails
    """
    rules = validation_rules or {}

    if param_type == "spatial_bbox":
        SpatialValidator.validate_bbox(value, strict=True)
        if "max_area_km2" in rules:
            SpatialValidator.validate_area_size(value, rules["max_area_km2"])

    elif param_type == "temporal_range":
        max_duration = rules.get("max_duration_days")
        TemporalValidator.validate_temporal_range(value, max_duration)

    elif param_type == "band_list":
        required_bands = rules.get("required_bands")
        algorithm_name = rules.get("algorithm_name")
        BandValidator.validate_band_list(value, required_bands, algorithm_name)

    elif param_type in ["string", "str"]:
        if not isinstance(value, str):
            raise ValidationError(f"Expected string, got {type(value)}")

    elif param_type in ["number", "float"]:
        if not isinstance(value, (int, float)):
            raise ValidationError(f"Expected number, got {type(value)}")

        if "min_value" in rules and value < rules["min_value"]:
            raise ValidationError(f"Value {value} below minimum {rules['min_value']}")

        if "max_value" in rules and value > rules["max_value"]:
            raise ValidationError(f"Value {value} above maximum {rules['max_value']}")

    else:
        # Generic validation - just check the value is not None
        if value is None:
            raise ValidationError(f"Parameter value cannot be None")

    return True
