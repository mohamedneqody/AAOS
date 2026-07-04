import google.auth
from google.auth.transport.requests import Request
import urllib.request
import json
import traceback

def test_vertex():
    project_id = "gen-lang-client-0319131014"
    location = "us-central1"
    model = "gemini-2.5-pro"
    credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
    credentials.refresh(Request())
    access_token = credentials.token
    
    url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/publishers/google/models/{model}:generateContent"
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": "Hello"}]}]
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    
    print(f"HTTP Request URL: {url}")
    print(f"HTTP Request Body: {json.dumps(payload)}")
    
    try:
        res = urllib.request.urlopen(req)
        print("HTTP Response: ")
        print(res.read().decode())
    except Exception as e:
        print("HTTP Error Caught:")
        print(e)
        if hasattr(e, 'read'):
            print("HTTP Response Body:")
            print(e.read().decode())
        traceback.print_exc()

if __name__ == "__main__":
    test_vertex()
