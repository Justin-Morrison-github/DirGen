import os, sys

curr_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(curr_dir)

from pathlib import Path
from sys import argv
import ArgParser
from ArgParser import ArgParser

from cache import Cache
from settings.settings import Settings
from tree import tree

SETTINGS_FILE = "./settings/settings.json"


def main():
    print(sys.argv)
    base_folder = Path.cwd()
    settings = Settings(SETTINGS_FILE)
    print(settings)

    cache = Cache()
    print(cache)

    arg_parser = ArgParser(argv[1:], settings, cache)
    arg_parser.parse()
    print(arg_parser.args)
    file_parser = arg_parser.get_parser()

    files_made: list[Path] = file_parser.mkdir()
    cache.append(files_made)

    # for file in files_made:
    #     if file.is_dir() and file.parent == files_made[0].parent:
    #         tree(file)
    # print()

    # cache.delete_files_found_in_cache()


if __name__ == "__main__":
    main()
