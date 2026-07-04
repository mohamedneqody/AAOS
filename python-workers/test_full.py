import urllib.request, json
import sys
sys.path.append('/app')
from shared_libs.ai_service.gemini import GeminiProvider

provider = GeminiProvider()

req = urllib.request.Request('http://localhost:8000/api/planning/profiler', data=json.dumps({'file_path': '/app/shared_libs/Book1.xlsx'}).encode(), headers={'Content-Type': 'application/json'})
res = urllib.request.urlopen(req)
profile = json.loads(res.read())

req = urllib.request.Request('http://localhost:8000/api/planning/semantic', data=json.dumps({'profile': profile, 'intent': 'Predict churn', 'model_name': 'gemini-flash-latest'}).encode(), headers={'Content-Type': 'application/json'})
res = urllib.request.urlopen(req)
semantic = json.loads(res.read())
print('Semantic success!')

req = urllib.request.Request('http://localhost:8000/api/planning/planner', data=json.dumps({'semantic_model': semantic, 'profile': profile, 'intent': 'Predict churn', 'model_name': 'gemini-flash-latest'}).encode(), headers={'Content-Type': 'application/json'})
res = urllib.request.urlopen(req)
plan = json.loads(res.read())
print('Planner success!')
print('Capabilities:', plan.get('capabilities', []))
