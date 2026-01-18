"""Simple parameter manager for OpenEO UDP notebooks.

This module provides a simplified ParameterManager that loads parameter sets
from co-located .py files containing a get_parameters() function.
"""

import importlib.util
from pathlib import Path
from typing import Dict, Any, List
from openeo.api.process import Parameter


class ParameterManager:
    """Simple parameter manager for OpenEO UDP notebooks.

    Loads parameter sets from co-located .py files that return
    pre-configured openEO Parameter objects.
    """

    def __init__(self, param_file_path: str):
        """Initialize parameter manager with a parameter file.

        Args:
            param_file_path: Path to the .params.py file
        """
        self.param_file = Path(param_file_path)
        self._parameter_sets = self._load_parameter_sets()
        self._current_set = None

    def _load_parameter_sets(self) -> Dict[str, Dict[str, Any]]:
        """Load parameter sets from the .py file.

        Returns:
            Dictionary of parameter sets with Parameter objects
        """
        if not self.param_file.exists():
            raise FileNotFoundError(f"Parameter file not found: {self.param_file}")

        try:
            # Load the module dynamically
            spec = importlib.util.spec_from_file_location(
                "params_module", self.param_file
            )
            params_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(params_module)

            # Get parameter sets from get_parameters function
            if hasattr(params_module, "get_parameters"):
                parameter_sets = params_module.get_parameters()
                return self._ensure_parameter_descriptions(parameter_sets)
            else:
                raise ValueError(
                    f"{self.param_file} does not have a get_parameters() function"
                )

        except Exception as e:
            raise RuntimeError(f"Error loading parameter file {self.param_file}: {e}")

    def _ensure_parameter_descriptions(
        self, parameter_sets: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """Ensure all Parameter objects have descriptions, using name as fallback.

        Args:
            parameter_sets: Dictionary of parameter sets

        Returns:
            Dictionary of parameter sets with description fallbacks applied
        """
        processed_sets = {}

        for set_name, param_set in parameter_sets.items():
            processed_set = {}

            for key, value in param_set.items():
                if isinstance(value, Parameter):
                    # Check if Parameter has a description
                    if not hasattr(value, "description") or not value.description:
                        # Create a new Parameter with description fallback
                        processed_set[key] = Parameter(
                            value.name,
                            description=f"{value.name.replace('_', ' ').title()}",
                            default=value.default
                            if hasattr(value, "default")
                            else None,
                            schema=value.schema if hasattr(value, "schema") else None,
                        )
                    else:
                        processed_set[key] = value
                else:
                    processed_set[key] = value

            processed_sets[set_name] = processed_set

        return processed_sets

    def list_parameter_sets(self) -> List[str]:
        """Get list of available parameter set names.

        Returns:
            List of parameter set names
        """
        return list(self._parameter_sets.keys())

    def get_parameter_set(self, set_name: str = None) -> Dict[str, Any]:
        """Get a complete parameter set with Parameter objects.

        Args:
            set_name: Name of parameter set. If None, uses current set or first available.

        Returns:
            Dictionary containing Parameter objects and metadata
        """
        if set_name is None:
            set_name = self._current_set or (
                list(self._parameter_sets.keys())[0]
                if self._parameter_sets
                else "default"
            )

        if set_name not in self._parameter_sets:
            available = list(self._parameter_sets.keys())
            raise ValueError(
                f"Parameter set '{set_name}' not found. Available: {available}"
            )

        return self._parameter_sets[set_name]

    def use_parameter_set(self, set_name: str) -> None:
        """Set the current parameter set to use.

        Args:
            set_name: Name of parameter set to use
        """
        if set_name not in self._parameter_sets:
            available = list(self._parameter_sets.keys())
            raise ValueError(
                f"Parameter set '{set_name}' not found. Available: {available}"
            )

        self._current_set = set_name

    def get_parameter(self, name: str, set_name: str = None) -> Parameter:
        """Get openEO Parameter object for a specific parameter.

        Args:
            name: Parameter name (e.g., 'bounding_box', 'time', 'bands')
            set_name: Parameter set to use. If None, uses current set or first available.

        Returns:
            openEO Parameter object (already created in params file)
        """
        # Determine which parameter set to use
        if set_name is None:
            set_name = self._current_set or list(self._parameter_sets.keys())[0]

        param_set = self.get_parameter_set(set_name)

        if name not in param_set:
            available = list(param_set.keys())
            raise ValueError(
                f"Parameter '{name}' not found in set '{set_name}'. Available: {available}"
            )

        return param_set[name]

    def print_options(self, algorithm_name: str = "algorithm") -> None:
        """Print available parameter sets and endpoint options.

        Args:
            algorithm_name: Name of the algorithm for display purposes
        """
        from .endpoints import get_all_endpoints

        # Show available parameter sets
        available_sets = self.list_parameter_sets()
        print(f"Available parameter sets for {algorithm_name}:")
        for i, set_name in enumerate(available_sets, 1):
            params = self.get_parameter_set(set_name)
            location_name = params.get("location_name", set_name)
            print(f"  {i}. {set_name}: {location_name}")

        # Load and show endpoint configuration
        all_endpoints = get_all_endpoints()
        available_endpoints = [
            name
            for name, config in all_endpoints.items()
            if config.get("enabled", True)
        ]
        print(f"\nAvailable OpenEO endpoints:")
        for i, endpoint in enumerate(available_endpoints, 1):
            endpoint_info = all_endpoints[endpoint]
            print(f"  {i}. {endpoint}: {endpoint_info.get('url', 'URL not specified')}")

        # Show defaults
        default_endpoint = (
            available_endpoints[0] if available_endpoints else "copernicus_explorer"
        )
        print(
            f"\nDefaults: Parameter set '{available_sets[0]}' and endpoint '{default_endpoint}'"
        )
        print("To change selections, use the interactive widgets in the next cell.")

    def _load_mapper(self, endpoint_name: str):
        """Load parameter mapper for specific endpoint.

        Args:
            endpoint_name: Name of the endpoint

        Returns:
            Mapper function or None if not found
        """
        from .endpoints import get_endpoint_mapper

        return get_endpoint_mapper(endpoint_name)

    def apply_endpoint_mapping(
        self, params: Dict[str, Any], endpoint_name: str
    ) -> Dict[str, Any]:
        """Apply endpoint-specific parameter mapping.

        Args:
            params: Parameter dictionary to map
            endpoint_name: Name of the target endpoint

        Returns:
            Mapped parameter dictionary
        """
        # Load and apply mapper
        mapper_fn = self._load_mapper(endpoint_name)
        if mapper_fn:
            return mapper_fn(params)
        else:
            return params

    def __str__(self) -> str:
        """String representation."""
        sets = list(self._parameter_sets.keys())
        current = self._current_set or "None"
        return f"ParameterManager({len(sets)} sets: {sets}, current: {current})"

    def interactive_parameter_selection(self):
        """Create interactive parameter selection widgets.

        Returns:
            Callable function that returns (connection, current_params) tuple
        """
        # Import here to avoid circular imports and heavy widget dependencies
        from .widgets import interactive_parameter_selection

        return interactive_parameter_selection(self)

    def quick_connect(self, parameter_set: str = None, endpoint: str = None):
        """Quick programmatic connection without UI widgets.

        Args:
            parameter_set: Name of parameter set to use (uses first available if None)
            endpoint: Name of endpoint to connect to (uses first available if None)

        Returns:
            Tuple of (connection, current_params) where current_params is a dict of Parameter objects
        """
        # Import here to avoid circular imports
        from .widgets import quick_connect

        return quick_connect(self, parameter_set, endpoint)
