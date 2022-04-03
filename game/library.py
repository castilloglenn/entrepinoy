import json
import os


class Library():
    """
    The library contains all the data from the json folder with the same name.
    """
    def __init__(self):
        self.business = self.get_dict_from_json("business.json")
    
    
    def get_dict_from_json(self, json_name: str):
        dirname = os.path.dirname(__file__)
        skills_path = os.path.join(dirname, "..", "library", json_name)

        with open(skills_path) as skills_json:
            json_dict = json.load(skills_json)
            return json_dict


