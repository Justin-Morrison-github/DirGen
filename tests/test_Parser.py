import json
import sys
from types import ModuleType
from parameterized import parameterized
from pathlib import Path
from src.Parser import Parser, JSONParser, TextParser, PyParser, path_to_import_str
import unittest


class TestParserInit(unittest.TestCase):
    def test_parser_init1(self):
        with self.assertRaises(TypeError):
            parser = Parser()
        
    def test_parser_init2(self):
        parser = Parser(Path.cwd().parent)
        self.assertEqual(parser.base_folder, Path.cwd().parent)
        self.assertEqual(parser.files_made, [])


class TestJSONParserInit(unittest.TestCase):
    @parameterized.expand([
        "test.json",
        "config\__default__.json",
    ])
    def test_json_parser_init(self, file):
        parser = JSONParser(Path.cwd(), file)
        self.assertEqual(parser.base_folder, Path.cwd())
        self.assertEqual(parser.files_made, [])
        self.assertEqual(parser.file, Path(file))
        with open(parser.file) as f:
            data = json.load(f)
        self.assertEqual(parser.dict, data)


class TestPyParserInit(unittest.TestCase):
    @parameterized.expand([
        "test.py",
        "config\__default__.py",
    ])
    def test_py_parser_init(self, test_module_name):
        # test_module_name = "test.py"
        try:
            import_str = path_to_import_str(Path(test_module_name))

            test_module = ModuleType(import_str)
            test_module.__target_dict__ = {"A": "$"}
            sys.modules[import_str] = test_module

            parser = PyParser(Path.cwd(), test_module_name)
            self.assertEqual(parser.base_folder, Path.cwd())
            self.assertEqual(parser.files_made, [])
            self.assertEqual(parser.file, Path(test_module_name))
            self.assertEqual(parser.import_string, import_str)

            self.assertEqual(parser.py_file, test_module)
            self.assertEqual(parser.dict, test_module.__target_dict__)
        
        finally:
            if import_str in sys.modules:
                del sys.modules[import_str]


class TestTextParserInit(unittest.TestCase):
    @parameterized.expand([
        "{'A': '$'}",
        "{'A': ['test.py', 'README.md'], 'B':'$'}",
    ])
    def test_text_parser_init(self, text:str):
        parser = TextParser(Path.cwd(), text)
        self.assertEqual(parser.base_folder, Path.cwd())
        self.assertEqual(parser.files_made, [])

        new_text = text.replace("\'", "\"")

        self.assertEqual(parser.text, new_text)
        data = json.loads(new_text)
        self.assertEqual(parser.dict, data)
