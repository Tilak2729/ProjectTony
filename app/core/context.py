from pathlib import Path


class TonyContext:

    def __init__(self):

        self.current_directory = Path.cwd()
        self.current_project = None

    def set_directory(self, path):

        path = Path(path).expanduser().resolve()

        if not path.exists():
            return False, f"{path} does not exist."

        if not path.is_dir():
            return False, f"{path} is not a directory."

        self.current_directory = path

        return True, path

    def get_directory(self):

        return self.current_directory

    def set_project(self, path):

        path = Path(path).expanduser().resolve()

        if not path.exists():
            return False, f"{path} does not exist."

        if not path.is_dir():
            return False, f"{path} is not a directory."

        self.current_project = path
        self.current_directory = path

        return True, path

    def get_project(self):

        return self.current_project

    def clear_project(self):

        self.current_project = None