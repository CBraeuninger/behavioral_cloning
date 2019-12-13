'''
Class for input data sets
'''

import csv

class DataSet:
    
    # Constructor
    def __init__(self, csv_path):
        
        self._csv_path = csv_path
        self._lines = self._read_lines() 
    
    # read the lines in the csv file
    def _read_lines(self):
    
        lines = []
        with open(self._csv_path) as csvfile:
            reader = csv.reader(csvfile)
            for ind, line in enumerate(reader):
                # first line is header, so ignore it
                if ind!=0:
                    lines.append(line)
                
        return lines
    
    # Getter for lines
    def get_lines(self):
        return self._lines