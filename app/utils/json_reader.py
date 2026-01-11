# app/utils/json_reader.py

import json


class JsonReader:
    def __init__(self, output_path: str) -> None:
        self.output_path = output_path

    def read_json_with_load(self):
        with open(self.output_path, "r") as json_file:
            return json.load(json_file)

    def read_json_with_line(self):
        with open(self.output_path, "r") as fp:
            json_file = []
            for line in fp:
                json_file.append(json.loads(line.strip()))
        return json_file
