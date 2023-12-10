#!/bin/bash

# this script is to plot the exponential curve, generate the statstics for 

# python exponential_curve.py --velfile /Volumes/USB/IBP_data/results/220830-E6.txt --out_prefix /Volumes/USB/IBP_data/results/220830-E6
# python exponential_curve.py --velfile /Volumes/USB/IBP_data/results/220830-E6_1.txt --out_prefix /Volumes/USB/IBP_data/results/220830-E6_combined --append --second_file /Volumes/USB/IBP_data/results/220830-E6_0.txt

DIRECTORY="/Volumes/USB/IBP_data/cell_type_results"
OUTPUT_DIR="/Volumes/USB/IBP_data/cell_type_results"
COMBINED_FILE="$OUTPUT_DIR/combined_info.txt"

# Iterate over each .txt file in the directory
for FILE in "$DIRECTORY"/*.txt; do
    # Run the Python script with each .txt file
    python exponential_curve.py --velfile "$FILE" --out_prefix "$OUTPUT_DIR"
done

# Clear the output file to avoid appending to an existing file
> "$COMBINED_FILE"

for FILE in "$DIRECTORY"/*.info.temp.txt; do
    # concatenat all the text files into one
    if [ -f "$FILE" ]; then
        cat "$FILE" >> "$COMBINED_FILE"
        # Remove the temporary files
        rm "$FILE"
    fi
done

