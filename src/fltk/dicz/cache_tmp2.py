import os
import json
import joblib  # pip install joblib
import tempfile


def get_persisted_cache(file_path):
    cache_dir = os.path.join(tempfile.gettempdir(), "my_app_cache")
    os.makedirs(cache_dir, exist_ok=True)

    cache_path = os.path.join(cache_dir, "cached_data.joblib")
    file_mtime = os.path.getmtime(file_path)

    # Check if cache exists and is fresh
    if os.path.exists(cache_path):
        cached_info = joblib.load(cache_path)
        if cached_info["timestamp"] == file_mtime:
            return cached_info["data"]

    # Otherwise, read the file and create a new cache
    print("Rebuilding persistent cache...")
    with open(file_path, "r") as f:
        data = json.load(f)

    joblib.dump({"timestamp": file_mtime, "data": data}, cache_path)
    return data
