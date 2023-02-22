import csv
from sys import argv
import re
from json import dump
import sys
import yaml

class DataAssurance:    
    def __init__(self) -> None:
         data = {}

    def check_preference_repeat(self, preferenceData):
        flippedData = {}
        for graduate in preferenceData:
            for key, value in preferenceData.items():
                if value in flippedData:
                    self.data = graduate[""]
                else:
                    flippedData[value].append(key)

    def write_yaml_file(filename, self.data):
         with open(filename, 'a') as f:
            yaml.dump_all(self.data, f, default_flow_style=False)
                
