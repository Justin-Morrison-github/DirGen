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
        # Commands/Operations
        {"flags": ("-clr", "--clear"), "action": "store_true", "help": "Clear options"},
        {"flags": ("-del", "--delete"), "action": "store_true", "help": "Delete options"},
        {"flags": ("-r", "--reset"), "action": "store_true", "help": "Reset options"},

        # Modes
        {"flags": ("-t", "--text"), "action": "store_true", "help": "Provide text input"},
        {"flags": ("-j", "--json"), "action": "store_true", "help": "Provide JSON file input"},
        {"flags": ("-py", "--python"), "action": "store_true", "help": "Provide Python file input"},

        # Options
        {"flags": ("-cfg_m", "--config_mode"), "action": "store_true", "help": "Set defaut mode"},
        {"flags": ("-cfg_py", "--config_python"), "action": "store_true", "help": "Set defaut python file"},
        {"flags": ("-cfg_j", "--config_json"), "action": "store_true", "help": "Set defaut json file"},
        {"flags": ("-cfg", "--config"), "action": "store_true", "help": "Provide config/settings options"},
        {"flags": ("-f", "--force"), "action": "store_true", "help": "Force operations"},
        {"flags": ("-c", "--cache"), "action": "store_true", "help": "Cache options"},
        {"flags": ("-v", "--verbose"), "action": "store_true", "help": "Prints messages to stdout on file/folder creation"},
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

    def only(self, arg: bool | str):
        for key,val in vars(self.args).items(): # Iterate over all of the args in the Namespace
            if val != arg and val:
                return False
        return arg == True


    def parse(self) -> argparse.Namespace:
        self.args = self.arg_parser.parse_args(self.argv)

        # Only allow one operator to be used at once

        if self.args.reset:
            return self.reset_handler()
        elif self.args.clear:
            return self.clear_handler()    
        elif self.args.delete:
            return self.delete_handler()   
        
        elif self.args.config_mode:
            return self.default_mode_handler()
        elif self.args.config_python:
            return self.default_python_handler()
        elif self.args.config_json:
            return self.default_json_handler()
        elif self.args.config:
            return self.config_handler()
        
        elif self.args.python:
            return self.python_handler()
        elif self.args.json:
            return self.json_handler()
        elif self.args.text:
            return self.text_handler()

        elif self.only(self.args.cache):
            return print(self.cache)


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

    def config_handler(self):
        if self.only(self.args.config):
            print(self.settings)

    def default_mode_handler(self):
        if self.args.data:
            self.settings[Settings.DEFAULT_MODE] = "-" + self.args.data
        else:
            self.args.data = self.settings.default_mode
            print(self.args.data)

    def default_python_handler(self):
        if self.args.data:
            self.settings[Settings.DEFAULT_PYTHON_FILE] = self.args.data
        else:
            self.args.data = self.settings.default_python_file
            print(self.args.data)

    def default_json_handler(self):
        if self.args.data:
            self.settings[Settings.DEFAULT_JSON_FILE] = self.args.data
        else:
            self.args.data = self.settings.default_json_file
            print(self.args.data)


    def dirgen(self):
        self.files_made = self.parser.mkdir()
        self.cache.append(self.files_made)

    def clear_handler(self):
        if self.args.cache:
            self.cache.clear()

    def delete_handler(self):
        if self.args.cache:
            self.cache.delete_all_files(self.args.verbose)

    def python_handler(self):
        if not self.args.data:
            self.args.data = self.settings.default_python_file
        self.parser = PyParser(self.dst_folder, self.args.data.strip(".py"))

    def json_handler(self):
        if not self.args.data:
            self.args.data = self.settings.default_json_file
        self.parser = JSONParser(self.dst_folder, self.args.data)

    def text_handler(self):
        if not self.args.data:
            raise ValueError("-t: no text given")
        self.parser = TextParser(self.dst_folder, self.args.data)

    def reset_handler(self):
        if self.args.cache:
            self.cache.delete_all_files(self.args.verbose)

        elif self.args.config:
            self.settings.reset(self.args.verbose)

        elif not self.args.config and not self.args.cache:
            self.cache.delete_all_files(self.args.verbose)
            self.settings.reset(self.args.verbose)


if __name__ == "__main__":
    app = ArgParser()
    app.parse()
    parser = app.get_parser()
