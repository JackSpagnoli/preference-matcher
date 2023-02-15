import json
import re
import sys
from typing import Any
import networkx as nx
import itertools
import tomllib
import tomlkit
import argparse
import math

PATH_TO_INPUT_FILES = "./input_files/"


def convert_json_to_dict_from_file(filename: str) -> dict[str, Any]:
    with open(PATH_TO_INPUT_FILES + filename) as f:
        return json.load(f)


def convert_toml_file_to_dict(filename: str) -> dict[str, Any]:
    with open(f"{PATH_TO_INPUT_FILES}{filename}", mode="rb") as f:
        return tomllib.load(f)


class PreferenceMatcher:
    def __init__(self, preference_file_name, placement_file_name) -> None:
        self.placements: dict[str, Any] = convert_toml_file_to_dict(placement_file_name)
        self.preferences_by_person: dict[str, Any] = convert_toml_file_to_dict(
            preference_file_name
        )
        self.placement_names = self.get_placement_names()
        self.people: list[str] = list(self.preferences_by_person.keys())
        self.create_placements_by_tag()

    def create_placements_by_tag(self):
        self.placements_by_tag = {}
        for placement, placement_data in self.placements.items():
            self.process_placement_tags(placement_data["tags"], placement)

    def process_placement_tags(self, placement_tags: list[str], placement: str):
        for tag in placement_tags:
            if tag in self.placements_by_tag:
                self.placements_by_tag[tag].add(placement)
            else:
                self.placements_by_tag[tag] = {placement}

    def generate_numbered_placement_names(self, placement: str, number_of_grads: int):
        numbered_names = []
        for i in range(1, number_of_grads + 1):
            numbered_names.append(f"{placement}_{i}")
        return numbered_names

    def get_placement_names(self):
        placement_names = []
        for placement, placement_data in self.placements.items():
            number_of_grads = placement_data["number_of_grads"]
            if number_of_grads > 1:
                numbered_names = self.generate_numbered_placement_names(
                    placement, number_of_grads
                )
                placement_names.extend(numbered_names)
            else:
                placement_names.append(placement)
        return placement_names

    def convert_preferences_to_graph(self):
        preferences_graph = nx.Graph()
        preferences_graph.add_nodes_from(self.placement_names)
        preferences_graph.add_nodes_from(self.people)
        preferences_graph.add_edges_from(
            list(itertools.product(self.people, self.placement_names)), weight=50
        )
        return preferences_graph

    def weight_placement(self, graph, person, placements_to_weight, weighting):
        for placementName in placements_to_weight:
            graph[person][placementName]["weight"] += weighting

    def get_placements_to_check_from_preference(self, preference):
        placements_to_check = []
        preference_is_a_tag = preference in self.placements_by_tag
        if preference_is_a_tag:
            placements_to_check.extend(self.placements_by_tag[preference])
        else:
            placements_to_check.append(preference)

        return placements_to_check

    def get_placements_from_preference(self, preference):
        placements_to_weight = []
        placements_to_check = self.get_placements_to_check_from_preference(preference)

        for placement_to_check in placements_to_check:
            number_of_grads = self.placements[placement_to_check]["number_of_grads"]
            placement_can_take_multiple_grads = number_of_grads > 1
            if placement_can_take_multiple_grads:
                numbered_names = self.generate_numbered_placement_names(
                    placement_to_check, number_of_grads
                )
                placements_to_weight.extend(numbered_names)
            else:
                placements_to_weight.append(placement_to_check)
        return placements_to_weight

    def apply_preference_weighting(self, graph, weightings):
        for person, preferences in self.preferences_by_person.items():
            first_placements_to_weight = self.get_placements_from_preference(
                preferences["firstPreference"]
            )
            second_placements_to_weight = self.get_placements_from_preference(
                preferences["secondPreference"]
            )
            third_placements_to_weight = self.get_placements_from_preference(
                preferences["thirdPreference"]
            )

            second_placements_with_duplicates_removed = [
                placement
                for placement in second_placements_to_weight
                if placement not in first_placements_to_weight
            ]
            third_placements_with_duplicates_removed = [
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
                second_placements_with_duplicates_removed,
                weightings[1],
            )
            self.weight_placement(
                graph,
                person,
                third_placements_with_duplicates_removed,
                weightings[2],
            )


def sort_matchings(matchings):
    sorted_matchings = []
    for match in matchings:
        sorted_matching = match

        first_element_is_a_person = sorted_matching[0] in pref_matcher.people
        if not first_element_is_a_person:
            sorted_matching = sorted_matching[::-1]

        sorted_matchings.append(sorted_matching)

    return sorted_matchings


def calculate_num_placements_by_directorate(matched_placements):
    num_directorate_placements_by_directorate = {
        "Product Development": 0,
        "Data Services": 0,
        "Cyber Operations": 0,
        "IT Operations": 0,
        "Platforms": 0,
    }
    for placement in matched_placements:
        placement_name_without_appended_number = re.sub(r"_\d", "", placement)
        placement_directorate = pref_matcher.placements[
            placement_name_without_appended_number
        ]["directorate"]
        num_directorate_placements_by_directorate[placement_directorate] += 1
    print(num_directorate_placements_by_directorate)
    return num_directorate_placements_by_directorate


def parse_matchings_for_output(sorted_matchings, pref_matcher: PreferenceMatcher):
    preference_matchings = {}
    for match in sorted_matchings:
        person = match[0]
        person_preferences = pref_matcher.preferences_by_person[person]
        first_preference = person_preferences["firstPreference"]
        second_preference = person_preferences["secondPreference"]
        third_preference = person_preferences["thirdPreference"]

        placement = match[1]
        placement_without_appended_number = re.sub(r"_\d", "", placement)
        placement_in_person_preferences = placement_without_appended_number in [
            first_preference,
            second_preference,
            third_preference,
        ]

        placement_tags = pref_matcher.placements[placement_without_appended_number][
            "tags"
        ]
        placement_in_person_tag_preferences = (
            first_preference in placement_tags
            or second_preference in placement_tags
            or third_preference in placement_tags
        )
        if (
            not placement_in_person_preferences
            and not placement_in_person_tag_preferences
        ):
            no_preference_matchings.append(match)
        preference_matchings[person] = {
            "matching": placement,
            "directorate": pref_matcher.placements[placement_without_appended_number][
                "directorate"
            ],
            "1st preference": first_preference,
            "2nd preference": second_preference,
            "3rd preference": third_preference,
        }

    return preference_matchings, no_preference_matchings


def write_to_file(
    preference_matchings,
    no_preference_matchings,
    num_directorate_placements_by_directorate,
):
    with open(f"./output/{OUTPUT_FILE_NAME}", "w", encoding="UTF-8") as file:
        file.write(f"{tomlkit.dumps(num_directorate_placements_by_directorate)}\n")
        file.write(f"{tomlkit.dumps(preference_matchings)}\n")

        if len(no_preference_matchings) == 0:
            file.write("\n# All people matched to a preference")
        else:
            file.write("\n# No Preference Matched:")

            for match in no_preference_matchings:
                file.write(f"{match[0]} -> {match[1]}\n")


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="Preference Matcher",
        description="This program matches graduates to placements based on preferences",
    )
    parser.add_argument(
        "-F",
        "--first",
        choices=range(0, 1001),
        metavar="First Preference",
        help="Enter the first preference weighting",
        default=100,
        type=int,
    )
    parser.add_argument(
        "-S",
        "--second",
        choices=range(0, 1001),
        metavar="Second Preference",
        help="Enter the second preference weighting",
        default=75,
        type=int,
    )
    parser.add_argument(
        "-T",
        "--third",
        choices=range(0, 1001),
        metavar="Third Preference",
        help="Enter the third preference weighting",
        default=50,
        type=int,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    weightings = [args.first, args.second, args.third]

    COHORT = "2022"
    OUTPUT_FILE_NAME = f"cohort-{COHORT}-{weightings}.toml"
    pref_matcher = PreferenceMatcher(
        "preferences_2022_cohort.toml", "placements_2022_cohort.toml"
    )

    preference_graph = pref_matcher.convert_preferences_to_graph()
    pref_matcher.apply_preference_weighting(preference_graph, weightings)
    unsorted_matchings = list(nx.max_weight_matching(preference_graph))
    sorted_matchings = sort_matchings(unsorted_matchings)

    no_preference_matchings = []
    matched_placements = [placement for (_, placement) in sorted_matchings]

    num_directorate_placements_by_directorate = calculate_num_placements_by_directorate(
        matched_placements
    )

    preference_matchings, no_preference_matchings = parse_matchings_for_output(
        sorted_matchings, pref_matcher
    )
    write_to_file(
        preference_matchings,
        no_preference_matchings,
        {"Directorate": num_directorate_placements_by_directorate},
    )
