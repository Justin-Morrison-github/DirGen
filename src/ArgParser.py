import os, sys
curr_dir =os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_dir)
import argparse
from pathlib import Path
from Parser import PyParser, TextParser, JSONParser, Parser
from cache import Cache
from settings.settings import Settings
from tree import tree


# DEFAULT_PYTHON_TARGET = "__mytool_target__"
# DEFAULT_JSON_FILE = "test.json"
SETTINGS_FILE = "./settings/settings.json"

TEXT_MODE = "-t"
PYTHON_MODE = "-py"
JSON_MODE = "-j"


def create_parser() -> argparse.ArgumentParser:
    arg_parser = argparse.ArgumentParser(description="MyTool - Command Line Options")

    options = [
        {"flags": ("-cache", "--cache"), "action": "store_true", "help": "Cache options"},
        {"flags": ("-clr", "--clear"), "action": "store_true", "help": "Clear cache"},
        {"flags": ("-p", "--print"), "action": "store_true", "help": "Print cache"},
        {"flags": ("-del", "--delete"), "action": "store_true", "help": "Delete cache"},
        {"flags": ("-r", "--reset"), "action": "store_true", "help": "Reset options"},
        {"flags": ("-sd", "--set_default"), "action": "store_true", "help": "Set default files"},
        {"flags": ("-m", "--mode"), "action": "store_true", "help": "Set default mode"},
        {"flags": ("-t", "--text"), "action": "store_true", "help": "Provide text input"},
        {"flags": ("-j", "--json"), "action": "store_true", "help": "Provide JSON file input"},
        {"flags": ("-py", "--python"), "action": "store_true", "help": "Provide Python file input"},
    ]

    for option in options:
        arg_parser.add_argument(*option['flags'], action=option['action'], help=option['help'])

    arg_parser.add_argument("data", type=str, nargs="?", default=None, help="Provide filename/text input")

    return arg_parser


class ArgParser():
    def __init__(self, argv: list[str], settings: Settings, cache: Cache, base_folder=Path.cwd()):
        self.argv = argv
        self.settings = settings
        self.cache = cache
        self.base_folder = base_folder
        self.arg_parser: argparse.ArgumentParser = create_parser()
        self.args = None

    def parse(self) -> argparse.Namespace:
        self.args = self.arg_parser.parse_args(self.argv)

        if self.args.reset:
            return self.reset()
        if self.args.cache:
            return self.cache_handler()
        if self.args.set_default:
            return self.set_default_handler()

        # IHandle Defaults
        if not any([self.args.json, self.args.python, self.args.text]):
            mode = self.settings.default_mode
            self.args.data = self.settings.default_map[mode]

            if mode == PYTHON_MODE:
                self.args.python = True
            elif mode == JSON_MODE:
                self.args.json = True
            elif mode == TEXT_MODE:
                self.args.text = True
        

    def get_parser(self) -> Parser:
        if self.args.text:
            if not self.args.data:
                raise ValueError("-t: no text given")
            parser = TextParser(self.base_folder, self.args.data)

        elif self.args.python:
            if not self.args.data:
                self.args.data = self.settings.default_python_file
            parser = PyParser(self.base_folder, self.args.data.strip(".py"))

        elif self.args.json:
            if not self.args.data:
                self.args.data = self.settings.default_json_file
            parser = JSONParser(self.base_folder, self.args.data)

        else:
            raise ValueError("mytool: Error Invalid Option")

        return parser

    def cache_handler(self):
        assert self.args.cache

        if self.args.clear:
            self.cache.clear()
        elif self.args.delete:
            self.cache.delete_all_files()
        else:
            self.cache.print()
            # raise ValueError("cache_handler: Invalid Arguement")

    def set_default_handler(self):
        assert self.args.set_default

        if self.args.mode:
            self.settings[Settings.DEFAULT_MODE] = "-" + self.args.data
        elif self.args.python:
            self.settings[Settings.DEFAULT_PYTHON_FILE] = "-" + self.args.data
        elif self.args.json:
            self.settings[Settings.DEFAULT_JSON_FILE] = "-" + self.args.data
        else:
            raise ValueError("set_default_handler: Invalid Arguement")

    def handler(self):
        if self.args.python and not self.args.data:
            self.args.data = self.settings.default_python_file
        elif self.args.json and not self.args.data:
            self.args.data = self.settings.default_json_file
        elif not self.args.json and not self.args.python and not self.args.text:
            mode = self.settings.default_mode
            if mode == PYTHON_MODE:
                self.args.python = True
            elif mode == JSON_MODE:
                self.args.json = True
            elif mode == TEXT_MODE:
                self.args.text = True

            self.args.data = self.settings.default_map[mode]

    def reset(self):
        self.settings.reset()
        self.cache.clear()


if __name__ == "__main__":
    app = ArgParser()
    app.parse()
    parser = app.get_parser()
