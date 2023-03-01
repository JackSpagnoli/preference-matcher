import unittest

from DataAssurance import DataAssurance

class DataAssuranceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dataAssuranceTestJson = {
            "Scott Caldwell-Nichols": {
                "firstPreference": "3 - Pathways",
                "secondPreference": "39 - Innovation and Delivery",
                "thirdPreference": "15 - INSTANT (Solution Assurance)",
                "antiPreference": ["15 - INSTANT (Solution Assurance)",]
            },
            "Mitul Dattani": {
                "firstPreference": "5 - NHS App",
                "secondPreference": "5 - NHS App",
                "thirdPreference": "10 - Spine Core",
                "antiPreference": ["15 - INSTANT (Solution Assurance)"]
            },
            "Kieran Robson": {
                "firstPreference": "5 - NHS App",
                "secondPreference": "3 - Pathways",
                "thirdPreference": "10 - Spine Core",
                "antiPreference": ["15 - INSTANT (Solution Assurance)","10 - Spine Core"]
            },
            "Laura Thrift": {
                "firstPreference": "34 - CSOC",
                "secondPreference": "15 - INSTANT (Solution Assurance)",
                "thirdPreference": "3 - Pathways",
                "antiPreference": ["39 - Innovation and Delivery"]
            },
            "Test person": {
                "firstPreference": "34 - CSOC",
                "secondPreference": "34 - CSOC",
                "thirdPreference": "3 - Pathways",
                "antiPreference": ["39 - Innovation and Delivery", "3 - Pathways"]
            }
        }   

        self.dataAssuranceResultJson = {
            "Scott Caldwell-Nichols": {
                "There has been repeated preference/antipreference"
            },
            "Mitul Dattani": {
                "There has been repeated preference/antipreference"
            },
            "Kieran Robson": {
                "There has been repeated preference/antipreference"
            },
            "Test Person": {
                "There has been repeated preference/antipreference"
            }

        }   
    
    def test_OutputJson(self):
        DataAssuranceBot = DataAssurance()
        DataAssuranceBot.check_preference_repeat(self.DataAssuranceTestJson)
        DataAssuranceBot.data