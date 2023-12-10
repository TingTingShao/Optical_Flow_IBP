#!/usr/bin/env python

import scipy.ndimage as ndimage
from skimage.feature import peak_local_max
from sklearn.neighbors import NearestNeighbors
from openpiv import preprocess
from skimage import exposure
import cv2
import skimage as ski
import numpy as np

class Preprocessing:
    """
    A class dedicated to preprocessing image data for PIV (Particle Image Velocimetry) analysis.
    
    The class provides methods for normalizing image arrays, checking for low contrast in a 
    localized area of the image, and increasing the contrast of an area within an image.
    
    Methods:
        normaliseImg: Normalizes the intensity of the entire image array.
        isLowConstrast: Checks if a specified area within the image is of low contrast.
        increaseContrast: Increases the contrast of a specified area within the image.
    """

    def __init__(self):
        """
        The constructor for Preprocessing class.
        
        This constructor currently does not initialize any attributes.
        """
        pass

    def normaliseImg(self, image_array):
        """
        Normalizes the intensity of the image array.
        
        Parameters:
            image_array (ndarray): The image array to normalize.
        
        Returns:
            ndarray: The normalized image array.
        """
        return preprocess.normalize_array(image_array, axis=None)

    def isLowConstrast(self, image_array, x, y, radius):
        """
        Checks if a specified area within the image is of low contrast.
        
        Parameters:
            image_array (ndarray): The image array to check.
            x (int): The x-coordinate of the center of the area of interest.
            y (int): The y-coordinate of the center of the area of interest.
            radius (int): The radius defining the size of the area of interest.
        
        Returns:
            bool: True if the area is of low contrast, False otherwise.
        """
        areaOfInterest = image_array[y-radius:y+radius, x-radius:x+radius]
        return exposure.is_low_contrast(areaOfInterest)
    
    def increaseContrast(self, image_array, x, y, radius):
        """
        Increases the contrast of a specified area within the image.
        
        Parameters:
            image_array (ndarray): The image array on which to perform the operation.
            x (int): The x-coordinate of the center of the area of interest.
            y (int): The y-coordinate of the center of the area of interest.
            radius (int): The radius defining the size of the area of interest.
        
        Returns:
            ndarray: The image array with increased contrast in the specified area.
        """
        crop = image_array[y-radius:y+radius, x-radius:x+radius]
        # crop = cv2.convertScaleAbs(crop) # default setting
        v_min, v_max = np.percentile(crop, (0.2, 99.8))
        crop = ski.exposure.rescale_intensity(crop, in_range=(v_min, v_max))
        result = image_array.copy()
        result[y-radius:y+radius, x-radius:x+radius] = crop 
        return  result
