import requests
import json

base_url = "http://localhost:8000/api/planning"
file_path = "/app/shared_libs/Book1.xlsx"

print("=== PROFILER ===")
prof_res = requests.post(f"{base_url}/profiler", json={"file_path": file_path}).json()
print(json.dumps(prof_res, indent=2))

print("\n=== SEMANTIC MODEL ===")
sem_res = requests.post(f"{base_url}/semantic", json={"profile": prof_res, "intent": "Analyze customer activity and predict churn"}).json()
print(json.dumps(sem_res, indent=2))

print("\n=== PLANNER LOGICAL PLAN ===")
plan_res = requests.post(f"{base_url}/planner", json={"semantic_model": sem_res, "profile": prof_res, "intent": "Analyze customer activity and predict churn"}).json()
print(json.dumps(plan_res, indent=2))

print("\n=== POLICY VALIDATION ===")
pol_res = requests.post(f"{base_url}/policy", json={"capabilities": plan_res, "profile": prof_res}).json()
print(json.dumps(pol_res, indent=2))

print("\n=== EXECUTION DAG ===")
dag_res = requests.post(f"{base_url}/execution-planner", json={"capabilities": plan_res}).json()
print(json.dumps(dag_res, indent=2))
