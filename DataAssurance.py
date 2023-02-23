import csv
from sys import argv
import re
from json import dump
import sys
import yaml

class DataAssurance:    
    def __init__(self) -> None:
         data = {}

    def check_reason_repeat(self, key):
        #find out actual wording
        if key == "Unwanted placement":
           return ""
        else:
            return "Graduate has added same placement multiple times."

    def check_preference_repeat(self, preferenceData):
        flippedData = {}
        for graduate in preferenceData:
            for key, value in preferenceData.items():
                if value in flippedData:
                    self.data[graduate] = {"Note": self.check_reason_repeat(key)}
                else:
                    flippedData[value] = key
                
    
    def write_yaml_file(self):
         with open("DataAssuranceReport", 'a') as f:
            yaml.dump_all(self.data, f, default_flow_style=False)
                
