import os

from constants import HASH_DIR


class SaveService:
    def __init__(self, filename: str = "mock_file") -> None:
        self.filename = os.path.join(os.getcwd(), HASH_DIR, filename)

    def save(self, lines: list):
        self._check_filename()
        with open(self.filename, "w") as f:
            for line in lines:
                f.write(line)

    def read(self):
        self._check_filename()
        if not os.path.exists(self.filename):
            return None
        with open(self.filename, "r") as f:
            return f.read()

    def delete(self):
        self._check_filename()
        os.remove(self.filename)

    def update_filename(self, new_filename: str):
        self.filename = os.path.join('/usr/share/app', HASH_DIR, new_filename)

    def _check_filename(self):
        if self.filename == "mock_file":
            raise ValueError(
                "File name is not set. Please define it calling update_filename method or when SaveService is instantiated"
            )
