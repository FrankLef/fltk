import os
import json


def cached_token(jsonfile):
    def has_valid_token(data):
        return "token" in data

    def get_token_from_file():
        with open(jsonfile) as f:
            data = json.load(f)
            if has_valid_token(data):
                return data.get("token")

    def save_token_to_file(token):
        with open(jsonfile, "w") as f:
            json.dump({"token": token}, f)

    def decorator(fn):
        def wrapped(*args, **kwargs):
            if os.path.exists(jsonfile):
                token = get_token_from_file()
                if token:
                    return f"{token} (cached!!)"
            res = fn(*args, **kwargs)
            save_token_to_file(res)
            return res

        return wrapped

    return decorator


@cached_token("token-cache.json")
def get_token():
    # imaginary API call to get token
    import time

    time.sleep(3)
    return "7c5d3ca5-0088-49a7-ae30-011931a44075"


print(get_token())
