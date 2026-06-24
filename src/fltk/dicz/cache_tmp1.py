import os
import json

# Global cache dictionary and timestamp tracker
_file_cache = {"data": None, "last_modified": 0}


def get_cached_file_data(file_path):
    # Get the last modification time of the external file
    current_mtime = os.path.getmtime(file_path)

    # Invalidate the cache if the file has been updated
    if current_mtime > _file_cache["last_modified"]:
        print("File updated or cache empty. Reloading...")
        with open(file_path, "r") as file:
            _file_cache["data"] = json.load(file)
            _file_cache["last_modified"] = current_mtime

    return _file_cache["data"]


# Example usage
# data = get_cached_file_data('data.json')
