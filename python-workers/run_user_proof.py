import psycopg2
import requests
import json
import subprocess
import time
import uuid

def print_counts(cur, label):
    print(f"\n--- {label} ---")
    cur.execute("SELECT COUNT(*) FROM tasks;")
    tasks = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM task_states;")
    task_states = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM event_queue;")
    event_queue = cur.fetchone()[0]
    
    print(f"Tasks count: {tasks}")
    print(f"Task_states count: {task_states}")
    print(f"Event_queue count: {event_queue}")
    return tasks, task_states, event_queue

conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()

print("======================================================")
print("SQL PROOF (BEFORE FIRST EXECUTION)")
print("======================================================")
counts_before = print_counts(cur, "Before execution")

correlation_id = f"proof-test-{uuid.uuid4()}"
payload = {
    "correlation_id": correlation_id,
    "causation_id": str(uuid.uuid4()),
    "source": "manual_proof",
    "timestamp": time.time(),
    "type": "USER_REGISTRATION"
}

print("\n======================================================")
print("EXECUTING WORKFLOW (FIRST RUN)")
print("======================================================")
response = requests.post('http://n8n:5678/webhook/execute-bootstrap', json=payload)
print(f"Webhook HTTP Status: {response.status_code}")
print(f"Webhook Response: {response.text}")
time.sleep(2)  # Give DB time to settle

print("\n======================================================")
print("SQL PROOF (AFTER FIRST EXECUTION)")
print("======================================================")
counts_after1 = print_counts(cur, "After first execution")
print("\nExplanation of changes:")
print(f"Tasks increased by {counts_after1[0] - counts_before[0]} (Expected: 1 for the new task)")
print(f"Task_states increased by {counts_after1[1] - counts_before[1]} (Expected: 4 for NEW, QUEUED, RUNNING, COMPLETED)")
print(f"Event_queue increased by {counts_after1[2] - counts_before[2]} (Expected: 1 for q_scheduler)")


print("\n======================================================")
print("EXECUTING WORKFLOW (SECOND RUN - IDEMPOTENCY CHECK)")
print("======================================================")
response2 = requests.post('http://n8n:5678/webhook/execute-bootstrap', json=payload)
print(f"Webhook HTTP Status: {response2.status_code}")
print(f"Webhook Response: {response2.text}")
time.sleep(2)

print("\n======================================================")
print("SQL PROOF (AFTER SECOND EXECUTION)")
print("======================================================")
counts_after2 = print_counts(cur, "After second execution")
print("\nExplanation of changes:")
print(f"Tasks increased by {counts_after2[0] - counts_after1[0]} (Expected: 0, duplicate prevented)")
print(f"Task_states increased by {counts_after2[1] - counts_after1[1]} (Expected: 1 for RUNNING, then stops)")
print(f"Event_queue increased by {counts_after2[2] - counts_after1[2]} (Expected: 0)")


print("\n======================================================")
print("N8N ACTUAL EXECUTION LOG (FROM N8N DATABASE)")
print("======================================================")
subprocess.run(["python", "/app/print_n8n_execution.py"])

