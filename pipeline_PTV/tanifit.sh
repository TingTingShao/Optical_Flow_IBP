#!/bin/bash

# python tanilacian.py -l 1.8 /Volumes/USB/IBP_data/peoject_starting_matrial/IBP-starting-data/ablations_data/220830-E1_Out.czi -o /Volumes/USB/IBP_data/results/tanitracer/220830-E1_Out_log.tif
python tanifit.py -l 1.8 -T 0.01 0.1 0.001 -i -z 3 /Volumes/USB/IBP_data/peoject_starting_matrial/IBP-starting-data/ablations_data/220830-E6_Out.czi -o /Volumes/USB/IBP_data/results/tanitracer/220830-E6_Out_fit.tif