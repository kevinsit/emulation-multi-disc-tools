#!/bin/bash
set -e

# Find all .cue files and process them
find . -type f -name "*.cue" -print0 | while IFS= read -r -d '' cue_file; do
    base_name="${cue_file%.cue}"
    chd_file="${base_name}.chd"

    if [ -f "$chd_file" ]; then
        echo "Skipping $cue_file: $chd_file already exists"
    else
        echo "Converting $cue_file to $chd_file..."
        chdman createcd -i "$cue_file" -o "$chd_file"
    fi
done
