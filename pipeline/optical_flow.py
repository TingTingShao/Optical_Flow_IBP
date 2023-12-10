#!/usr/bin/env python

import czifile
import os, sys, argparse
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.registration import optical_flow_ilk
import math
from skimage.draw import ellipse
from skimage.measure import label, regionprops, regionprops_table
from openpiv import tools, preprocess
import time
import pandas as pd
import scipy.ndimage as ndimage

from opclass import cutPosition
from opclass import timeInterval
from opclass import exponentialCurve
from opclass import preprocessing

start_time = time.time()

### Default values
input_filename = None
output_filename = None
lineage_filename = None
frametimes_filename = None
csv_filename = None

### Use the argparse module to handle command-line arguments

parser = argparse.ArgumentParser(description='plot the velocity change', \
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('input_file', nargs=1, default=input_filename, \
                    help='input czi file')
parser.add_argument('-l', '--lineage-file', nargs=1, default=None , \
                    help='input the lineage file to get cut position')
parser.add_argument('-t', '--timeframe-file', nargs=1, default=None , \
                    help='input time frame file to get time interval')
parser.add_argument('-c', '--csv-file', nargs=1, default=None , \
                    help='input the CSV file')
parser.add_argument('-o', '--output_file', nargs=1, default=None, \
                    help='input the output file name')

args = parser.parse_args()

# Prints the arguments to the console (just for checking the input)
print(args)

input_filename = args.input_file[0]
lineage_filename = args.lineage_file[0]
frametimes_filename = args.timeframe_file[0]
csv_filename = args.csv_file[0]

if args.output_file is None:
    output_filename = os.path.splitext(os.path.basename(input_filename))[0]
    if input_filename == output_filename:
        raise Exception('input_filename == output_image_filename')
    print(output_filename)
else:
    output_filename = args.output_file[0]

'''
Takes a 2-dimensional vector a as input and returns a new vector b that is perpendicular to a
'''

def perpendicular(a):
    b = np.empty_like(a) # creates a new NumPy array b with the same shape and data type as the input vector
    b[0] = -a[1] # assigns the value of -a[1] to the first element of the array b
    b[1] = a[0] # assigns the value of a[0] to the second element of the array b
    return b

"""
Takes a vector a as input, converts it to a NumPy array, and then returns a new vector where all 
elements are scaled such that the resulting vector has a length of 1 --> returns the unit vector
"""
def normalize(a):
    a = np.array(a)
    return a/np.linalg.norm(a)
# np.linalg.norm calculates the Euclidean norm (length) of the vector a. This is the square root of the sum of the squares of the elements in a.

"""
Takes an image as input and returns a normalized version of the image (pixel values ranging from 0 to 1)
"""
def normaliseImg(image):
    image=preprocess.normalize_array(image, axis=None)
    return image

"""
Takes the image array (imgs) with dimensions (timepoints, x, y) and returns the list of vectors
located around the cut site for timepoints 4(right after the cut) to 9 (?)
"""
def select_vectors(imgs, c):

    global p1, p2, diameter
    results={}
    midX=(p1[0]+p2[0])/2
    midY=(p1[1]+p2[1])/2

    for i in range(0,6):

        radius=diameter/2

        # img0 = imgs[0]
        img1 = imgs[i]
        img2 = imgs[i+1]

        v, u = optical_flow_ilk(img1, img2, radius=15) ## specifying a window or neighborhood size for processing
        nvec = 20  # Number of vectors to be displayed along each image dimension
        nl, nc = img1.shape
        step = max(nl//nvec, nc//nvec)
        y, x = np.mgrid[:nl:step, :nc:step]
        u_ = u[::step, ::step]
        v_ = v[::step, ::step]

        ##### under development --stt
        if i==0:     
            norm = np.sqrt(u ** 2 + v ** 2)
            fig, ax1 = plt.subplots(figsize=(8, 4))
            ax1.imshow(norm)
            ax1.quiver(x, y, u_, v_, color='r', units='dots',
                    angles='xy', scale_units='xy', lw=3)
            ax1.set_title(f"Optical flow vector field image {i+3}-{i+4}")
            ax1.set_axis_off()
            fig.tight_layout()
            fig.savefig(f"{output_filename}_{c}.log.png")
        #####

        #  define the region of interest (ROI) for selecting vectors in the subsequent steps.
        rr, cc = ellipse(midY, midX, radius, radius)
        # Create a boolean mask that checks if each (x, y) coordinate is within the ellipse region
        mask = np.isin(x, cc) & np.isin(y, rr)

        # Use the mask to select the corresponding vectors from u_ and v_
        selected_u = u_[mask]
        selected_v = v_[mask]
        selected_x = x[mask]
        selected_y = y[mask]

        # centering
        selected_y=selected_y-midY
        selected_x=selected_x-midX
        vector_data = np.column_stack((selected_x, selected_y, selected_u, selected_v))

        p1 = np.array(p1)
        p2 = np.array(p2)
        direction_vector = p2 - p1

        projectTo_Unit_Vec=perpendicular(normalize(direction_vector))

        # project the position vectors
        projected_position = np.dot(vector_data[:, 0:2], projectTo_Unit_Vec)
        
        vector_data = np.concatenate((vector_data, projected_position.reshape(-1, 1)), axis=1)

        # Calculate velocity based on the sign(+/-) of the positional vectors
        vec_len = np.where(vector_data[:, 4] > 0, 
                           np.dot(vector_data[:, 2:4], projectTo_Unit_Vec), 
                           np.dot(vector_data[:, 2:4], -projectTo_Unit_Vec))

        # convert velocity from pixels/s to micrometers/mins
        # 1 pixel = 0.05 micrometers
        vec_len_micrometers_per_minute = (vec_len/time_interval) * 0.05 * 60

        # Store the vectors in the results dictionary (each entry is a list of vectors for a certain timepoint start from time point 4)
        results[time_points[i+1+3]-time_points[4]] = vec_len_micrometers_per_minute


    result_df = pd.DataFrame(results)
    return result_df 


########################################
########## Implementation ##############
########################################

# get cut position
position = cutPosition.CutPosition(lineage_filename)
p1, p2, diameter=position.get_cut_position()

# Create an instance of TimeInterval
interObject = timeInterval.TimeInterval(frametimes_filename)
time_points=interObject.getTimePoints()
time_interval = interObject.getTimeInterval()
print("Time interval:" + str(time_interval))


image_data=czifile.imread(input_filename).squeeze()

# initiate a directory to input the sample-specific statistics: 
# channel number, label, cell type, MSE, a, b......
infoDir={}

if image_data.ndim == 3:
    infoDir['channel_num']=1
    imgs = image_data[3:10:1]    
    result = select_vectors(imgs, c=0)
    print('image with only one channel')
if image_data.ndim == 4:
    infoDir['channel_num']=2
    img0=image_data[0]
    img1=image_data[1]
    imgs0 = img0[3:10:1]
    imgs1 = img1[3:10:1]  
    df1 = select_vectors(imgs1, c=1)
    df0 = select_vectors(imgs0, c=0)
    frames = [df0, df1]
    result = pd.concat(frames)
    print('image with two channels')

# print(result)
result.to_csv(output_filename+".txt", sep='\t', index=False)

channel_info_file = os.path.join(output_filename + ".channel_info.csv")
with open(channel_info_file, 'w') as file:
    file.write(str(infoDir['channel_num']))

end_time_read = time.time()
print("Time to process: "+str(end_time_read - start_time)+" seconds")
