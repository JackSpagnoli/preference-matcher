import toml

class DataAssurance:
    def __init__(self) -> None:
        self.data = {}

    def check_preference_repeats(self, preference_data: dict[str, dict:[str, any]]):
        for graduate, preferences in preference_data.items():
            self.data[graduate] = check_repeated_preferences(preferences)
            

    def write_toml_file(self):
        toml_config = toml.dumps(self.data)

        with open("DataAssuranceReport", "a") as f:
            f.write(toml_config)

def check_repeated_preferences(preferences_dict):
    response = []
    stated_preferences = []

    preferences = preferences_dict
    anti_preferences = preferences.pop("antiPreference", [])

    for preference in preferences.values():
        if preference in stated_preferences:
            response.append("Graduate has repeated preferences")
        stated_preferences.append(preference)

    for anti_preference in anti_preferences:
        if anti_preference in stated_preferences:
            response.append(
                "Graduate has put a preference as an antipreference"
            )

    return response