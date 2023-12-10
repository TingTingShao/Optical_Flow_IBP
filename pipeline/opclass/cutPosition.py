    
#!/usr/bin/env python

import math

class CutPosition:
    # Constructor method with parameter file_name
    def __init__(self, file_name):
        # Open the specified file for reading with proper encoding
        self.file = open(file_name, 'r', encoding='unicode_escape')
        # Initialize empty lists to store coordinates of cut positions
        self.p1 = []
        self.p2 = []

    '''
    Reads a file containing lineage information and extracts the coordinates of two points labeled 
    as 'cut1' and 'cut2' and calculates the Euclidean distance between these two points.
    Input parameter: None (uses the file opened during the object's initialization)
    Returns: cut position 1 and 2 (in the form of array) and cut length
    '''
    def get_cut_position(self):
        # Iterate through each line in the file
        for line in self.file:
            # Split the line into columns based on tab delimiter
            columns = line.strip().split('\t')
            # If the first column equals 'cut1', read the x and y coordinates
            if columns[0] == 'cut1':
                cut1_x = float(columns[2])
                cut1_y = float(columns[3])
                # Store the coordinates in the p1 list
                self.p1 = [cut1_x, cut1_y]
            # If the first column equals 'cut2', read the x and y coordinates
            elif columns[0] == 'cut2':
                cut2_x = float(columns[2])
                cut2_y = float(columns[3])
                # Store the coordinates in the p2 list
                self.p2 = [cut2_x, cut2_y]
        # Calculate the Euclidean distance between the two points
        cut_length = math.dist(self.p1, self.p2)
        # Return the coordinates of the two points and the distance between them
        return self.p1, self.p2, cut_length


