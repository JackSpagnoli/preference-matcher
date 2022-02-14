import json


class PreferenceMatcher():
  
  def readPreferenceFile(self):
    preferenceFile = open("preferences.json", "r")
    preferences = json.load(preferenceFile)
    preferenceFile.close()
    return preferences
  
  
if __name__ == "__main__":
  pass