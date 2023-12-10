#!/bin/bash

# rm /Volumes/USB/IBP_data/info_trail.csv
# touch /Volumes/USB/IBP_data/info_trail.csv

# python optical_flow.py /Volumes/USB/IBP_data/peoject_starting_matrial/IBP-starting-data/ablations_data/220830-E6_Out.czi \\
#     -l /Volumes/USB/IBP_data/peoject_starting_matrial/IBP-starting-data/ablations_data/220830-E6_Out.lineage \\
#     -t /Volumes/USB/IBP_data/peoject_starting_matrial/IBP-starting-data/ibp-frametimes/220830-E6_frametimes.txt \\
#     -c /Volumes/USB/IBP_data/peoject_starting_matrial/IBP-starting-data/ablation_info_big.csv \\
#     -o /Volumes/USB/IBP_data/results/220830-E6_Out


# Paths
path_csv="/Volumes/USB/IBP_data/peoject_starting_matrial/IBP-starting-data/ablation_info_big.csv"
path_input_dir="/Volumes/USB/IBP_data/all_files"
path_output_dir="/Volumes/USB/IBP_data/all_results_pipline"

# Check if the input directory exists
if [ ! -d "$path_input_dir" ]; then
    echo "Input directory does not exist."
    exit 1
fi

# Check if the CSV file exists
if [ ! -f "$path_csv" ]; then
    echo "CSV file does not exist."
    exit 1
fi

# Iterate over .czi files in the input directory
for czi_file in "$path_input_dir"/*_Out.czi; do
    if [ -f "$czi_file" ]; then
        base_name=$(basename "$czi_file" "_Out.czi")
        lineage_file="$path_input_dir/${base_name}_Out.lineage"
        frametimes_file="$path_input_dir/${base_name}_frametimes.txt"
        output_file="$path_output_dir/${base_name}"

        echo "Processing: $czi_file"

        python optical_flow.py "$czi_file" \
            -l "$lineage_file" \
            -t "$frametimes_file" \
            -c "$path_csv" \
            -o "$output_file"
    else
        echo "No .czi files found in $path_input_dir."
    fi
done


