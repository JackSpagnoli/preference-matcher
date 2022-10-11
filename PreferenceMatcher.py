import json
import pprint as pp
import re
import sys
from typing import Any
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
PATH_TO_INPUT_FILES = "./input_files/"


def convert_json_to_dict_from_file(filename: str) -> dict[str, Any]:
    with open(PATH_TO_INPUT_FILES + filename) as f:
        return json.load(f)


class PreferenceMatcher:
    def __init__(self, preference_file_name, placement_file_name) -> None:
        self.placements = convert_json_to_dict_from_file(placement_file_name)
        self.preferences_by_person = convert_json_to_dict_from_file(
            preference_file_name
        )
        self.create_tag_data_structure()

    def create_tag_data_structure(self):
        self.placements_by_tag = {}
        for placement_name, placement_data in self.placements.items():
            for tag in placement_data["tags"]:
                if tag in self.placements_by_tag:
                    self.placements_by_tag[tag].append(placement_name)
                else:
                    self.placements_by_tag[tag] = [placement_name]

    def extract_placement_names(self):
        placement_names = []
        for placement_name, placement_data in self.placements.items():
            if placement_data["number_of_grads"] > 1:
                numbered_names = []
                for i in range(
                    1, self.placements[placement_name]["number_of_grads"] + 1
                ):
                    numbered_names.append(f"{placement_name}_{i}")
                placement_names.extend(numbered_names)
            elif placement_data["number_of_grads"] == 1:
                placement_names.append(placement_name)
        return placement_names

    def extract_people_names(self):
        return list(self.preferences_by_person.keys())

    def convert_preferences_to_graph(self):
        preferences_graph = nx.Graph()
        self.placement_names = self.extract_placement_names()
        self.people_names = self.extract_people_names()
        preferences_graph.add_nodes_from(self.placement_names)
        preferences_graph.add_nodes_from(self.people_names)
        preferences_graph.add_edges_from(
            list(itertools.product(self.people_names, self.placement_names)), weight=50
        )
        return preferences_graph

    def weight_placement(self, graph, person, placements_to_weight, weighting):
        for placementName in placements_to_weight:
            graph[person][placementName]["weight"] += weighting

    def extract_placements_from_preference(self, preference):
        placements_to_weight = []
        placements_to_check_num_of_grads = []

        preference_is_a_tag = preference in self.placements_by_tag
        if preference_is_a_tag:
            placements_to_check_num_of_grads.extend(self.placements_by_tag[preference])
        else:
            placements_to_check_num_of_grads.append(preference)
        for placement_to_check in placements_to_check_num_of_grads:
            placement_can_take_multiple_grads = (
                self.placements[placement_to_check]["number_of_grads"] > 1
            )
            if placement_can_take_multiple_grads:
                for i in range(
                    1, self.placements[placement_to_check]["number_of_grads"] + 1
                ):
                    placements_to_weight.append(f"{placement_to_check}_{i}")
            else:
                placements_to_weight.append(placement_to_check)
        return placements_to_weight

    def apply_preference_weighting(self, graph, weightings):
        for person in self.people_names:
            first_placements_to_weight = self.extract_placements_from_preference(
                self.preferences_by_person[person]["firstPreference"]
            )
            second_placements_to_weight = self.extract_placements_from_preference(
                self.preferences_by_person[person]["secondPreference"]
            )
            third_placements_to_weight = self.extract_placements_from_preference(
                self.preferences_by_person[person]["thirdPreference"]
            )
            second_placements_with_duplicate_placements_removed = [
                placement
                for placement in second_placements_to_weight
                if placement not in first_placements_to_weight
            ]
            third_placements_with_duplicate_placements_removed = [
                placement
                for placement in third_placements_to_weight
                if (
                    placement not in first_placements_to_weight
                    and placement not in second_placements_to_weight
                )
            ]
            self.weight_placement(
                graph, person, first_placements_to_weight, weightings[0]
            )
            self.weight_placement(
                graph,
                person,
                second_placements_with_duplicate_placements_removed,
                weightings[1],
            )
            self.weight_placement(
                graph,
                person,
                third_placements_with_duplicate_placements_removed,
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
    COHORT = "2022"
    pref_matcher = PreferenceMatcher(
        "preferences_2022_cohort.json", "placements_2022_cohort.json"
    )
    preference_graph = pref_matcher.convert_preferences_to_graph()
    pref_matcher.apply_preference_weighting(preference_graph, weightings)
    matching = list(nx.max_weight_matching(preference_graph))
    for i, match in enumerate(matching):
        if not match[0] in pref_matcher.people_names:
            matching[i] = (match[1], match[0])
    no_preference_matchings = []
    placement_by_person = {person: placement for (person, placement) in matching}

    num_directorate_placements_by_directorate = {
        "Product Development": 0,
        "Data Services": 0,
        "Cyber Operations": 0,
        "IT Operations": 0,
        "Platforms": 0,
    }
    for placement in placement_by_person.values():
        placement_name_without_appended_number = re.sub(r"_\d", "", placement)
        directorate = pref_matcher.placements[placement_name_without_appended_number][
            "directorate"
        ]
        num_directorate_placements_by_directorate[directorate] += 1
    print(num_directorate_placements_by_directorate)
    with open(
        f"./output/cohort-without-api-management-{COHORT}-{weightings}.txt", "w"
    ) as file:

        for match in sorted(matching):
            person_name = match[0]
            placement_name = match[1]
            person_first_preference = pref_matcher.preferences_by_person[person_name][
                "firstPreference"
            ]
            person_second_preference = pref_matcher.preferences_by_person[person_name][
                "secondPreference"
            ]
            person_third_preference = pref_matcher.preferences_by_person[person_name][
                "thirdPreference"
            ]
            placement_name_without_appended_number = re.sub(r"_\d", "", match[1])
            is_placement_in_person_preferences = (
                placement_name_without_appended_number
                in [
                    person_first_preference,
                    person_second_preference,
                    person_third_preference,
                ]
            )
            placement_tags = pref_matcher.placements[
                placement_name_without_appended_number
            ]["tags"]
            is_placement_in_person_tag_preferences = (
                person_first_preference in placement_tags
                or person_second_preference in placement_tags
                or person_third_preference in placement_tags
            )
            if (
                not is_placement_in_person_preferences
                and not is_placement_in_person_tag_preferences
            ):
                no_preference_matchings.append(match)
            file.write(
                f"""\n{match[0]} -> {match[1]} - Directorate: {pref_matcher.placements[placement_name_without_appended_number]["directorate"]}:
                    1st:{pref_matcher.preferences_by_person[match[0]]['firstPreference']}
                    2nd:{pref_matcher.preferences_by_person[match[0]]['secondPreference']}
                    3rd:{pref_matcher.preferences_by_person[match[0]]['thirdPreference']}"""
            )

        file.write("\nNo Preference Matched:")

        for match in no_preference_matchings:
            file.write(f"{match[0]} -> {match[1]}\n")
