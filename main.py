import argparse
import json
import requests
from flask import Flask, request, jsonify
from config import load_config, store_config, load_google_config

app = Flask(__name__, static_folder='static')

google_config = load_google_config()
GOOGLE_CLIENT_ID = google_config.get("client_id")
GOOGLE_CLIENT_SECRET = google_config.get("client_secret")

config = load_config()

@app.route('/')
def index():
    # Serves index.html from the /static folder
    return app.send_static_file('index.html')


@app.route('/auth/google', methods=['POST'])
def validate_google_popup_code():
    data = request.get_json()
    auth_code = data.get('code')
    
    # 1. The special redirect_uri for popup/postMessage flows
    # This is a literal string and usually doesn't need to be in Google Console
    REDIRECT_URI = "postmessage" 

    payload = {
        'code': auth_code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI, # MUST be "postmessage"
        'grant_type': 'authorization_code'
    }

    # 2. Exchange for tokens
    response = requests.post("https://oauth2.googleapis.com/token", data=payload)
    token_data = response.json()

    if response.status_code != 200:
        return jsonify({"error": "Exchange failed", "details": token_data}), 400

    config["google"] = token_data
    store_config(config)

    return jsonify(token_data)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')        # string or None
    page = request.args.get('page', 1)   # default value
    page = int(page)

    return jsonify({
        "query": query,
        "page": page
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Flask app on a custom port.")
    parser.add_argument("-p", "--port", required=False, type=int, default=5000, help="Port to run on")
    args = parser.parse_args()

    port = args.port or 5000


    app.run(debug=True, port=port)