"""OpenEO User-Defined Processes (UDP) - Simple Parameter Management System

This package provides simple parameter management and endpoint configuration
for OpenEO notebooks in the DevelopmentSeed UDP repository.
"""

__version__ = "0.1.0"

from .parameter_manager import ParameterManager

__all__ = [
    "ParameterManager",
]