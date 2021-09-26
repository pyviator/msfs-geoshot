# MSFS Screenshot GeoTag

import os
import sys
from pathlib import Path

__version__ = "1.0.0-beta.2"
__author__ = "pyviator"
__author_link__ = "https://github.com/pyviator"
__app_name__ = "MSFS GeoShot"
__copyright_year__ = 2021
__repository__ = "https://github.com/pyviator/msfs-geoshot"
__issues_tracker__ = "https://github.com/pyviator/msfs-geoshot/issues"
__support_thread__ = ""
__store_url__ = "https://flightsim.to/file/20868/geoshot-geotagged-screenshots-and-more"

def _resource_path(relative_path):
    """Shim for getting absolute path to resource that works in pyinstaller-bundled version"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


BINARY_PATH = Path(_resource_path("_bin"))
RESOURCES_PATH = Path(_resource_path("_resources"))
LICENSES_PATH = Path(_resource_path("_licenses"))

DEBUG = os.environ.get("DEBUG") is not None
MOCK_SIMULATOR = os.environ.get("MOCK_SIMULATOR") is not None
