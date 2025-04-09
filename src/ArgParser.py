import os, sys
curr_dir =os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_dir)
import argparse
from pathlib import Path
from Parser import PyParser, TextParser, JSONParser, Parser
from cache import Cache
from settings import Settings
from tree import tree
import constants


def create_parser() -> argparse.ArgumentParser:
    arg_parser = argparse.ArgumentParser(description="MyTool - Command Line Options")

    options = [
        {"flags": ("-c", "--cache"), "action": "store_true", "help": "Cache options"},
        {"flags": ("-clr", "--clear"), "action": "store_true", "help": "Clear options"},
        {"flags": ("-m", "--mode"), "action": "store_true", "help": "Mode options"},
        {"flags": ("-t", "--text"), "action": "store_true", "help": "Provide text input"},
        {"flags": ("-j", "--json"), "action": "store_true", "help": "Provide JSON file input"},
        {"flags": ("-py", "--python"), "action": "store_true", "help": "Provide Python file input"},
        {"flags": ("-f", "--force"), "action": "store_true", "help": "Force operations"},
        {"flags": ("-del", "--delete"), "action": "store_true", "help": "Delete options"},
        {"flags": ("-r", "--reset"), "action": "store_true", "help": "Reset options"},
        {"flags": ("-cfg", "--config"), "action": "store_true", "help": "Provide config/settings options"},
        {"flags": ("-set", "--set"), "action": "store_true", "help": "Set options"},
        {"flags": ("-get", "--get"), "action": "store_true", "help": "Get options"},
    ]

    for option in options:
        arg_parser.add_argument(*option['flags'], action=option['action'], help=option['help'])

    arg_parser.add_argument("data", type=str, nargs="?", default=None, help="Provide filename/text input")

    return arg_parser


class ArgParser():
    def __init__(self, argv: list[str], settings: Settings, cache: Cache, dst_folder=Path.cwd()):
        self.argv = argv
        self.settings = settings
        self.cache = cache
        self.dst_folder = dst_folder
        self.arg_parser: argparse.ArgumentParser = create_parser()
        self.args = None
        self.parser = None
        self.files_made = []

    def parse(self) -> argparse.Namespace:
        self.args = self.arg_parser.parse_args(self.argv)

        # Only allow one operator to be used at once

        if self.args.reset:
            return self.reset_handler()
        elif self.args.clear:
            return self.clear_handler()    
        elif self.args.delete:
            return self.delete_handler()   
        elif self.args.set:
            return self.set_handler()
        elif self.args.get:
            return self.get_handler()

        # Handle Defaults
        elif not any([self.args.json, self.args.python, self.args.text]):
            mode = self.settings.default_mode
            self.args.data = self.settings.default_map[mode]

            if mode == constants.PYTHON_MODE:
                self.args.python = True
            elif mode == constants.JSON_MODE:
                self.args.json = True
            elif mode == constants.TEXT_MODE:
                self.args.text = True


        if not self.args.data:
            if self.args.python:
                self.args.data = self.settings.default_python_file
            elif self.args.json:
                self.args.data = self.settings.default_json_file
            elif self.args.text:
                raise ValueError("parse: No text provided")

        if any([self.args.python, self.args.json, self.args.text]):
            self.parser = self.get_parser()
            # self.files_made = self.parser.mkdir()
            # self.cache.append(self.files_made)

    def dirgen(self):
        self.files_made = self.parser.mkdir()
        self.cache.append(self.files_made)

    def clear_handler(self):
        if self.args.cache:
            self.cache.clear()

    def delete_handler(self):
        if self.args.cache:
            self.cache.delete_all_files()

    def get_handler(self):
        if self.args.cache:
            self.args.data = str(self.cache)
        elif self.args.python:
            self.args.data = self.settings.default_python_file
        elif self.args.json:
            self.args.data = self.settings.default_json_file
        elif self.args.mode:
            self.args.data = self.settings.default_mode
        elif self.args.config:
            self.args.data = str(self.settings)
        
        print(self.args.data)

    def get_parser(self) -> Parser:
        if self.args.text:
            if not self.args.data:
                raise ValueError("-t: no text given")
            parser = TextParser(self.dst_folder, self.args.data)

        elif self.args.python:
            if not self.args.data:
                self.args.data = self.settings.default_python_file
            parser = PyParser(self.dst_folder, self.args.data.strip(".py"))

        elif self.args.json:
            if not self.args.data:
                self.args.data = self.settings.default_json_file
            parser = JSONParser(self.dst_folder, self.args.data)
        else:
            parser = None
      
        return parser

    def set_handler(self):
        if self.args.config:
            if self.args.mode:
                self.settings[Settings.DEFAULT_MODE] = "-" + self.args.data
            elif self.args.python:
                self.settings[Settings.DEFAULT_PYTHON_FILE] = self.args.data
            elif self.args.json:
                self.settings[Settings.DEFAULT_JSON_FILE] = self.args.data
        else:
            raise ValueError("set_handler: Invalid Arguement")

    def reset_handler(self):
        if self.args.cache:
            self.cache.delete_all_files()
        elif self.args.config:
            self.settings.reset()
        elif not self.args.config and not self.args.cache:
            self.cache.delete_all_files()
            self.settings.reset()



if __name__ == "__main__":
    app = ArgParser()
    app.parse()
    parser = app.get_parser()
