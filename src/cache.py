from pathlib import Path
from constants import DEFAULT_CACHE


class Cache():
    def __init__(self, filename: str | Path = DEFAULT_CACHE):
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

    def append(self, files_to_append: list[Path]):
        for file in files_to_append:
            if file not in self.files:
                self.files.append(file)

        self._update()

    def pop(self):
        elem =  self.files.pop()
        self._update()
        return elem

    def delete_all_files(self, verbose:bool = False):
        if verbose:
            print("Deleted files found in cache")

        while self.files:
            file = self.files.pop()
            if file.is_dir():
                try:
                    file.rmdir()
                except Exception as e:
                    file.chmod(0o777)
                    file.rmdir()
            else:
                file.unlink()

            if verbose:
                print(f"Removed {file}")

        self.clear()

    def print(self):
        for file in self.files:
            print(file)

    def __str__(self):
        if self.files:
            return "\n".join(str(file) for file in self.files)
        return "Cache Empty"

    def __repr__(self):
        # return f"Cache({self.files=}, {self.filepath=})"
        return str([f"{file.parent.name}/{file.name}" for file in self.files])