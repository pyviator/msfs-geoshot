# MSFS Screenshot GeoTag

import os
import sys
from pathlib import Path

__version__ = "0.1.0"
__author__ = "pyviator"
__app_name__ = "MSFS GeoShot"


def _resource_path(relative_path):
    """Shim for getting absolute path to resource that works in pyinstaller-bundled version"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


BINARY_PATH = Path(_resource_path("_bin"))
RESOURCES_PATH = Path(_resource_path("_resources"))

DEBUG = os.environ.get("DEBUG") is not None
MOCK_SIMULATOR = os.environ.get("MOCK_SIMULATOR") is not None
