import json
import pprint as pp
import networkx as nx
from networkx.readwrite import json_graph
import itertools
import matplotlib.pyplot as plt
from d3graph import d3graph, vec2adjmat
import pandas as pd
import numpy as np

DIRECTORATES_BY_PLACEMENT_NAME = {
    "Adult Social Care Statistics": "Data Services",
    "Business Intelligence/Data Visualisation": "Data Services",
    "Data Management/Engineering": "Data Services",
    "Turing Tribe": "Data Services",
    "Data Quality Dashboards": "Platforms",
    "Spine Core": "Platforms",
    "NHS Pathways - Development Team": "Product Development",
    "NHS Pathways - Reporting Team": "Product Development",
    "111 Online - Developer": "Product Development",
    "Cyber Security": "IT Operations (Including Cyber Security)",
    "Core Infrastructure Services - Networks": "IT Operations (Including Cyber Security)",
    "Core Infrastructure Services - Sustainable Hybrid Cloud": "IT Operations (Including Cyber Security)",
    "Live Services - IT Operations Centre": "IT Operations (Including Cyber Security)",
}

PLACEMENTS_BY_DIRECTORATE_NAME = {
    "Data Services": ["Adult Social Care Statistics",
                      "Business Intelligence/Data Visualisation",
                      "Data Management/Engineering", "Turing Tribe"],
    "Platforms": ["Data Quality Dashboards", "Spine Core"],
    "Product Development": ["NHS Pathways - Development Team",
                            "NHS Pathways - Reporting Team",
                            "111 Online - Developer"],
    "IT Operations (Including Cyber Security)": ["Cyber Security",
                                                 "Core Infrastructure Services - Networks",
                                                 "Core Infrastructure Services - Sustainable Hybrid Cloud",
                                                 "Live Services - IT Operations Centre"]
}


class PreferenceMatcher():

    def __init__(self, preferenceFileName, prevPreferencesFileName) -> None:
        self.readPreferenceFile(preferenceFileName)
        self.readPreviousPreferences(prevPreferencesFileName)

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
        for k in placements:
            if placements[k]["numberOfGrads"] > 1:
                numberedNames = []
                for i in range(1, placements[k]["numberOfGrads"]+1):
                    numberedNames.append(f"{k}_{i}")
                placementNames.extend(numberedNames)
            else:
                placementNames.append(k)
        return placementNames

    def extractPeopleNames(self):
        return [k for k in self.preferences["preferences"]]

    def convertPreferencesToGraph(self):
        preferencesGraph = nx.Graph()
        self.placementNames = self.extractPlacementNames(
            self.preferences["placements"])
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
        if self.preferences["placements"][preference]["numberOfGrads"] > 1:
            for i in range(1, self.preferences["placements"][preference]["numberOfGrads"]+1):
                graph[person][f"{preference}_{i}"]["weight"] += weighting
        else:
            graph[person][preference]["weight"] += weighting

    def removePlacement(self, graph, person, preference):
        if self.preferences["placements"][preference]["numberOfGrads"] > 1:
            for i in range(1, self.preferences["placements"][preference]["numberOfGrads"]+1):
                graph[person][f"{preference}_{i}"]["weight"] = 0
        else:
            graph[person][preference]["weight"] = 0

    def removePreviousDirectoratePlacements(self, graph):
        for k in self.previousPlacements:
            for person in self.peopleNames:
                prevPlacement = self.previousPlacements[k][person]
                prevDirectorate = DIRECTORATES_BY_PLACEMENT_NAME[prevPlacement]
                placementsToRemove = PLACEMENTS_BY_DIRECTORATE_NAME[prevDirectorate]
                for placementToRemove in placementsToRemove:
                    self.removePlacement(
                        graph, person, placementToRemove)

    def applyPreferenceWeighting(self, graph):
        for person in self.peopleNames:
            firstPreference = self.preferences["preferences"][person]["firstPreference"]
            secondPreference = self.preferences["preferences"][person]["secondPreference"]
            thirdPreference = self.preferences["preferences"][person]["thirdPreference"]
            self.weightPlacement(
                graph, person, firstPreference, 175)
            self.weightPlacement(
                graph, person, secondPreference, 100)
            self.weightPlacement(
                graph, person, thirdPreference, 75)


if __name__ == "__main__":
    prefMatcher = PreferenceMatcher(
        "preferences.json", "previousPlacements.json")
    preferenceGraph = prefMatcher.convertPreferencesToGraph()
    prefMatcher.applyPreferenceWeighting(preferenceGraph)
    prefMatcher.removePreviousDirectoratePlacements(preferenceGraph)
    matching = list(nx.max_weight_matching(preferenceGraph))
    for match in matching:
        if match[0] in prefMatcher.peopleNames:
            print(
                f"{match[0]} - {match[1]} - 1st:{prefMatcher.preferences['preferences'][match[0]]['firstPreference']}")
        else:
            print(
                f"{match[1]} - {match[0]} - 1st:{prefMatcher.preferences['preferences'][match[1]]['firstPreference']}")
    # prefMatcher.drawGraph(preferenceGraph)
    nodes = [{'name': str(name), "id": name}
             for i, name in enumerate(preferenceGraph.nodes())]
    links = [{'source': u[0], 'target': u[1], "value": preferenceGraph.edges[u[0], u[1]]["weight"], "weight": preferenceGraph.edges[u[0], u[1]]["weight"]}
             for u in preferenceGraph.edges()]
    nodesWithNeighbours = {node: [
        neighbour for neighbour in preferenceGraph.neighbors(node)] for node in preferenceGraph.nodes()}
    print(nodesWithNeighbours)
    with open('graph.json', 'w') as f:
        json.dump({'nodes': nodes, 'links': links, "people": prefMatcher.peopleNames, "placements": prefMatcher.placementNames, "nodesWithNeighbours": nodesWithNeighbours},
                  f, indent=4,)
