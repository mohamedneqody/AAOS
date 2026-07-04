import urllib.request, json, time, subprocess

def is_ready():
    try:
        req = urllib.request.Request('http://localhost:8000/api/planning/profiler', data=json.dumps({'file_path': '/app/shared_libs/Book1.xlsx'}).encode(), headers={'Content-Type': 'application/json'})
        res = urllib.request.urlopen(req)
        profile = json.loads(res.read())

        req = urllib.request.Request('http://localhost:8000/api/planning/semantic', data=json.dumps({'profile': profile, 'intent': 'Predict churn'}).encode(), headers={'Content-Type': 'application/json'})
        res = urllib.request.urlopen(req)
        semantic = json.loads(res.read())
        
        req = urllib.request.Request('http://localhost:8000/api/planning/planner', data=json.dumps({'semantic_model': semantic, 'profile': profile, 'intent': 'Predict churn'}).encode(), headers={'Content-Type': 'application/json'})
        res = urllib.request.urlopen(req)
        return True
    except Exception as e:
        if hasattr(e, 'read'): print(e.read().decode())
        return False

print('Waiting for API rate limit to reset...')
while not is_ready():
    print('Still waiting... Sleeping for 60s to save quota.')
    time.sleep(60)

print('API ready! Running validation script...')
subprocess.run(['python', 'validate_sprint1.py'])
