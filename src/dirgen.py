import os, sys

curr_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(curr_dir)

from sys import argv
from ArgParser import ArgParser

from cache import Cache
from settings import Settings
import constants


def main():
    print()
    settings = Settings(constants.SETTINGS_FILE)

    cache = Cache()

    arg_parser = ArgParser(argv[1:], settings, cache)
    arg_parser.parse()

    if arg_parser.parser:
        arg_parser.dirgen()

    # for file in files_made:
    #     if file.is_dir() and file.parent == files_made[0].parent:
    #         tree(file)
    print()


if __name__ == "__main__":
    main()
