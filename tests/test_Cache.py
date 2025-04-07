import os
from unittest.mock import Mock
from src.cache import Cache
import unittest
import constants


class TestMockCache(unittest.TestCase):

    def setUp(self):
        self.cache = Mock(spec=Cache)

    def test_cache_load(self):
        self.cache._load()
        self.cache._load.assert_called_once()

    def test_cache_write(self):
        self.cache.write()
        self.cache.write.assert_called_once()

    def test_cache_print(self):
        self.cache.print()
        self.cache.print.assert_called_once()

    def test_cache_clear(self):
        self.cache.clear()
        self.cache.clear.assert_called_once()

    def test_cache_delete_files(self):
        self.cache.delete_all_files()
        self.cache.delete_all_files.assert_called_once()

    def test_cache_append(self):
        self.cache.append()
        self.cache.append.assert_called_once()


class TestCacheForReal(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.A = constants.DEV_FOLDER / "A"
        if not self.A.exists():
            self.A.mkdir()
        self.A.chmod(0o777)  # Full read/write/execute permissions

        self.B = constants.DEV_FOLDER / "B"
        if not self.B.exists():
            self.B.mkdir()
        self.B.chmod(0o777)

        self.C = constants.DEV_FOLDER / "C"
        if not self.C.exists():
            self.C.mkdir()
        self.C.chmod(0o777)

        self.D = constants.DEV_FOLDER / "D"
        if not self.D.exists():
            self.D.mkdir()
        self.D.chmod(0o777)

        self.cache_path = constants.DEV_FOLDER / "test_cache"
        self.test_cache = Cache(self.cache_path)

    # def setUp(self):
    #     self.test_cache.clear()

    # ------ Load -------#

    def test_cache_load(self):
        self.assertEqual(self.test_cache.files, [])

    def test_cache_load_after_append(self):
        self.test_cache.append([self.A])
        self.test_cache._load()
        self.assertEqual(self.test_cache.files, [self.A])

    # ------ Append -------#

    def test_cache_append_one(self):
        self.test_cache.append([self.A])
        self.assertEqual(self.test_cache.files, [self.A])

    def test_cache_append_duplicate(self):
        self.test_cache.append([self.A, self.A])
        self.assertEqual(self.test_cache.files, [self.A])

    def test_cache_append_many(self):
        self.test_cache.append([self.A, self.B, self.C])
        self.assertEqual(self.test_cache.files, [self.A, self.B, self.C])

    # ------ Update -------#
    def test_cache_update_one(self):
        self.assertEqual(os.stat(self.cache_path).st_size, 0)

        # Directly append to files field
        self.test_cache.files.append(self.A)
        self.test_cache._update()
        self.assertEqual(os.stat(self.cache_path).st_size, len(str(self.A) + "\n\r"))
        with open(self.cache_path) as file:
            count = 0
            for line in file:
                count += 1
        self.assertEqual(count, 1)

    def test_cache_update_many(self):
        self.assertEqual(os.stat(self.cache_path).st_size, 0)
        files = [self.A, self.B, self.C]
        self.test_cache.append(files)
        self.test_cache._update()
        self.assertEqual(os.stat(self.cache_path).st_size, sum(
            [len(str(file)) for file in files]) + len("\n\r") * len(files))
        with open(self.cache_path) as file:
            count = 0
            for line in file:
                count += 1
        self.assertEqual(count, 3)

    def tearDown(self):
        self.test_cache.clear()

    @classmethod
    def tearDownClass(self):
        """ Called after every test. """
        self.A.rmdir()
        self.B.rmdir()
        self.C.rmdir()
        self.D.rmdir()


# class TestCache(unittest.TestCase):

#     def setUp(self):
#         self._temp_dir = tempfile.TemporaryDirectory()
#         self.temp_path = Path(self._temp_dir.name)
#         self.cache_path = self.temp_path / "cache"
#         self.cache = Cache([], self.cache_path)

#         self.p1 = Path(self.temp_path / 'test')
#         self.p2 = Path(self.temp_path / 'test' / 'A')
#         self.p3 = Path(self.temp_path / 'test'/ ' B')

#         with open(self.cache_path, "w+") as file:
#             file.write(f"{self.p1}\n")
#             file.write(f"{self.p2}\n")
#             file.write(f"{self.p3}\n")

#     def tearDown(self):
#         """ Called after every test. """
#         self._temp_dir.cleanup()

#     def test_cache_load(self):
#         self.cache.load()
#         self.assertEqual(self.cache.files, [self.p1, self.p2, self.p3])

#     def test_cache_write(self):
#         self.cache.load()
#         self.cache.write()
#         self.assertEqual(self.cache.files, [self.p1, self.p2, self.p3])

#         self.cache.files = []
#         self.cache.write()
#         self.assertEqual(self.cache.files, [])

#     def test_cache_delete_files(self):
#         self.cache.load()
#         self.assertTrue(self.p1 in self.cache.files, f"File does not exist {self.p1}")
#         self.assertTrue(self.p2 in self.cache.files, f"File does not exist {self.p2}")
#         self.assertTrue(self.p3 in self.cache.files, f"File does not exist {self.p3}")

#         self.cache.delete_files()
#         self.assertEqual(self.cache.files, [])
#         self.assertEqual(Path(self.cache_path).stat().st_size, 0)
#         self.assertTrue(self.p1 not in self.cache.files, f"File still exists {self.p1}")
#         self.assertTrue(self.p2 not in self.cache.files, f"File still exists {self.p2}")
#         self.assertTrue(self.p3 not in self.cache.files, f"File still exists {self.p3}")

#     def test_cache_clear(self):
#         self.cache.clear()
#         self.assertEqual(self.cache.files, [])
#         self.assertEqual(Path(self.cache_path).stat().st_size, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
