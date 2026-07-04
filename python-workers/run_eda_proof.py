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

# Clear execution entity to make it clean
cur.execute("DELETE FROM execution_entity;")
conn.commit()

print("======================================================")
print("1. SQL PROOF (BEFORE)")
print("======================================================")
counts_before = print_counts(cur, "Before any execution")
cur.execute("SELECT id, queue_name, status FROM event_queue;")
print("Queue State:", cur.fetchall())


correlation_id = f"eda-proof-{uuid.uuid4()}"
payload = {
    "correlation_id": correlation_id,
    "causation_id": str(uuid.uuid4()),
    "source": "manual_proof",
    "timestamp": time.time(),
    "type": "USER_REGISTRATION"
}

print("\n======================================================")
print("2. EXECUTING WORKFLOW (00_bootstrap ONLY)")
print("======================================================")
response = requests.post('http://n8n:5678/webhook/execute-bootstrap', json=payload)
print(f"Webhook HTTP Status: {response.status_code}")

print("\nWaiting 5 seconds for Event-Driven Architecture to complete the chain...")
time.sleep(5)  # Let 00_bootstrap insert into queue, and 01_scheduler process it.


print("\n======================================================")
print("3. SQL PROOF (AFTER EDA CHAIN)")
print("======================================================")
counts_after = print_counts(cur, "After Scheduler should have consumed the queue")
cur.execute("SELECT id, queue_name, status FROM event_queue;")
print("Queue State:", cur.fetchall())

print("\n======================================================")
print("4. N8N EXECUTION HISTORY (TWO EXECUTIONS EXPECTED)")
print("======================================================")
cur.execute('''
    SELECT e.id, w.name, e.status, e."startedAt", e."stoppedAt" 
    FROM execution_entity e
    JOIN workflow_entity w ON e."workflowId" = w.id
    ORDER BY e."startedAt" ASC
''')
rows = cur.fetchall()
for i, row in enumerate(rows):
    duration = (row[4] - row[3]).total_seconds() if row[4] and row[3] else 0
    print(f"\nExecution {i+1}")
    print(f"Workflow: {row[1]}")
    print(f"Status:   {row[2].upper()}")
    print(f"Started:  {row[3]}")
    print(f"Stopped:  {row[4]}")
    print(f"Duration: {duration}s")

if len(rows) == 2:
    diff = (rows[1][3] - rows[0][4]).total_seconds()
    print(f"\nTime difference between Bootstrap stopping and Scheduler starting: {diff}s")

print("\n======================================================")
print("5. SCHEDULER NODE EXECUTION (No skipped nodes)")
print("======================================================")
subprocess.run(["python", "/app/print_n8n_execution.py"])

