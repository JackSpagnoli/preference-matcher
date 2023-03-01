import csv
from sys import argv
import re
from json import dump
import sys
import yaml

class DataAssurance:    
    def __init__(self) -> None:
         self.data = {}

    def check_preference_repeat(self, preferenceData):
        for graduate in preferenceData:
            flippedData = {}
            for key, value in preferenceData.items():
                if type(value) is list:
                    for antiPreference in value:
                        if antiPreference in flippedData:
                            self.data[graduate] = "There has been repeated preference/antipreference"
                            flippedData[value] = key
                        else:
                            flippedData[value] = key
                if value in flippedData:
                    self.data[graduate] = "There has been repeated preference/antipreference"
                    flippedData[value] = key
                else:
                    flippedData[value] = key
                
    
    def write_yaml_file(self):
         with open("DataAssuranceReport", 'a') as f:
            yaml.dump_all(self.data, f, default_flow_style=False)

   
                
