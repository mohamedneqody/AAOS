import os
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

def get_token():
    creds = service_account.Credentials.from_service_account_file(
        'sa.json', 
        scopes=['https://www.googleapis.com/auth/generative-language']
    )
    request = Request()
    creds.refresh(request)
    return creds.token

def test_gemini(token):
    url = "https://generativelanguage.googleapis.com/v1beta/models"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    print("Status Code:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    try:
        token = get_token()
        print("Got token successfully")
        test_gemini(token)
    except Exception as e:
        print(f"Error: {e}")
