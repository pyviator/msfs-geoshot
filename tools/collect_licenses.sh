#!/bin/bash

PACKAGE_NAME="msfs_geoshot"
RESOURCES_PATH="${PACKAGE_NAME}/_resources"
BINARIES_PATH="$PACKAGE_NAME/_bin"
LICENSES_PATH="${PACKAGE_NAME}/_licenses"

# Binaries
out_file="$LICENSES_PATH/licenses_binaries.txt"
rm "$out_file"
for license_file in $BINARIES_PATH/license_*; do
    base_name=$(basename $license_file)
    binary_name="$(echo "$base_name" | cut -d '_' -f 2 | cut -d "." -f 1)"
    content=$(cat "$license_file")
    content="exiftool\n\n${content}"
    echo -e "$content" >> "$out_file"
done

# Python packages
out_file="$LICENSES_PATH/licenses_pypi.txt"
bundled_packages=$(poetry show --no-dev | cut -d " " -f 1 | tr "\n" " ")
pip-licenses --from=mixed --format=plain-vertical --with-authors --with-urls --with-license-file --no-license-path --output-file "$out_file" --packages ${bundled_packages}
sed -i -- 's/UNKNOWN//g' "$out_file"

# Media
out_file="$LICENSES_PATH/licenses_media.txt"
python -m markdown "$RESOURCES_PATH/README.md" > "$out_file"

# Own license
cp LICENSE "$LICENSES_PATH/license.txt"
