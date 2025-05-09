
from pathlib import Path
from itertools import islice

space = '    '
branch = '│   '
tee = '├── '
last = '└── '


def tree(dir_path: Path, level: int = -1, limit_to_directories: bool = False,
         length_limit: int = 1000):
    """Given a directory Path object print a visual tree structure"""
    dir_path = Path(dir_path)  # accept string coerceable to Path
    files = 0
    directories = 0

    def inner(dir_path: Path, prefix: str = '', level=-1):
        nonlocal files, directories
        if not level:
            return  # 0, stop iterating
        if limit_to_directories:
            contents = [d for d in dir_path.iterdir() if d.is_dir()]

        else:
            contents = list(dir_path.iterdir())
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name
                directories += 1
                extension = branch if pointer == tee else space
                yield from inner(path, prefix=prefix+extension, level=level-1)
            elif not limit_to_directories:
                yield prefix + pointer + path.name
                files += 1
    print(dir_path.name)
    if dir_path.is_dir() and len(list(dir_path.iterdir())) == 0:
        print(f"{last}Empty")

    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        print(line)
    if next(iterator, None):
        print(f'... length_limit, {length_limit}, reached, counted:')
    print(f'\n{directories} directories' + (f', {files} files' if files else ''), "\n")


# Example usage
if __name__ == "__main__":
    root_path = Path("C:\\Users\\morri\\Downloads")
    tree(root_path)
        
