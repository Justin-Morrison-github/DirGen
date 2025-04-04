from pathlib import Path


class FolderStack():

    def __init__(self, iterable=[]):
        self.backing_list: list[Path] = []
        for item in iterable:
            self.push(item)

    def __len__(self):
        return len(self.backing_list)

    def __iter__(self):
        return iter(self.backing_list)

    def pop(self):
        return self.backing_list.pop()

    def peek(self):
        if self.backing_list:
            return self.backing_list[-1]
        raise IndexError("peek: FolderStack is empty")

    def push(self, path: Path, base_folder: Path = Path.cwd(), ):
        if self.backing_list:
            last_item = self.peek()
            new_item = last_item / path
            self.backing_list.append(new_item)
        else:
            self.backing_list.append(base_folder / path)

    def __str__(self):
        return str(self.backing_list)

    def __repr__(self):
        return repr(self.backing_list)
