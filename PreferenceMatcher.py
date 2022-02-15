import json
import pprint as pp
import networkx as nx
import itertools
import matplotlib.pyplot as plt


class PreferenceMatcher():

    def readPreferenceFile(self):
        preferenceFile = open("preferences.json", "r")
        preferences = json.load(preferenceFile)
        preferenceFile.close()
        return preferences

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

    def extractPeopleNames(self, preferences):
        return [k for k in preferences]

    def convertPreferencesToGraph(self, preferences):
        preferencesGraph = nx.Graph()
        self.placementNames = self.extractPlacementNames(
            preferences["placements"])
        self.peopleNames = self.peopleNames = self.extractPeopleNames(
            preferences["preferences"])
        preferencesGraph.add_nodes_from(self.placementNames)
        preferencesGraph.add_nodes_from(self.peopleNames)
        preferencesGraph.add_edges_from(
            list(itertools.product(self.peopleNames, self.placementNames)), weight=100)
        return preferencesGraph

    def drawGraph(self, graph):
        nx.draw(graph, with_labels=True)
        pos = nx.spring_layout(graph)
        labels = {e: graph.edges[e]["weight"] for e in graph.edges}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        plt.show()

    def weightPlacement(self, graph, person, preferences, preference, weighting):
        if preferences["placements"][preference]["numberOfGrads"] > 1:
            for i in range(1, preferences["placements"][preference]["numberOfGrads"]+1):
                graph[person][f"{preference}_{i}"]["weight"] += weighting
        else:
            graph[person][preference]["weight"] += weighting

    def applyPreferenceWeighting(self, graph, preferences):
        for person in self.peopleNames:
            firstPreference = preferences["preferences"][person]["firstPreference"]
            secondPreference = preferences["preferences"][person]["secondPreference"]
            thirdPreference = preferences["preferences"][person]["thirdPreference"]
            self.weightPlacement(
                graph, person, preferences, firstPreference, 75)
            self.weightPlacement(
                graph, person, preferences, secondPreference, 50)
            self.weightPlacement(
                graph, person, preferences, thirdPreference, 25)


if __name__ == "__main__":
    prefMatcher = PreferenceMatcher()
    preferences = prefMatcher.readPreferenceFile()
    preferenceGraph = prefMatcher.convertPreferencesToGraph(preferences)
    prefMatcher.drawGraph(preferenceGraph)
    prefMatcher.applyPreferenceWeighting(preferenceGraph, preferences)
    prefMatcher.drawGraph(preferenceGraph)
    pp.pprint(nx.max_weight_matching(preferenceGraph))
