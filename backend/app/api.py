import os
import requests
from flask import Flask, jsonify
from dotenv import load_dotenv
from app.constants import STRONG_API_BASE_URL, JSON_FILE_PATH
from app.logger import logger

load_dotenv()
import json

def get_auth():
    """Gets the access token from the request cookies."""
    try:
        email = os.getenv("username")
        password = os.getenv("password")
        # Send login request to Strong App API
        if not email or not password:
            logger.error("❌ Missing username or password in environment variables.")
            return None
        
        print("🔑 Requesting new access token...")
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

        if response.status_code == 200:
            auth_data = response.json()
            if auth_data:
                logger.info("✅ Access token retrieved successfully.")
                return  {
                    "access_token": auth_data["accessToken"],
                    "user_id": auth_data['userId']
                }
            else:
                logger.error("❌ Access token missing in response.")
                return None
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except ValueError as e:
        logger.error(str(e))
        return None
    except requests.RequestException as e:
        logger.error(f"❌ Request failed: {e}")
        return None
    
def get_data():
    """Fetches all the data from Strong App API."""
    auth_data = get_auth()
    access_token = auth_data['access_token']
    user_id= auth_data['user_id']
    if not auth_data:
        logger.error("❌ No access token. Aborting data fetch.")
        return
    
    url = f"https://back.strong.app/api/users/{user_id}/?continuation=&limit=300&include=template&include=log&include=measurement&include=widget&include=tag&include=folder&include=metric&include=measuredValue"

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
    try:
        response = requests.get(url, headers=headers, data=payload)
        if response.status_code == 200:
            logger.info("✅ Data fetched successfully.")
            try:
                with open(JSON_FILE_PATH, "w") as file:
                    json.dump(response.json(), file, indent=4)
                logger.info(f"✅ Data saved at {JSON_FILE_PATH}")
                return {"status": "success", "message": "Data fetched and saved successfully."}         
            except Exception as e:
                logger.error(f"❌ Failed to save data.json: {e}")
                return {"status": "error", "message": f"Failed to save data: {e}"}
        else:
            logger.error(f"❌ Failed to fetch data. Status: {response.status_code} - {response.text}")
            return {"status": "error", "message": f"Failed to fetch data. Status: {response.status_code}"}

    except requests.RequestException as e:
        logger.error(f"❌ Request failed: {e}")
        return {"status": "error", "message": f"Request failed: {e}"}

if __name__ == "__main__":
    get_data()