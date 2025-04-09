
import os
import sys
from parameterized import parameterized
from pathlib import Path
from unittest.mock import Mock, patch
from src.ArgParser import ArgParser, create_parser, Cache, Settings
import constants

import unittest


class TestArgParserInit(unittest.TestCase):
    def setUp(self):
        # self.settings = Settings(SETTINGS_FILE)
        self.cache = Mock(spec=Cache)
        self.settings = Mock(spec=Settings)
        self.base_folder = Path(".")

    def test_init_fields(self):
        with patch('sys.argv', ["Empty"]):

            parser = ArgParser(argv=["Empty"], settings=self.settings, cache=self.cache)

            self.assertEqual(parser.argv,  sys.argv)
            self.assertEqual(parser.settings,  self.settings)
            self.assertEqual(parser.cache,  self.cache)
            self.assertEqual(parser.dst_folder,  Path.cwd())
            self.assertEqual(parser.args,  None)


class TestArgParserParse(unittest.TestCase):

    def setUp(self):
        # self.settings = Mock(spec=Settings)
        self.settings = Settings(constants.SETTINGS_FILE)
        self.cache = Mock(spec=Cache)
        self.base_folder = Path(".")

    def test_parse_with_no_args(self):
        with patch('sys.argv', ["dirgen"]):
            parser = ArgParser(argv=sys.argv[1:], dst_folder=constants.DEV_FOLDER,
                               settings=self.settings, cache=self.cache)

            parser.parse()
            self.assertEqual(parser.args.cache, False)
            self.assertEqual(parser.args.clear, False)
            self.assertEqual(parser.args.delete, False)
            self.assertEqual(parser.args.config_mode, False)

            self.assertTrue(parser.args.text == (self.settings.default_mode == "-t"), "Text mode mismatch")
            self.assertTrue(parser.args.json == (self.settings.default_mode == "-j"), "JSON mode mismatch")
            self.assertTrue(parser.args.python == (self.settings.default_mode == "-py"), "Python mode mismatch")

            self.assertEqual(parser.args.data, self.settings.default_map[self.settings.default_mode])

    @parameterized.expand([
        ("python_mode", "-py", {"text": False, "json": False, "python": True}, "-py", None),
        ("json_mode", "-j", {"text": False, "json": True, "python": False}, "-j", None),
        ("text_mode", "-t", {"text": True, "json": False, "python": False}, None, ValueError),
    ])
    def test_parse_modes(self, name, mode, expected_modes, expected_data_key, expected_exception):
        with patch('sys.argv', ["dirgen", mode]):
            parser = ArgParser(argv=sys.argv[1:], settings=self.settings, cache=self.cache)

            if expected_exception:
                with self.assertRaises(expected_exception):
                    parser.parse()
            else:
                parser.parse()

            # Mode flags
            self.assertEqual(parser.args.text, expected_modes["text"], "Text mode mismatch")
            self.assertEqual(parser.args.json, expected_modes["json"], "JSON mode mismatch")
            self.assertEqual(parser.args.python, expected_modes["python"], "Python mode mismatch")

            # Other flags
            self.assertFalse(parser.args.cache)
            self.assertFalse(parser.args.clear)
            self.assertFalse(parser.args.delete)
            self.assertFalse(parser.args.config_mode)

            # Data check
            if expected_exception:
                self.assertIsNone(parser.args.data)
            else:
                self.assertEqual(parser.args.data, self.settings.default_map[expected_data_key])

    @parameterized.expand([
        ("cache", "-c", None),
        ("clear", "-clr", None),
        ("delete", "-del", None),
        ("reset", "-r", None),
        ("config_mode", "-cfg_m", None),
        ("text", "-t", ValueError),
        ("json", "-j", None),
        ("python", "-py", None),
    ])
    def test_parse_flags_set_correctly(self, name, mode, expected_exception):
        with patch('sys.argv', ["dirgen", mode]):
            parser = ArgParser(argv=sys.argv[1:], settings=self.settings, cache=self.cache)

            if expected_exception:
                with self.assertRaises(expected_exception):
                    parser.parse()
            else:
                parser.parse()

            self.assertTrue(getattr(parser.args, name))


class TestArgParser(unittest.TestCase):

    def setUp(self):
        # Use Mock instead of MagicMock
        self.settings = Settings(constants.SETTINGS_FILE)
        self.cache = Mock(spec=Cache)
        self.base_folder = Path(".")

    # def test_cache_option(self):
    #     with patch('sys.argv', ["dirgen", "--cache"]):
    #         parser = ArgParser(argv=sys.argv[1:], settings=self.settings, cache=self.cache)
    #         parser.parse()
    #         self.assertTrue(parser.args.cache)
    #         self.assertFalse(parser.args.clear)
    #         self.assertFalse(parser.args.delete)
    #         # Simulate cache handler behavior
    #         self.cache.print.assert_called_once()

    def test_cache_clear_option(self):
        with patch('sys.argv', ["dirgen", "--clear", "--cache"]):
            parser = ArgParser(argv=sys.argv[1:], settings=self.settings, cache=self.cache)
            args = parser.parse()
            self.cache.clear.assert_called_once()

    def test_reset_option(self):
        with patch('sys.argv', ["dirgen", "--reset"]):
            parser = ArgParser(argv=sys.argv[1:], settings=self.settings, cache=self.cache)
            parser.parse()
            self.assertTrue(parser.args.reset)
            self.cache.delete_all_files.assert_called_once()

    def test_text_input(self):
        with patch('sys.argv', ["dirgen", "--text", "{'A':'$'}"]):
            parser = ArgParser(argv=sys.argv[1:], settings=self.settings, cache=self.cache)
            parser.parse()
            self.assertTrue(parser.args.text)
            self.assertEqual(parser.args.data, "{'A':'$'}")

    def test_json_input(self):
        with patch('sys.argv', ["dirgen", "--json", "test.json"]):
            parser = ArgParser(argv=sys.argv[1:], settings=self.settings, cache=self.cache)
            parser.parse()
            self.assertTrue(parser.args.json)
            self.assertEqual(parser.args.data, "test.json")

    def test_python_input(self):
        with patch('sys.argv', ["dirgen", "--python", "test.py"]):
            parser = ArgParser(argv=sys.argv[1:], settings=self.settings, cache=self.cache)
            parser.parse()
            self.assertTrue(parser.args.python)
            self.assertEqual(parser.args.data, "test.py")

    def test_default_mode_handling(self):
        # Mocking attribute values directly
        self.settings.default_mode = constants.PYTHON_MODE
        self.settings.default_map = {constants.PYTHON_MODE: "config/__default__.py"}

        with patch('sys.argv', ["dirgen"]):
            parser = ArgParser(argv=sys.argv[1:], settings=self.settings, cache=self.cache)
            parser.parse()
            self.assertTrue(parser.args.python)
            self.assertEqual(parser.args.data, "config/__default__.py")

    # def test_invalid_option(self):
    #     with patch('sys.argv', ["dirgen", "--invalid"]):
    #         parser = ArgParser(argv=["--invalid"], settings=self.settings, cache=self.cache)
    #         with self.assertRaises(SystemExit):  # argparse raises SystemExit on invalid arguments
    #             parser.parse()


if __name__ == "__main__":
    unittest.main(verbosity=2)
