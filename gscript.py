import requests
import json

from config import load_config, store_config, load_google_config
config = load_config()

def get_script():
    if config.get("gscript"):
        return config.get("gscript")
    
    headers = {
        "Authorization": f"Bearer {config['google']['access_token']}",
    }

    payload = {
        "title": "My WebApp Project"
    }

    # 2. Exchange for tokens
    response = requests.post("https://script.googleapis.com/v1/projects", data=payload, headers=headers)
    if response.status_code != 200:
        return {"error": "Exchange failed", "details": response_data}

    response_data = response.json()
    config["gscript"] = response_data
    store_config(config)

    return response_data

def update_script():
    if not config.get("gscript"):
        raise "No script"
    
    headers = {
        "Authorization": f"Bearer {config['google']['access_token']}",
    }

    payload = {
        "files": [
            {
                "name": "Code",
                "type": "SERVER_JS",
                "source": "function doGet(e){return ContentService.createTextOutput('Hello World 2');}"
            },
            {
                "name": "appsscript",
                "type": "JSON",
                "source": json.dumps({
                    "runtimeVersion": "V8",
                    "timeZone": "Etc/UTC",
                    "webapp": {
                        "access": "ANYONE_ANONYMOUS",
                        "executeAs": "USER_DEPLOYING"
                    }
                })
            },
        ]
    }

    # 2. Exchange for tokens
    response = requests.put(f"https://script.googleapis.com/v1/projects/{config['gscript']['scriptId']}/content", json=payload, headers=headers)
    if response.status_code != 200:
        return {"error": "Exchange failed", "details": response_data}

    response_data = response.json()
    config["gscript"].update(response_data)
    store_config(config)

    return response_data

def add_version():
    if not config.get("gscript"):
        raise "No script"
    
    headers = {
        "Authorization": f"Bearer {config['google']['access_token']}",
    }

    payload = { "description": "First Web App version" }

    # 2. Exchange for tokens
    response = requests.post(f"https://script.googleapis.com/v1/projects/{config['gscript']['scriptId']}/versions", json=payload, headers=headers)
    response_data = response.json()

    if response.status_code != 200:
        return {"error": "Exchange failed", "details": response_data}

    config["gscript"].update(response_data)
    store_config(config)

    return response_data

def deploy_script():
    if not config.get("gscript"):
        raise "No script"
    
    headers = {
        "Authorization": f"Bearer {config['google']['access_token']}",
    }

    payload = {
        "versionNumber": config['gscript']['versionNumber'],
        "manifestFileName": "appsscript",
        "description": "Web App deploy"
    }

    # 2. Exchange for tokens
    response = requests.post(f"https://script.googleapis.com/v1/projects/{config['gscript']['scriptId']}/deployments", json=payload, headers=headers)
    response_data = response.json()

    if response.status_code != 200:
        return {"error": "Exchange failed", "details": response_data}

    config["gscript"].update(response_data)
    store_config(config)

    return response_data

def refresh_token(google_config):
    if not config.get("google", {}).get("refresh_token"):
        raise "no refresh token"

    payload = {
        "grant_type": "refresh_token",
        "redirect_uri": "postmessage",
        "refresh_token": config["google"]["refresh_token"],
        "client_id": google_config.get("client_id"),
        "client_secret": google_config.get("client_secret"),
    }

    # 2. Exchange for tokens
    response = requests.post("https://oauth2.googleapis.com/token", data=payload)
    if response.status_code != 200:
        return {"error": "Exchange failed", "details": response_data}

    response_data = response.json()
    config["google"].update(response_data)
    store_config(config)

    return response_data



if __name__ == "__main__":
    google_config = load_google_config()
    GOOGLE_CLIENT_ID = google_config.get("client_id")
    GOOGLE_CLIENT_SECRET = google_config.get("client_secret")

    refresh_token(google_config);

    gscript = get_script()
    # print(gscript)

    s = update_script()
    # s = add_version()
    s = deploy_script()
    print(s)