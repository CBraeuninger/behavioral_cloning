'''
Class for samples of input data
'''

import csv

class Sample:
    
    # constructor
    def __init__(self, line, images_path, correction_factor):
        
        self._line = line
        self._images_path = images_path
        self._correction_factor = correction_factor
        
    
    # getter for path to images folder
    def get_images_path(self):
        return self._images_path
    
    # getter for correction factor
    def get_correction_factor(self):
        return self._correction_factor
    
    # getter for line data
    def get_line(self):
        return self._line
    
        