#!/usr/bin/env python

# run expamle

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.optimize import curve_fit
import pandas as pd
import os, sys, argparse
import seaborn as sns

def parse_args():
    parser=argparse.ArgumentParser(description="plot the exponential curve")
    parser.add_argument("--velfile")
    parser.add_argument("--out_prefix")    
    return parser.parse_args()

def func(x, a, b):
    return a * np.exp(-b * x)
    
def main():
    args=parse_args()
    f=pd.read_csv(args.velfile,sep="\t", header=None)
    y=f.mean(numeric_only=True) 
    t = range(0, len(y)) 

    plt.figure(figsize=(10, 6))
    std_dev = f.std(numeric_only=True)
    plt.errorbar(t, y, yerr=std_dev, fmt='d', color='blue', 
                 ecolor='lightgray', elinewidth=3, 
                 capsize=0, label='Mean and Standard Deviation')

    infoDir={}

    # Create a line plot
    xdata = np.linspace(0, len(y), 100)
    # plt.plot(t, y, 'b-', label='data')
    popt,pcov = curve_fit(func, t, y)
    std_devs = np.sqrt(np.diag(pcov))
    a=popt[0]
    b=popt[1]
    std_dev_a = std_devs[0]
    std_dev_b = std_devs[1]

    cell= os.path.splitext(os.path.basename(args.velfile))[0]
    channel_num = None
    channel_info_file = os.path.join(args.out_prefix, f"{cell}.channel_info.csv")
    if os.path.exists(channel_info_file):
        with open(channel_info_file, 'r') as file:
            channel_num = int(file.read().strip())

    infoDir = {
        'cell': cell,
        'a': a,
        'b': b,
        'std_dev_a': std_dev_a,
        'std_dev_b': std_dev_b
    }
    
    # Include channel_num in infoDir if available
    if channel_num is not None:
        infoDir['channel_num'] = channel_num

    info_df = pd.DataFrame([infoDir])
    output_file_path = os.path.join(args.out_prefix, f"{cell}.info.temp.txt")
    info_df.to_csv(output_file_path, sep='\t', index=False, header=False)

    plt.plot(xdata, func(xdata, *popt), 'r-',
            label='Fitted Function:\n $y = %0.2f e^{-%0.2f t}$' % tuple(popt))
    plt.xlabel('Time (s)', fontsize=18)
    plt.ylabel('Velocity (micrometers/min)', fontsize=18)
    plt.title(f"Exponential Recoil Curve for Cell Type {cell}", fontsize=20, fontweight='bold')
    plt.ylim(-5, 20) 
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(frameon=True, shadow=True)
    for i, val in enumerate(y):
        plt.text(t[i], val, f'{val:.2f}', color='black', va='center', ha='right', fontsize=12)
    output_image_path = os.path.join(args.out_prefix, f"{cell}.expoCurve.png")
    plt.savefig(output_image_path, dpi=1000)
    plt.close()


    
if __name__=="__main__":
    main()

