"""Configuration module for OpenEO UDP parameter management.

Provides endpoint configuration and connection management functionality.
"""

from .endpoint_config import load_endpoint_config, get_connection

__all__ = [
    "load_endpoint_config",
    "get_connection",
]