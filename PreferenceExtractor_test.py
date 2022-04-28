import unittest
from PreferenceExtractor import PreferenceExtractor


class PreferenceExtractorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.preferenceExtractor = PreferenceExtractor()

    def test_readPreferenceData(self):
        self.assertEqual(
            [
                {
                    "Timestamp": "3/4/2022 16:48:54",
                    "What is your name?": "Mia Noonan",
                    "Please select your previous directorate for your first placement": "Platforms",
                    "Please select which of the following would be your first choice placement:": "17 - Data Science Skilled Team",
                    "Please select your second choice placement:": "22 - Secondary Care Scheduled Release Team",
                    "Finally, please select your third choice placement": "3 - Pathways",
                },
                {
                    "Timestamp": "3/7/2022 14:13:17",
                    "What is your name?": "Nathan",
                    "Please select your previous directorate for your first placement": "Product Development",
                    "Please select which of the following would be your first choice placement:": "14 - Cloud Centre of Excellence (Infrastructure Services)",
                    "Please select your second choice placement:": "39 - Innovation and Delivery",
                    "Finally, please select your third choice placement": "29 - Various, within Data Engineering Skilled Team and as assigned by HoST for Data Engineering",
                },
                {
                    "Timestamp": "3/7/2022 14:13:58",
                    "What is your name?": "Joe Wilson",
                    "Please select your previous directorate for your first placement": "Platforms",
                    "Please select which of the following would be your first choice placement:": "3 - Pathways",
                    "Please select your second choice placement:": "34 - CSOC",
                    "Finally, please select your third choice placement": "19 - Business Intelligence (Dashboard) Team",
                },
            ],
            self.preferenceExtractor.readPreferenceData(
                "PreferenceResponsesSimplified.csv"
            ),
        )

    def test_cleanPreferenceData(self):
        rawPreferenceData = self.preferenceExtractor.readPreferenceData(
            "PreferenceResponsesSimplified.csv"
        )
        self.assertEqual(
            {
                "Mia Noonan": {
                    "firstPreference": "17 - Data Science Skilled Team",
                    "secondPreference": "22 - Secondary Care Scheduled Release Team",
                    "thirdPreference": "3 - Pathways",
                },
                "Nathan": {
                    "firstPreference": "14 - Cloud Centre of Excellence (Infrastructure Services)",
                    "secondPreference": "39 - Innovation and Delivery",
                    "thirdPreference": "29 - Various, within Data Engineering Skilled Team and as assigned by HoST for Data Engineering",
                },
                "Joe Wilson": {
                    "firstPreference": "3 - Pathways",
                    "secondPreference": "34 - CSOC",
                    "thirdPreference": "19 - Business Intelligence (Dashboard) Team",
                },
            },
            self.preferenceExtractor.cleanPreferenceData(rawPreferenceData),
        )


if __name__ == "__main__":
    unittest.main()
