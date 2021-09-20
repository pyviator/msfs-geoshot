#!/bin/bash

PACKAGE_NAME="msfs_screenshot_geotag"
RESOURCES_PATH="${PACKAGE_NAME}/_resources"

out_file="$RESOURCES_PATH/licenses.txt"
bundled_packages=$(poetry show --no-dev | cut -d " " -f 1 | tr "\n" " ")
pip-licenses --from=mixed --format=plain-vertical --with-authors --with-urls --with-license-file --no-license-path --output-file "$out_file" --packages ${bundled_packages}
sed -i -- 's/UNKNOWN//g' "$out_file"
