import unittest
import networkx as nx
from PreferenceMatcher import PreferenceMatcher


class PreferenceMatcherTest(unittest.TestCase):
    def setUp(self) -> None:
        self.preferenceMatcher = PreferenceMatcher(
            "simplifiedPreferences.json", "previousPlacements.json"
        )
        self.preferencesObj = {
            "placements": {
                "Adult Social Care Statistics": {
                    "directorate": "Data Services",
                    "numberOfGrads": 1,
                },
                "Business Intelligence/Data Visualisation": {
                    "directorate": "Data Services",
                    "numberOfGrads": 1,
                },
                "Data Management/Engineering": {
                    "directorate": "Data Services",
                    "numberOfGrads": 2,
                },
                "Turing Tribe": {"directorate": "Data Services", "numberOfGrads": 1},
                "Data Quality Dashboards": {
                    "directorate": "Platforms",
                    "numberOfGrads": 2,
                },
                "Spine Core": {"directorate": "Platforms", "numberOfGrads": 3},
                "NHS Pathways - Development Team": {
                    "directorate": "Product Development",
                    "numberOfGrads": 1,
                },
                "NHS Pathways - Reporting Team": {
                    "directorate": "Product Development",
                    "numberOfGrads": 1,
                },
                "111 Online - Developer": {
                    "directorate": "Product Development",
                    "numberOfGrads": 1,
                },
                "Cyber Security": {
                    "directorate": "IT Operations (Including Cyber Security)",
                    "numberOfGrads": 1,
                },
                "Core Infrastructure Services - Networks": {
                    "directorate": "IT Operations (Including Cyber Security)",
                    "numberOfGrads": 1,
                },
                "Core Infrastructure Services - Sustainable Hybrid Cloud": {
                    "directorate": "IT Operations (Including Cyber Security)",
                    "numberOfGrads": 1,
                },
                "Live Services - IT Operations Centre": {
                    "directorate": "IT Operations (Including Cyber Security)",
                    "numberOfGrads": 2,
                },
            },
            "preferences": {
                "Amaan Ibn-Nasar": {
                    "firstPreference": "Spine Core",
                    "secondPreference": "Adult Social Care Statistics",
                    "thirdPreference": "111 Online - Developer",
                },
                "Abbie Prescott": {
                    "firstPreference": "Live Services - IT Operations Centre",
                    "secondPreference": "Cyber Security",
                    "thirdPreference": "Data Quality Dashboards",
                },
                "Adam Carruthers": {
                    "firstPreference": "Core Infrastructure Services - Networks",
                    "secondPreference": "Spine Core",
                    "thirdPreference": "111 Online - Developer",
                },
                "Alice Tapper": {
                    "firstPreference": "Business Intelligence/Data Visualisation",
                    "secondPreference": "Cyber Security",
                    "thirdPreference": "Turing Tribe",
                },
                "Amelia Noonan": {
                    "firstPreference": "Data Quality Dashboards",
                    "secondPreference": "Business Intelligence/Data Visualisation",
                    "thirdPreference": "Cyber Security",
                },
                "Anna Evans": {
                    "firstPreference": "Cyber Security",
                    "secondPreference": "Turing Tribe",
                    "thirdPreference": "NHS Pathways - Development Team",
                },
                "Benjamin Wallace": {
                    "firstPreference": "Adult Social Care Statistics",
                    "secondPreference": "111 Online - Developer",
                    "thirdPreference": "Spine Core",
                },
                "Joel Helbling": {
                    "firstPreference": "NHS Pathways - Development Team",
                    "secondPreference": "Cyber Security",
                    "thirdPreference": "Turing Tribe",
                },
                "Joseph Wilson": {
                    "firstPreference": "Spine Core",
                    "secondPreference": "Data Quality Dashboards",
                    "thirdPreference": "Core Infrastructure Services - Networks",
                },
                "Laura Thirft": {
                    "firstPreference": "Data Management/Engineering",
                    "secondPreference": "NHS Pathways - Reporting Team",
                    "thirdPreference": "Core Infrastructure Services - Networks",
                },
                "Maisie Blyth": {
                    "firstPreference": "Spine Core",
                    "secondPreference": "Turing Tribe",
                    "thirdPreference": "Core Infrastructure Services - Sustainable Hybrid Cloud",
                },
                "Mitul Dattani": {
                    "firstPreference": "Core Infrastructure Services - Sustainable Hybrid Cloud",
                    "secondPreference": "Data Quality Dashboards",
                    "thirdPreference": "Spine Core",
                },
                "Nathan Gregory": {
                    "firstPreference": "Live Services - IT Operations Centre",
                    "secondPreference": "Data Management/Engineering",
                    "thirdPreference": "Cyber Security",
                },
                "Nathan Pettit": {
                    "firstPreference": "111 Online - Developer",
                    "secondPreference": "Spine Core",
                    "thirdPreference": "Turing Tribe",
                },
                "Oluwadamiloju Makinde": {
                    "firstPreference": "Data Quality Dashboards",
                    "secondPreference": "Business Intelligence/Data Visualisation",
                    "thirdPreference": "Turing Tribe",
                },
                "Roshaan Bajwa": {
                    "firstPreference": "Turing Tribe",
                    "secondPreference": "Spine Core",
                    "thirdPreference": "Cyber Security",
                },
                "Scott Caldwell-Nichols": {
                    "firstPreference": "Data Management/Engineering",
                    "secondPreference": "NHS Pathways - Reporting Team",
                    "thirdPreference": "Spine Core",
                },
                "Zahra Ahmed": {
                    "firstPreference": "NHS Pathways - Reporting Team",
                    "secondPreference": "111 Online - Developer",
                    "thirdPreference": "Data Management/Engineering",
                },
            },
        }
        self.simplifiedPreferencesObj = {
            "placements": {
                "Adult Social Care Statistics": {
                    "directorate": "Data Services",
                    "numberOfGrads": 1,
                },
                "Business Intelligence/Data Visualisation": {
                    "directorate": "Data Services",
                    "numberOfGrads": 1,
                },
                "Turing Tribe": {"directorate": "Data Services", "numberOfGrads": 1},
                "Spine Core": {"directorate": "Platforms", "numberOfGrads": 3},
                "111 Online - Developer": {
                    "directorate": "Product Development",
                    "numberOfGrads": 1,
                },
                "Cyber Security": {
                    "directorate": "IT Operations (Including Cyber Security)",
                    "numberOfGrads": 1,
                },
            },
            "preferences": {
                "Amaan Ibn-Nasar": {
                    "firstPreference": "Spine Core",
                    "secondPreference": "Adult Social Care Statistics",
                    "thirdPreference": "111 Online - Developer",
                },
                "Alice Tapper": {
                    "firstPreference": "Business Intelligence/Data Visualisation",
                    "secondPreference": "Cyber Security",
                    "thirdPreference": "Turing Tribe",
                },
            },
        }
        self.preferencesGraph = self.preferenceMatcher.convertPreferencesToGraph()

    def test_addPlacementNodesToGraph(self):
        placements = [
            "Adult Social Care Statistics",
            "Business Intelligence/Data Visualisation",
            "Turing Tribe",
            "Spine Core_1",
            "Spine Core_2",
            "Spine Core_3",
            "111 Online - Developer",
            "Cyber Security",
        ]
        actualPlacements = self.preferenceMatcher.extractPlacementNames(
            self.simplifiedPreferencesObj["placements"]
        )
        self.assertEqual(placements, actualPlacements)

    def test_addPeopleNodesToGraph(self):
        people = ["Amaan Ibn-Nasar", "Alice Tapper"]
        actualPeople = self.preferenceMatcher.extractPeopleNames()
        self.assertEqual(people, actualPeople)

    def test_convertPlacementsToGraph(self):
        expectedEdges = [
            ("Adult Social Care Statistics", "Amaan Ibn-Nasar"),
            ("Adult Social Care Statistics", "Alice Tapper"),
            ("Business Intelligence/Data Visualisation", "Amaan Ibn-Nasar"),
            ("Business Intelligence/Data Visualisation", "Alice Tapper"),
            ("Data Management/Engineering_1", "Amaan Ibn-Nasar"),
            ("Data Management/Engineering_1", "Alice Tapper"),
            ("Data Management/Engineering_2", "Amaan Ibn-Nasar"),
            ("Data Management/Engineering_2", "Alice Tapper"),
            ("Turing Tribe", "Amaan Ibn-Nasar"),
            ("Turing Tribe", "Alice Tapper"),
            ("Data Quality Dashboards_1", "Amaan Ibn-Nasar"),
            ("Data Quality Dashboards_1", "Alice Tapper"),
            ("Data Quality Dashboards_2", "Amaan Ibn-Nasar"),
            ("Data Quality Dashboards_2", "Alice Tapper"),
            ("Spine Core_1", "Amaan Ibn-Nasar"),
            ("Spine Core_1", "Alice Tapper"),
            ("Spine Core_2", "Amaan Ibn-Nasar"),
            ("Spine Core_2", "Alice Tapper"),
            ("Spine Core_3", "Amaan Ibn-Nasar"),
            ("Spine Core_3", "Alice Tapper"),
            ("NHS Pathways - Development Team", "Amaan Ibn-Nasar"),
            ("NHS Pathways - Development Team", "Alice Tapper"),
            ("NHS Pathways - Reporting Team", "Amaan Ibn-Nasar"),
            ("NHS Pathways - Reporting Team", "Alice Tapper"),
            ("111 Online - Developer", "Amaan Ibn-Nasar"),
            ("111 Online - Developer", "Alice Tapper"),
            ("Cyber Security", "Amaan Ibn-Nasar"),
            ("Cyber Security", "Alice Tapper"),
            ("Core Infrastructure Services - Networks", "Amaan Ibn-Nasar"),
            ("Core Infrastructure Services - Networks", "Alice Tapper"),
            (
                "Core Infrastructure Services - Sustainable Hybrid Cloud",
                "Amaan Ibn-Nasar",
            ),
            ("Core Infrastructure Services - Sustainable Hybrid Cloud", "Alice Tapper"),
            ("Live Services - IT Operations Centre_1", "Amaan Ibn-Nasar"),
            ("Live Services - IT Operations Centre_1", "Alice Tapper"),
            ("Live Services - IT Operations Centre_2", "Amaan Ibn-Nasar"),
            ("Live Services - IT Operations Centre_2", "Alice Tapper"),
        ]
        self.assertEqual(list(self.preferencesGraph.edges()), expectedEdges)

    def test_applyPreferenceWeighting(self):
        self.preferenceMatcher.applyPreferenceWeighting(self.preferencesGraph)
        amaanWeights = [
            v["weight"] for _, v in self.preferencesGraph["Amaan Ibn-Nasar"].items()
        ]
        aliceWeights = [
            v["weight"] for _, v in self.preferencesGraph["Alice Tapper"].items()
        ]
        self.assertEqual(
            [
                150,
                100,
                100,
                100,
                100,
                100,
                100,
                175,
                175,
                175,
                100,
                100,
                125,
                100,
                100,
                100,
                100,
                100,
            ],
            amaanWeights,
        )
        self.assertEqual(
            [
                100,
                175,
                100,
                100,
                125,
                100,
                100,
                100,
                100,
                100,
                100,
                100,
                100,
                150,
                100,
                100,
                100,
                100,
            ],
            aliceWeights,
        )

    def test_weightPlacement(self):
        self.preferenceMatcher.weightPlacement(
            self.preferencesGraph, "Amaan Ibn-Nasar", "Spine Core", 75
        )
        amaanWeights = [
            v["weight"] for _, v in self.preferencesGraph["Amaan Ibn-Nasar"].items()
        ]
        self.assertEqual(
            [
                100,
                100,
                100,
                100,
                100,
                100,
                100,
                175,
                175,
                175,
                100,
                100,
                100,
                100,
                100,
                100,
                100,
                100,
            ],
            amaanWeights,
        )
        self.preferenceMatcher.weightPlacement(
            self.preferencesGraph, "Amaan Ibn-Nasar", "Adult Social Care Statistics", 50
        )
        amaanWeights = [
            v["weight"] for _, v in self.preferencesGraph["Amaan Ibn-Nasar"].items()
        ]
        self.assertEqual(
            [
                150,
                100,
                100,
                100,
                100,
                100,
                100,
                175,
                175,
                175,
                100,
                100,
                100,
                100,
                100,
                100,
                100,
                100,
            ],
            amaanWeights,
        )

    def test_removePreviousDirectoratePlacements(self):
        self.preferenceMatcher.removePreviousDirectoratePlacements(
            self.preferencesGraph
        )
        amaanWeights = [
            v["weight"] for _, v in self.preferencesGraph["Amaan Ibn-Nasar"].items()
        ]
        self.assertEqual(5, amaanWeights.count(0))


if __name__ == "__main__":
    unittest.main()
