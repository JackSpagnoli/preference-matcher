import csv
from sys import argv
import re
from json import dump
import sys
import toml


class DataAssurance:
    def __init__(self) -> None:
        self.data = {}

    def check_preference_repeat(self, preferenceData):
        for graduate in preferenceData:
            self.data[graduate] = []
            flippedData = {}
            for key, value in preferenceData[graduate].items():
                if type(value) is list:
                    for antiPreference in value:
                        if antiPreference in flippedData:
                            self.data[graduate].append(
                                "Graduate has put a preference as an antipreference"
                            )
                            flippedData[antiPreference] = key
                        else:
                            flippedData[antiPreference] = key
                elif value in flippedData:
                    self.data[graduate].append("Graduate has repeated preferences")
                    flippedData[value] = key
                else:
                    flippedData[value] = key

    def write_toml_file(self):
        toml_config = toml.dumps(self.data)

        with open("DataAssuranceReport", "a") as f:
            f.write(toml_config)
