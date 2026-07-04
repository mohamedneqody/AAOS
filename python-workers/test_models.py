import urllib.request, json, os
import sys
sys.path.append('/app')
from shared_libs.ai_service.gemini import GeminiProvider

token = GeminiProvider().get_token()
url = 'https://generativelanguage.googleapis.com/v1beta/models'
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
try:
    res = urllib.request.urlopen(req)
    data = json.loads(res.read())
    print([m['name'] for m in data.get('models', [])])
except Exception as e:
    print(e)
    if hasattr(e, 'read'): print(e.read().decode())
