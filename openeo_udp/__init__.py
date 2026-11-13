"""OpenEO User-Defined Processes (UDP) - Simple Parameter Management System

This package provides simple parameter management and endpoint configuration
for OpenEO notebooks in the DevelopmentSeed UDP repository.
"""

__version__ = "0.2.0"

from .parameter_manager import ParameterManager, list_parameter_files

__all__ = [
    "ParameterManager",
    "list_parameter_files",
]
