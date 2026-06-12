# Adding in Local JSONL Storage v0.2.1 STEP 5
import json


class JsonlStorage:
    def __init__(self, path):
        self.path = path

    def write(self, event):
        with open(self.path, "a", encoding="utf-8") as file:
            file.write(json.dumps(event) + "\n")
