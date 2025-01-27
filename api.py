import os
import requests
from flask import Flask, jsonify
from dotenv import load_dotenv
from .constants import STRONG_API_BASE_URL
load_dotenv()

import json

def get_access_token():
    """Gets the access token from the request cookies."""
    email = os.getenv("username")
    password = os.getenv("password")
    # Send login request to Strong App API
    response = requests.post(
        f"{STRONG_API_BASE_URL}/auth/login",
        json={"usernameOrEmail": email, "password": password},
        headers={
            "Content-Type": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "x-client-platform": "ios",
            "accept-language": "en-US,en;q=0.9",
            "x-client-build": "8039",
            "User-Agent": "Strong iOS",
            "sentry-trace": "513627f9dbf64187a06723df9f5888c0-a684d4f373184e1e-0",
        },
    )

    print(response.json())

    if response.status_code == 200:
        auth_data = response.json()
        return auth_data["accessToken"]
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
def get_data():
    """Fetches all the data from Strong App API."""
    access_token = get_access_token()
    url = "https://back.strong.app/api/users/d8bde7f2-0b70-4adf-beb5-b1dd2a48230e/?continuation=&limit=300&include=template&include=log&include=measurement&include=widget&include=tag&include=folder&include=metric&include=measuredValue"

    payload = ""
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'x-client-platform': 'ios',
    'accept-language': 'en-US,en;q=0.9',
    'x-client-build': '8039',
    'User-Agent': 'Strong iOS',
    'sentry-trace': '513627f9dbf64187a06723df9f5888c0-a684d4f373184e1e-0',
    'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(url, headers=headers, data=payload)
    # save to json file
    try:
        with open("data/data.json", "w") as file:
            json.dump(response.json(), file, indent=4)
    except FileNotFoundError:
        print("File not found")
    