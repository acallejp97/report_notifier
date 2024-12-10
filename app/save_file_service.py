class SaveService:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def save(self, lines: list):
        with open(self.filename, "w") as f:
            for line in lines:
                f.write(line)

    def read(self):
        with open(self.filename, "r") as f:
            return f.read()
