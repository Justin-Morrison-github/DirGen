
from importlib import import_module
import sys
import os
# Adjusting path for imports
curr_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(curr_dir)
import constants
from pathlib import Path
import json
from FolderStack import FolderStack


class Parser():
    def __init__(self, base_folder):
        self.base_folder = base_folder
        self.files_made: list[Path] = []

    def mkdir(self):
        self.folder_stack = FolderStack()

        def _mkdir(key, value):

            self.folder_stack.push(Path(key), self.base_folder)
            try:
                folder = self.folder_stack.peek()
                folder.mkdir()
                # os.mkdir(self.folder_stack.peek())
                folder.chmod(0o777)  # Full read/write/execute permissions

            except FileExistsError as e:
                self.folder_stack.pop()
                print(e)
                return
            self.files_made.append(self.folder_stack.peek())

            if value == "$":
                self.folder_stack.pop()

            if isinstance(value, list):
                folder = self.folder_stack.pop()
                for file in value:
                    file = folder / Path(file)
                    with open(file, "w") as f:
                        self.files_made.append(file)

            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    _mkdir(sub_key, sub_value)
                self.folder_stack.pop()

        for key, value in self.dict.items():
            _mkdir(key, value)

        return self.files_made


class JSONParser(Parser):
    def __init__(self, base_folder, file):
        super().__init__(base_folder)
        self.file = Path(file)
        self.dict = {}

        with open(self.file) as file:
            self.dict = json.load(file)
            print(self.dict)

    def mkdir(self):
        return super().mkdir()


class PyParser(Parser):
    def __init__(self, base_folder, file: str):
        super().__init__(base_folder)
        self.file = Path(file)

        import_string = path_to_import_str(self.file)
        py_file = import_module(import_string)
        json_str = json.dumps(py_file.__target_dict__)
        self.dict = json.loads(json_str)

    def mkdir(self):
        return super().mkdir()


class TextParser(Parser):
    def __init__(self, base_folder, text: str):
        super().__init__(base_folder)

        self.text = text.replace("'", "\"")
        self.dict = json.loads(self.text)

    def mkdir(self):
        return super().mkdir()


def path_to_import_str(file: Path):
    str = ".".join(part for part in file.parts)
    return str.strip(".json")
