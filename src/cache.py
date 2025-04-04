from genericpath import isdir
from pathlib import Path
import shutil

__DEFAULT_CACHE__ = "./.mytool_cache/cache"


class Cache():
    def __init__(self, filename: str | Path = __DEFAULT_CACHE__):
        self.filepath = Path(filename)
        if not self.filepath.exists():
            with open(self.filepath, "w"):
                self.files = []
        self.files:list[Path] = []
        self._load()

    def _load(self):
        with open(self.filepath, "r") as cache:
            for line in cache:
                line = line.strip()
                file = Path(line)
                if file.exists() and file not in self.files:
                    self.files.append(file)

        self._update()
                    
    # def get_files_in_cache(self):
    #     files = []
    #     with open(self.filepath, "r") as cache:
    #         lines = reversed([line for line in cache])
    #         for line in lines:
    #             line = line.strip()
    #             file = Path(line)
    #             if file.exists():
    #                 files.append(file)

    #     return files
           
    def _update(self):
        with open(self.filepath, "w") as cache:
            for file in self.files:
                cache.write(str(file) + "\n")

    def remove(self, path:Path):
        self.files.remove(path)
        
        if path.is_dir():
            # shutil.rmtree(str(path))
            path.rmdir()
        else:
            path.unlink()

        self._update()

    def write(self):
        with open(self.filepath, "w+") as cache:
            for file in self.files:
                cache.write(str(file) + "\n")

    def clear(self):
        self.files.clear()
        with open(self.filepath, "w") as cache:
            pass

    def append(self, file_to_append: Path):
        with open(self.filepath, "a") as cache:
            if file_to_append not in self.files:
                cache.write(str(file_to_append) + "\n")
                self.files.append(file_to_append)

        self._update()

    def pop(self):
        elem =  self.files.pop()
        self._update()
        return elem

    def delete_all_files(self):
        for file in reversed(self.files):
            if file.is_dir():
                # shutil.rmtree(str(file))

                file.rmdir()
            else:
                file.unlink()

            print(f"Removed {file}")

        self.clear()

    def print(self):
        for file in self.files:
            print(file)

    def __str__(self):
        return str([file.name for file in self.files])

    def __repr__(self):
        # return f"Cache({self.files=}, {self.filepath=})"
        return str([f"{file.parent.name}/{file.name}" for file in self.files])

if __name__ == "__main__":

        
    a = Path("C:/Users/morri/OneDrive/Code/Python/Creating-Folder-Structure/A")
    if not a.exists():
        a.mkdir()
        a.chmod(0o777)  # Full read/write/execute permissions

    b = Path("C:/Users/morri/OneDrive/Code/Python/Creating-Folder-Structure/B")
    if not b.exists():
        b.mkdir()
        b.chmod(0o777)  # Full read/write/execute permissions

    c = Path("C:/Users/morri/OneDrive/Code/Python/Creating-Folder-Structure/C")
    if not c.exists():
        c.mkdir()
        c.chmod(0o777)  # Full read/write/execute permissions

    d = Path("C:/Users/morri/OneDrive/Code/Python/Creating-Folder-Structure/D")
    if not d.exists():
        d.mkdir()
        d.chmod(0o777)  # Full read/write/execute permissions

    cache = Cache(filename = "./.mytool_cache/test")
    print(cache)

    cache.append(a)
    cache.append(b)
    cache.append(c)
    print(cache)

    print(cache.clear())
    print(cache)

    # cache.remove(a)
    # print(cache)

    # cache.append(d)
    # print(cache)

    # cache.delete_all_files()
    # print(cache)