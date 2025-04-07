import os
import sys

from src.FolderStack import FolderStack
import unittest
from pathlib import Path


class TestLen(unittest.TestCase):
    def test_len1(self):
        stack = FolderStack()
        self.assertEqual(len(stack), 0)

    def test_len2(self):
        stack = FolderStack([Path("a")])
        self.assertEqual(len(stack), 1)

    def test_len3(self):
        stack = FolderStack([Path("a"), Path("b"), Path("a")])
        self.assertEqual(len(stack), 3)


class TestIter(unittest.TestCase):
    def test_iter1(self):
        stack = FolderStack()
        count = 0
        for _ in stack:
            count += 1
        self.assertEqual(count, 0)

    def test_len2(self):
        stack = FolderStack([Path("a")])
        count = 0
        for _ in stack:
            count += 1
        self.assertEqual(count, 1)

    def test_len3(self):
        stack = FolderStack([Path("a"), Path("b"), Path("a")])
        count = 0
        for _ in stack:
            count += 1
        self.assertEqual(count, 3)


class TestLen(unittest.TestCase):
    def test_len1(self):
        stack = FolderStack()
        self.assertEqual(len(stack), 0)

    def test_len2(self):
        stack = FolderStack([Path("a")])
        self.assertEqual(len(stack), 1)

    def test_len3(self):
        stack = FolderStack([Path("a"), Path("b"), Path("a")])
        self.assertEqual(len(stack), 3)


class TestPop(unittest.TestCase):
    def test_pop1(self):
        base = Path.cwd()
        path_a = Path("a")
        stack = FolderStack([path_a])

        self.assertEqual(stack.pop(), base / path_a)
        self.assertEqual(len(stack), 0)

    def test_pop2(self):
        base = Path.cwd()
        path_a = Path("a")
        path_b = Path("b")
        stack = FolderStack([path_a, path_b])

        self.assertEqual(stack.pop(), base / path_a / path_b)
        self.assertEqual(len(stack), 1)


class TestPush(unittest.TestCase):
    def test_push1(self):
        stack = FolderStack([])
        base = Path.cwd()

        path_a = Path("a")
        stack.push(path_a)
        self.assertEqual(stack.peek(), base / path_a)
        self.assertEqual(len(stack), 1)

    def test_push2(self):
        stack = FolderStack([])
        base = Path.cwd()

        path_a = Path("a")
        stack.push(path_a)
        self.assertEqual(stack.peek(), base / path_a)
        self.assertEqual(len(stack), 1)

        path_b = Path("b")
        stack.push(path_b)
        self.assertEqual(stack.peek(), base / path_a / path_b)
        self.assertEqual(len(stack), 2)

        path_c = Path("c")
        stack.push(path_c)
        self.assertEqual(stack.peek(), base / path_a / path_b / path_c)
        self.assertEqual(len(stack), 3)


class TestPeek(unittest.TestCase):
    def test_peek1(self):
        stack = FolderStack([])
        with self.assertRaises(IndexError):
            stack.peek()

        self.assertEqual(len(stack), 0)

    def test_peek2(self):
        base = Path.cwd()
        path_a = Path("a")
        path_b = Path("b")
        path_c = Path("c")

        stack = FolderStack()
        stack.push(path_a)
        self.assertEqual(stack.peek(), base / path_a)
        self.assertEqual(len(stack), 1)

        stack.push(path_b)
        self.assertEqual(stack.peek(), base / path_a / path_b)
        self.assertEqual(len(stack), 2)

        stack.push(path_c)
        self.assertEqual(stack.peek(), base / path_a / path_b / path_c)
        self.assertEqual(len(stack), 3)


class TestStr(unittest.TestCase):
    def test_str1(self):
        stack = FolderStack([])
        self.assertEqual(str(stack), str(stack.backing_list))

    def test_str2(self):
        stack = FolderStack([Path("a"), Path("b")])
        self.assertEqual(str(stack), str(stack.backing_list))


class TestRepr(unittest.TestCase):
    def test_repr1(self):
        stack = FolderStack([])
        self.assertEqual(repr(stack), repr(stack.backing_list))

    def test_repr2(self):
        stack = FolderStack([Path("a"), Path("b")])
        self.assertEqual(repr(stack), repr(stack.backing_list))


if __name__ == "__main__":
    unittest.main()
