import json
import pprint as pp
import re
import sys
import networkx as nx
import itertools
import matplotlib.pyplot as plt

PLACEMENTS_BY_DIRECTORATE_NAME = {
    "Data Services": [
        "0 - Babbage Squad - Archimedes Tribe",
        "1 - Turing squad",
        "3 - Nightingale squad",
        "6 - SDE Platform Team",
        "8 - Analytical Services: Population Health, Clinical Audit and Specialist Care (Seacole squad)",
        "9 - Lovelace Squad",
        "10 - Data Visualisation & Insights - Analytical Insights Service",
        "11 - Cohorting & Data Linkage - Analytical Insights Service",
        "12 - Lovelace (in Archimedes tribe)",
        "20 - Data Science Skilled Team - MPS",
        "21 - Data Science / Artificial Data",
        "22 - Data Science / RAP",
        "23 - Data Science / Business Intelligence",
        "24 - Data Science / covid patient pathways",
        "25 - Data Science / TRE Data Wranglers",
        "28 - Analytical Insights",
        "29 - Data Engineering",
    ],
    "Product Development": [
        "2 - Management Information Team",
        "4 - Digital Transformation of Screening",
        "5 - Bowel Cancer Screening",
        "7 - Screening Programme (Digital Transformation of Screening and Live Screening Services)",
        "14 - DoS & DoS Integration team",
        "15 - DoS Integration",
        "16 - Developer / DoS Features",
        "17 - Test / DoS Features / Live Service",
        "18 - 111 online",
        "19 - 111 online",
        "26 - Vaccinations Programme, Tech & Data Delivery Team",
        "27 - Vaccinations - National Booking Service",
        "30 - UEC Data, Digital Urgent & Emergency Care",
        "31 - Child Protection Information Sharing (CP-IS)",
    ],
    "IT Operations": ["13 - ITOC Onboarding / Development ", "36 - Infra Ops"],
    "Platforms": [
        "32 - Electronic Prescription Service (Team Epsilon)",
        "33 - API Management ",
        "34 - API Management",
        "35 - Primary Care Registration Management",
    ],
    "Cyber Operations": [
        "37 - Specialist Security Services",
        "38 - Cyber Security Operations Centre (CSOC)",
    ],
}


class PreferenceMatcher:
    def __init__(
        self, preferenceFileName, prevPreferencesFileName, placementFileName
    ) -> None:
        self.readPreferenceFile(preferenceFileName)
        self.readPreviousPreferences(prevPreferencesFileName)
        self.readPlacementsFile(placementFileName)
        self.createTagDataStructure()

    def createTagDataStructure(self):
        self.placementsByTag = {}
        for placementName, placementData in self.placements.items():
            for tag in placementData["tags"]:
                if tag in self.placementsByTag:
                    self.placementsByTag[tag].append(placementName)
                else:
                    self.placementsByTag[tag] = [placementName]

    def readPlacementsFile(self, placementFileName):
        placementsFile = open(placementFileName, "r")
        self.placements = json.load(placementsFile)
        placementsFile.close()

    def readPreferenceFile(self, preferenceFileName):
        preferenceFile = open(preferenceFileName, "r")
        self.preferences = json.load(preferenceFile)
        preferenceFile.close()

    def readPreviousPreferences(self, prevPreferencesFileName):
        prevPreferenceFile = open(prevPreferencesFileName, "r")
        self.previousPlacements = json.load(prevPreferenceFile)
        prevPreferenceFile.close()

    def extractPlacementNames(self, placements):
        placementNames = []
        for placementName, placementData in placements.items():
            if placementData["numberOfGrads"] > 1:
                numberedNames = []
                for i in range(1, placements[placementName]["numberOfGrads"] + 1):
                    numberedNames.append(f"{placementName}_{i}")
                placementNames.extend(numberedNames)
            else:
                placementNames.append(placementName)
        return placementNames

    def extractPeopleNames(self):
        return [k for k in self.preferences]

    def convertPreferencesToGraph(self):
        preferencesGraph = nx.Graph()
        self.placementNames = self.extractPlacementNames(self.placements)
        self.peopleNames = self.peopleNames = self.extractPeopleNames()
        preferencesGraph.add_nodes_from(self.placementNames)
        preferencesGraph.add_nodes_from(self.peopleNames)
        preferencesGraph.add_edges_from(
            list(itertools.product(self.peopleNames, self.placementNames)), weight=50
        )
        return preferencesGraph

    def drawGraph(self, graph):
        nx.draw(graph, with_labels=True)
        pos = nx.kamada_kawai_layout(graph)
        labels = {e: graph.edges[e]["weight"] for e in graph.edges}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        plt.show()

    def weightPlacement(self, graph, person, placementsToWeight, weighting):
        for placementName in placementsToWeight:
            graph[person][placementName]["weight"] += weighting

    def removePlacement(self, graph, person, preference):
        if self.placements[preference]["numberOfGrads"] > 1:
            for i in range(1, self.placements[preference]["numberOfGrads"] + 1):
                graph.remove_edge(person, f"{preference}_{i}")
        else:
            graph.remove_edge(person, preference)

    def removePreviousDirectoratePlacements(self, graph):
        for k in self.previousPlacements:
            for person in self.peopleNames:
                prevDirectorate = self.previousPlacements[k][person]
                placementsToRemove = PLACEMENTS_BY_DIRECTORATE_NAME[prevDirectorate]
                for placementToRemove in placementsToRemove:
                    self.removePlacement(graph, person, placementToRemove)

    def extractPlacementsFromPreference(self, preference):
        placementsToWeight = []
        placementsToCheckNumOfGrads = []
        preferenceIsATag = preference in self.placementsByTag
        if preferenceIsATag:
            placementsToCheckNumOfGrads.extend(self.placementsByTag[preference])
        else:
            placementsToCheckNumOfGrads.append(preference)
        for placementToCheck in placementsToCheckNumOfGrads:
            placementCanTakeMultipleGrads = (
                self.placements[placementToCheck]["numberOfGrads"] > 1
            )
            if placementCanTakeMultipleGrads:
                for i in range(
                    1, self.placements[placementToCheck]["numberOfGrads"] + 1
                ):
                    placementsToWeight.append(f"{placementToCheck}_{i}")
            else:
                placementsToWeight.append(placementToCheck)
        return placementsToWeight

    def applyPreferenceWeighting(self, graph, weightings):
        for person in self.peopleNames:
            firstPlacementsToWeight = self.extractPlacementsFromPreference(
                self.preferences[person]["firstPreference"]
            )
            secondPlacementsToWeight = self.extractPlacementsFromPreference(
                self.preferences[person]["secondPreference"]
            )
            thirdPlacementsToWeight = self.extractPlacementsFromPreference(
                self.preferences[person]["thirdPreference"]
            )
            secondPlacementsWithDuplicatePlacementsRemoved = [
                placement
                for placement in secondPlacementsToWeight
                if placement not in firstPlacementsToWeight
            ]
            thirdPlacementsWithDuplicatePlacementsRemoved = [
                placement
                for placement in thirdPlacementsToWeight
                if (
                    placement not in firstPlacementsToWeight
                    and placement not in secondPlacementsToWeight
                )
            ]
            self.weightPlacement(graph, person, firstPlacementsToWeight, weightings[0])
            self.weightPlacement(
                graph,
                person,
                secondPlacementsWithDuplicatePlacementsRemoved,
                weightings[1],
            )
            self.weightPlacement(
                graph,
                person,
                thirdPlacementsWithDuplicatePlacementsRemoved,
                weightings[2],
            )


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Weightings must be given in a list format e.g 100 75 50")
        sys.exit()
    else:
        weightings = [
            int(weighting) for weighting in [sys.argv[1], sys.argv[2], sys.argv[3]]
        ]
    prefMatcher = PreferenceMatcher(
        "preferences.json", "previousPlacements.json", "placements.json"
    )
    preferenceGraph = prefMatcher.convertPreferencesToGraph()
    prefMatcher.applyPreferenceWeighting(preferenceGraph, weightings)
    prefMatcher.removePreviousDirectoratePlacements(preferenceGraph)
    matching = list(nx.max_weight_matching(preferenceGraph))
    for i, match in enumerate(matching):
        if not match[0] in prefMatcher.peopleNames:
            matching[i] = (match[1], match[0])
    no_preference_matchings = []
    with open(f"preferenceOutput-{weightings}.txt", "w") as file:

        for match in matching:
            if re.sub(r"_\d", "", match[1]) not in [
                prefMatcher.preferences[match[0]]["firstPreference"],
                prefMatcher.preferences[match[0]]["secondPreference"],
                prefMatcher.preferences[match[0]]["thirdPreference"],
            ]:
                no_preference_matchings.append(match)
            file.write(
                f"""\n{match[0]} -> {match[1]}:
                    1st:{prefMatcher.preferences[match[0]]['firstPreference']}
                    2nd:{prefMatcher.preferences[match[0]]['secondPreference']}
                    3rd:{prefMatcher.preferences[match[0]]['thirdPreference']}"""
            )

        file.write("\nNo Preference Matched:")
        for match in no_preference_matchings:
            file.write(f"{match[0]} -> {match[1]}")
    nodes = [
        {"name": str(name), "id": name}
        for i, name in enumerate(preferenceGraph.nodes())
    ]
    links = [
        {
            "source": u[0],
            "target": u[1],
            "value": preferenceGraph.edges[u[0], u[1]]["weight"],
            "weight": preferenceGraph.edges[u[0], u[1]]["weight"],
        }
        for u in preferenceGraph.edges()
    ]
    nodesWithNeighbours = {
        node: [neighbour for neighbour in preferenceGraph.neighbors(node)]
        for node in preferenceGraph.nodes()
    }
    with open(f"graph{weightings}.json", "w") as f:
        json.dump(
            {
                "nodes": nodes,
                "links": links,
                "people": prefMatcher.peopleNames,
                "placements": prefMatcher.placementNames,
                "nodesWithNeighbours": nodesWithNeighbours,
            },
            f,
            indent=4,
        )
