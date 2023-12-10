#!/bin/bash

# path to the ablation_into_big.csv
path_csv="/Volumes/USB/IBP_data/peoject_starting_matrial/IBP-starting-data"

# out directory path
out_path="/Volumes/USB/IBP_data/cell_type_results"

# input_txt input files with individual sample (cell) velocity 
input_txt="/Volumes/USB/IBP_data/all_results_pipline"

# Read distinct values from col2 (label) in CSV file
distinct_values=$(tail -n +2 "$path_csv/ablation_info_big.csv" | cut -d ',' -f 2 | sort -u)

# Create CSV files for each distinct value
for value in $distinct_values; do
    csv_filename="$out_path/${value}.txt"
done

# Process files in folder/*.txt
for txt_file in $input_txt/*.txt; do
    filename=$(basename "$txt_file" .txt)
    label_value=$(grep -m 1 "^$filename," "$path_csv/ablation_info_big.csv" | cut -d ',' -f 2)

    if [ -n "$label_value" ]; then
        tail -n +2 "$txt_file" >> "$out_path/${label_value}.txt"
    else
        echo "Warning: No matching value found for $txt_file in the txt file."
    fi
done
