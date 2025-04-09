import json
import constants

class Settings():
    DEFAULT_JSON_FILE = "default_json_file"
    DEFAULT_PYTHON_FILE = "default_python_file"
    DEFAULT_MODE = "default_mode"

    init_settings = {
        DEFAULT_JSON_FILE: "config/__default__.json",
        DEFAULT_PYTHON_FILE: "config/__default__.py",
        DEFAULT_MODE: "-j"
    }


    def __init__(self, settings_file=constants.SETTINGS_FILE):
        self.settings_dict = {}
        self.settings_file = settings_file
        with open(self.settings_file, 'r') as settings_json:
            self.settings_dict: dict = json.load(settings_json)

        self.default_json_file = self.settings_dict.get(Settings.DEFAULT_JSON_FILE)
        self.default_python_file = self.settings_dict.get(Settings.DEFAULT_PYTHON_FILE)
        self.default_mode = self.settings_dict.get(Settings.DEFAULT_MODE)

        self.default_map = {
            "-j": self.default_json_file,
            "-py": self.default_python_file
        }

    def __str__(self):
        return "\n".join(f"{f'{key.upper()}:':<25} {val}" for key, val in self.settings_dict.items())

    def __repr__(self):
        return repr(self.settings_dict)

    def __setitem__(self, key, value):
        self.settings_dict[key] = value
        setattr(self, key, value)
        with open(self.settings_file, "w") as json_file:
            json.dump(self.settings_dict, json_file)

    def reset(self, verbose:bool):
        self.settings_dict = Settings.init_settings
        with open(self.settings_file, "w") as json_file:
            json.dump(self.settings_dict, json_file)

        if verbose:
            print("\nSettings Reset")
            print(self)
