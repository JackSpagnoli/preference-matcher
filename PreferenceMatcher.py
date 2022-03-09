import json
import pprint as pp
import re
import sys
import networkx as nx
from networkx.readwrite import json_graph
import itertools
import matplotlib.pyplot as plt
from d3graph import d3graph, vec2adjmat
import pandas as pd
import numpy as np

PLACEMENTS_BY_DIRECTORATE_NAME = {
    "Data Services": ["17 - Data Science Skilled Team",
                      "18 - Adult Social Care Statistics",
                      "19 - Business Intelligence (Dashboard) Team",
                      "20 - Information Standards",
                      "21 - Publications and Adhocs Development Team (Seacole Squad) in the Analytical Serivces: Population Health, Clinical Audit and Specialist Care tribe.",
                      "22 - Secondary Care Scheduled Release Team",
                      "23 - Analytical Insights (COVID Squad)",
                      "24 - Lovelace squad (Archimedes tribe)",
                      "25 - Analytical Insights (Prescribing)",
                      "26 - SPL/Enhanced Protection Programme",
                      "27 - Analytical Insight - Analytical Delivery Squad Number 2",
                      "28 - Primary Care Domain",
                      "29 - Various, within Data Engineering Skilled Team and as assigned by HoST for Data Engineering",
                      "30 - Burden Reduction (automated data extraction + data ingest transformation programmes)",
                      "31 - Population Health, Clinical Audit and Specialist Care (Turing Tribe)",
                      "32 - Lovelace squad within Archimedes tribe",
                      "33 - Babbage squad (in the Archimedes tribe)"],
    "Platforms": ["10 - Spine Core",
                  "11 - Development Office",
                  "12 - Risk Stratification",
                  "13 - Business Operations", "40 - Risk Stratification"],
    "Product Development": ["1 - NHS.UK",
                            "2 - 111 online (UEC Digital Services)",
                            "3 - Pathways",
                            "4 - Content Modularisation Team (NHS UK)",
                            "5 - NHS App",
                            "7 - NHS Pathways",
                            "8 - DoS Suite of products (Urgent & Emergency Care directorate)",
                            "9 - Management Information Team, Product Implementation (PIRM)",
                            "43 - Delivery Management Team, NHS Pathways",
                            "45 - National Vaccination Booking Service",
                            "46 - NHS.UK Campaigns Team",
                            "47 - Clinical Safety"],
    "IT Operations": ["14 - Cloud Centre of Excellence (Infrastructure Services)",
                      "15 - INSTANT (Solution Assurance)",
                      "16 - ITOC",
                      "35 - Sub directorate: Core Infrastructure services- (Team: Infra Operations)",
                      "37 - Data Operations Team",
                      "38 - Future Connectivity (Infrastructure Services)",
                      "41 - Vulnerability and Patching Team (Infrastructure Services)"],
    "Cyber Security": ["34 - CSOC",
                       "39 - Innovation and Delivery"],
    "Assurance and Risk Management": ["42 - CPMO Standards & Investment",
                                      "44 - Medical Device Directive Programme"]
}


class PreferenceMatcher():

    def __init__(self, preferenceFileName, prevPreferencesFileName, placementFileName) -> None:
        self.readPreferenceFile(preferenceFileName)
        self.readPreviousPreferences(prevPreferencesFileName)
        self.readPlacementsFile(placementFileName)

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
                for i in range(1, placements[placementName]["numberOfGrads"]+1):
                    numberedNames.append(f"{placementName}_{i}")
                placementNames.extend(numberedNames)
            else:
                placementNames.append(placementName)
        return placementNames

    def extractPeopleNames(self):
        return [k for k in self.preferences]

    def convertPreferencesToGraph(self):
        preferencesGraph = nx.Graph()
        self.placementNames = self.extractPlacementNames(
            self.placements)
        self.peopleNames = self.peopleNames = self.extractPeopleNames()
        preferencesGraph.add_nodes_from(self.placementNames)
        preferencesGraph.add_nodes_from(self.peopleNames)
        preferencesGraph.add_edges_from(
            list(itertools.product(self.peopleNames, self.placementNames)), weight=50)
        return preferencesGraph

    def drawGraph(self, graph):
        nx.draw(graph, with_labels=True)
        pos = nx.kamada_kawai_layout(graph)
        labels = {e: graph.edges[e]["weight"] for e in graph.edges}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        plt.show()

    def weightPlacement(self, graph, person, preference, weighting):
        if self.placements[preference]["numberOfGrads"] > 1:
            for i in range(1, self.placements[preference]["numberOfGrads"]+1):
                graph[person][f"{preference}_{i}"]["weight"] += weighting
        else:
            graph[person][preference]["weight"] += weighting

    def removePlacement(self, graph, person, preference):
        if self.placements[preference]["numberOfGrads"] > 1:
            for i in range(1, self.placements[preference]["numberOfGrads"]+1):
                graph.remove_edge(person, f"{preference}_{i}")
        else:
            graph.remove_edge(person, preference)

    def removePreviousDirectoratePlacements(self, graph):
        for k in self.previousPlacements:
            for person in self.peopleNames:
                prevDirectorate = self.previousPlacements[k][person]
                placementsToRemove = PLACEMENTS_BY_DIRECTORATE_NAME[prevDirectorate]
                for placementToRemove in placementsToRemove:
                    self.removePlacement(
                        graph, person, placementToRemove)

    def applyPreferenceWeighting(self, graph, weightings):
        for person in self.peopleNames:
            firstPreference = self.preferences[person]["firstPreference"]
            secondPreference = self.preferences[person]["secondPreference"]
            thirdPreference = self.preferences[person]["thirdPreference"]
            self.weightPlacement(
                graph, person, firstPreference, weightings[0])
            self.weightPlacement(
                graph, person, secondPreference, weightings[1])
            self.weightPlacement(
                graph, person, thirdPreference, weightings[2])


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Weightings must be given in a list format e.g [100, 75, 50]")
        sys.exit()
    else:
        weightings = [int(weighting) for weighting in [
            sys.argv[1], sys.argv[2], sys.argv[3]]]
    prefMatcher = PreferenceMatcher(
        "preferences.json", "previousPlacements.json", "placements.json")
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
            if re.sub(r"_\d", "", match[1]) not in [prefMatcher.preferences[match[0]]['firstPreference'], prefMatcher.preferences[match[0]]['secondPreference'], prefMatcher.preferences[match[0]]['thirdPreference']]:
                no_preference_matchings.append(match)
            file.write(f"""\n{match[0]} -> {match[1]}:
                    1st:{prefMatcher.preferences[match[0]]['firstPreference']}
                    2nd:{prefMatcher.preferences[match[0]]['secondPreference']}
                    3rd:{prefMatcher.preferences[match[0]]['thirdPreference']}""")

        file.write("\nNo Preference Matched:")
        for match in no_preference_matchings:
            file.write(f"{match[0]} -> {match[1]}")
    nodes = [{'name': str(name), "id": name}
             for i, name in enumerate(preferenceGraph.nodes())]
    links = [{'source': u[0], 'target': u[1], "value": preferenceGraph.edges[u[0], u[1]]["weight"], "weight": preferenceGraph.edges[u[0], u[1]]["weight"]}
             for u in preferenceGraph.edges()]
    nodesWithNeighbours = {node: [
        neighbour for neighbour in preferenceGraph.neighbors(node)] for node in preferenceGraph.nodes()}
    with open(f'graph{weightings}.json', 'w') as f:
        json.dump({'nodes': nodes, 'links': links, "people": prefMatcher.peopleNames, "placements": prefMatcher.placementNames, "nodesWithNeighbours": nodesWithNeighbours},
                  f, indent=4,)
