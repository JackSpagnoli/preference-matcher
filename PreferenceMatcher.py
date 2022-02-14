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

    def applyPreferenceWeighting(self, graph, preferences):
        for person in self.peopleNames:
            firstPreference = preferences["preferences"][person]["firstPreference"]
            secondPreference = preferences["preferences"][person]["secondPreference"]
            thirdPreference = preferences["preferences"][person]["thirdPreference"]
            if preferences["placements"][firstPreference]["numberOfGrads"] > 1:
                for i in range(1, preferences["placements"][firstPreference]["numberOfGrads"]+1):
                    graph[person][f"{firstPreference}_{i}"]["weight"] += 75
            else:
                graph[person][firstPreference]["weight"] += 75
            if preferences["placements"][secondPreference]["numberOfGrads"] > 1:
                for i in range(1, preferences["placements"][secondPreference]["numberOfGrads"]+1):
                    graph[person][f"{secondPreference}_{i}"]["weight"] += 50
            else:
                graph[person][secondPreference]["weight"] += 50
            if preferences["placements"][thirdPreference]["numberOfGrads"] > 1:
                for i in range(1, preferences["placements"][thirdPreference]["numberOfGrads"]+1):
                    graph[person][f"{thirdPreference}_{i}"]["weight"] += 25
            else:
                graph[person][thirdPreference]["weight"] += 25


if __name__ == "__main__":
    prefMatcher = PreferenceMatcher()
    preferences = prefMatcher.readPreferenceFile()
    preferenceGraph = prefMatcher.convertPreferencesToGraph(preferences)
    prefMatcher.drawGraph(preferenceGraph)
    prefMatcher.applyPreferenceWeighting(preferenceGraph, preferences)
    prefMatcher.drawGraph(preferenceGraph)
    pp.pprint(nx.maximal_matching(preferenceGraph))
    pp.pprint(nx.max_weight_matching(preferenceGraph))
