#!/usr/bin/env python

import subprocess
import sys
from pathlib import Path
from typing import Dict, List

from jinja2 import Template
from msfs_geoshot import __app_name__, __author__, __version__

# packages to exclude from wheels (e.g. in case they are platform-specific
# or do not support wheels)
EXCLUDE_PACKAGES: List[str] = ["xcffib"]

PACKAGING_PATH = Path(__file__).parent.parent / "packaging"
TEMPLATE_PATH = PACKAGING_PATH / "pynsist.cfg.jinja"
OUT_PATH = PACKAGING_PATH / "pynsist.cfg"

with TEMPLATE_PATH.open(encoding="utf-8") as template_file:
    template: Template = Template(template_file.read())

non_dev_dependencies = subprocess.check_output("poetry show --no-dev", text=True)

packages: Dict[str, str] = {}

for line in non_dev_dependencies.replace("(!)", "   ").split("\n"):
    try:
        name, version, *_ = line.split()
    except ValueError:
        continue
    if name in EXCLUDE_PACKAGES:
        continue
    packages[name] = version

wheels_string = "\n".join(
    f"    {package}=={version}" for package, version in packages.items()
)

build_data = {
    "__author__": __author__,
    "__app_name__": __app_name__,
    "__version__": __version__,
    "wheels": wheels_string,
    "python_version": sys.version.split()[0],
}

with OUT_PATH.open("w", encoding="utf-8") as config_file:
    config_file.write(template.render(build_data))
