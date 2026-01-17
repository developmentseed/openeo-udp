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
                return params_module.get_parameters()
            else:
                raise ValueError(
                    f"{self.param_file} does not have a get_parameters() function"
                )

        except Exception as e:
            raise RuntimeError(f"Error loading parameter file {self.param_file}: {e}")

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

    def get_all_parameters(self, set_name: str = None) -> Dict[str, Parameter]:
        """Get all parameters as openEO Parameter objects.

        Args:
            set_name: Parameter set to use

        Returns:
            Dictionary mapping parameter names to Parameter objects
        """
        param_set = self.get_parameter_set(set_name)

        # Filter out non-Parameter objects (like location_name)
        parameters = {}
        for param_name, param_value in param_set.items():
            if isinstance(param_value, Parameter):
                parameters[param_name] = param_value

        return parameters

    def __str__(self) -> str:
        """String representation."""
        sets = list(self._parameter_sets.keys())
        current = self._current_set or "None"
        return f"ParameterManager({len(sets)} sets: {sets}, current: {current})"
