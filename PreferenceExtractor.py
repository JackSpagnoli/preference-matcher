import csv
from sys import argv
import re
from json import dump
import sys


class PreferenceExtractor:

    def readPreferenceData(self, preferenceFile):
        with open(preferenceFile) as file:
            reader = csv.DictReader(file)

            data = [row for row in reader]
        return data

    def cleanPreferenceData(self, rawPreferenceData):
        cleanData = {}
        for preferenceDatum in rawPreferenceData:
            cleanData[preferenceDatum["What is your name?"]] = {
                "firstPreference": preferenceDatum[
                    "Please select which of the following would be your first choice placement:"
                ],
                "secondPreference": preferenceDatum[
                    "Please select your second choice placement:"
                ],
                "thirdPreference": preferenceDatum[
                    "Finally, please select your third choice placement"
                ],
            }
        
        return cleanData


if __name__ == "__main__":
    print(len(argv))
    if len(argv) < 2:
        print("The preferences csv file must be specified when running the program!")
        sys.exit()
    else:
        preferenceFile = argv[1]
    preferenceExtractor = PreferenceExtractor()
    rawPreferenceData = preferenceExtractor.readPreferenceData(preferenceFile)
    cleanPreferenceData = preferenceExtractor.cleanPreferenceData(rawPreferenceData)
    with open("preferences.json", "w") as file:
        dump(cleanPreferenceData, file)
