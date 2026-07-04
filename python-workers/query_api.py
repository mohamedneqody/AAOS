import urllib.request
import base64
import json
import sys

url = f"http://n8n:5678/api/v1/executions/{sys.argv[1]}?includeData=true" if len(sys.argv) > 1 else "http://n8n:5678/api/v1/executions?limit=1"

auth = base64.b64encode(b"admin:admin").decode("ascii")
req = urllib.request.Request(url)
req.add_header("Authorization", f"Basic {auth}")
try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode('utf-8'))
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
