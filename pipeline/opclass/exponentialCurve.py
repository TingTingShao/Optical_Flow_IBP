#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
from sklearn.metrics import mean_squared_error 

class ExponentialCurve:
    '''
    A class to encapsulate the operations for fitting an exponential curve to
    a given set of data points, plotting the results, and calculating the mean
    squared error of the fit.
    
    Attributes:
        df (DataFrame): A pandas DataFrame where each row corresponds to a set
                        of y-values at different time points.
        title (str): The title for the plot.
        time_points (array_like): An array of time points corresponding to the
                                  y-values in the dataframe.
    '''

    def __init__(self, df, title, time):
        '''
        The constructor for ExponentialCurve class.
        
        Parameters:
            df (DataFrame): The pandas DataFrame containing the y-values for fitting.
            title (str): The title for the plot.
            time (array_like): The time points for the data.
        '''
        self.df = df
        self.time_points = time
        self.title = title

    def func(self, x, a, b):
        '''
        The exponential function model a * exp(-b * x).
        
        Parameters:
            x (array_like): The independent variable where the model is evaluated.
            a (float): The pre-exponential factor.
            b (float): The rate constant.
            
        Returns:
            array_like: Computed values of the exponential function at 'x'.
        '''
        return a * np.exp(-b * x)

    def fit_curve(self):
        '''
        Fits the exponential curve to the mean of the dataframe's values using
        non-linear least squares optimization.
        
        Returns:
            array_like: The optimized parameters 'a' and 'b' of the model.
        '''
        y = self.df.mean()
        popt, pcov = curve_fit(self.func, self.time_points, y)
        return popt

    def plot_curve(self, out_prefix):
        '''
        Plots the data points, the mean of the data, and the fitted curve. It also
        annotates the plot with the mean data values and saves the plot to an image file.
        
        Parameters:
            out_prefix (str): The file path prefix for the output plot image.
        
        Returns:
            tuple: A tuple containing the mean squared error of the fit, and the
                   optimized parameters 'a' and 'b'.
        '''
        y = self.df.mean()
        t = self.time_points

        # plt.figure(figsize=(16, 8))
        # for index, row in self.df.iterrows():
        #     values = row.values
        #     plt.scatter(t, values, s=2)
        plt.figure(figsize=(10, 6))
        std_dev = self.df.std(numeric_only=True)
        plt.errorbar(t, y, yerr=std_dev, fmt='d', color='blue', 
                 ecolor='lightgray', elinewidth=3, 
                 capsize=0, label='Mean and Standard Deviation')

        xdata = np.linspace(0, max(t), 100)
        # plt.plot(t, y, 'b-', label='data')
        popt = self.fit_curve() 
        a, b = popt
        MSE = mean_squared_error(y, self.func(t, *popt)) 
        plt.plot(xdata, self.func(xdata, *popt), 'r-', label=f'fit: a={a:.3f}, b=-{b:.3f}')

        plt.xlabel('Time (s)', fontsize=18)
        plt.ylabel('Velocity (micrometers/min)', fontsize=18)
        plt.title(f"Exponential Recoil Curve for Cell " + self.title, fontsize=20, fontweight='bold')
        plt.ylim(-5, 20)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12) 
        plt.legend(frameon=True, shadow=True)
        for i, val in enumerate(y):
            plt.text(t[i], val, f'{val:.2f}', color='black', va='center', ha='right', fontsize=12)

        for i, val in enumerate(y):
            plt.text(t[i], val, f'{val:.2f}', color='black', va='center', ha='right', fontsize=12)

        plt.savefig(f"{out_prefix}.expoCurve.png", dpi=1000)
        return MSE, a, b
