# Adding in the ability to read JSONL Logs 

import json
from pathlib import Path


class JsonlStorage:
    def __init__(self, path):
        self.path = Path(path)

    def write(self, event):
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event) + "\n")

    def read_all(self):
        if not self.path.exists():
            return []

        events = []

        with self.path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                events.append(json.loads(line))

        return events
    
    

