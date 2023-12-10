#!/usr/bin/env python

class TimeInterval:
    """
    A class for extracting and processing time intervals from a given file.

    The class is designed to read a file containing time points, extract these
    points, and compute intervals between consecutive time points.

    Attributes:
        file (file object): A file object opened for reading time points data.
        timePoints (list): A list to store time points extracted from the file.
        intervals (list): A list to store time intervals between consecutive time points.
    """

    def __init__(self, file_name):
        """
        The constructor for TimeInterval class.

        Opens the specified file for reading and initializes lists for time points and intervals.

        Parameters:
            file_name (str): The name of the file containing time points.
        """
        self.file = open(file_name, "r") 
        self.timePoints = []
        self.intervals = []

    def getTimePoints(self):
        """
        Reads and processes data from the file specified during object initialization
        to extract time points.

        Processes each line of the file by removing brackets, splitting the data on commas,
        and converting them to floats.

        Returns:
            list: A list of time points as floats.
        """
        self.timePoints = []
        for line in self.file:
            data = line.strip().replace("[", "").replace("]", "").split(",")
            self.timePoints = [float(x) for x in data]
        return self.timePoints

    def getTimeInterval(self):
        """
        Calculates the time intervals between consecutive time points starting from the fourth time point.

        Iterates over the time points and calculates the difference between consecutive points,
        summing these differences and then computing the average interval.

        Returns:
            float: The average time interval calculated from the time points.
        """
        total_interval = 0
        for i in range(4, len(self.timePoints)):
            interval = self.timePoints[i] - self.timePoints[i - 1]
            total_interval += interval
        average_interval = total_interval / (len(self.timePoints) - 4 - 1)
        return average_interval
