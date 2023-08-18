from json import load, dump
from os.path import relpath, join

def load_json(filepath: str):
    file_path = relpath(filepath)
    with open(file_path, "r", encoding="utf-8") as f:
        return load(f)

class ResourceLoader:
    def __init__(self, filepath: str):
        self.resources = load_json(filepath)
    
    def get_resource_path(self, start_path, resource):
        return relpath(join(start_path, self.resources[resource]))
    
    def grab_put(self, start_path, resource, key, extra_key):
        with open(self.get_resource_path(start_path, resource), "r", encoding="utf-8") as f:
            self.resources[key] = load(f)[extra_key]
    
    def update(self, start_path, resource, key, new_key):
        with open(self.get_resource_path(start_path, resource), "w", encoding="utf-8") as f:
            dump({new_key: self.resources[key]}, f)
