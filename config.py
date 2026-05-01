import json

def load_config(filepath="config.json"):
    with open(filepath, "r") as f:
        data = json.load(f)
        return data

def store_config(data, filepath="config.json"):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

# Load credentials from the JSON file
def load_google_config(filepath="client_secret.json"):
    with open(filepath, "r") as f:
        data = json.load(f)
        # Google JSONs wrap keys in 'web' or 'installed' depending on app type
        return data.get("web") or data.get("installed")