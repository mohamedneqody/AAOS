import requests
import time
import psycopg2
import json

def run_tests():
    n8n_conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
    n8n_conn.autocommit = True
    
    for i in range(5):
        print(f"\n==========================================")
        print(f"EXECUTION {i+1} / 5")
        print(f"==========================================")
        
        # Trigger Webhook
        try:
            res = requests.post('http://n8n:5678/webhook/execute-bootstrap', json={"correlation_id": f"test-run-{i}"})
            print(f"Webhook Status: {res.status_code}")
        except Exception as e:
            print(f"Webhook Error: {e}")
            
        time.sleep(3) # Wait for n8n to complete execution
        
        # Get Execution Data
        cur = n8n_conn.cursor()
        cur.execute('SELECT id, status, "startedAt", "stoppedAt" FROM execution_entity ORDER BY id DESC LIMIT 1;')
        exec_row = cur.fetchone()
        
        if exec_row:
            exec_id, status, started_at, stopped_at = exec_row
            duration = (stopped_at - started_at).total_seconds() if stopped_at and started_at else "N/A"
            
            # Count executed nodes (by looking at execution_data)
            cur.execute('SELECT data FROM execution_data WHERE "executionId" = %s', (exec_id,))
            data_row = cur.fetchone()
            executed_nodes = 0
            failed_nodes = "None"
            if data_row:
                data = data_row[0]
                if isinstance(data, str):
                    data = json.loads(data)
                
                # N8n compresses execution data in v1. 
                # It's an array, lastNodeExecuted is somewhere.
                # Just trying to extract it heuristically if compressed
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            if "resultData" in item and isinstance(item["resultData"], dict):
                                rd = item["resultData"]
                                if "runData" in rd:
                                    executed_nodes = len(rd["runData"].keys())
                                if "error" in rd:
                                    failed_nodes = rd["lastNodeExecuted"]
                                break
                            # If it's the compressed format, look for dicts with specific keys
                            if "error" in item:
                                failed_nodes = "Unknown (Compressed)"
            
            print(f"Execution ID: {exec_id}")
            print(f"Start Time: {started_at}")
            print(f"End Time: {stopped_at}")
            print(f"Duration: {duration}s")
            print(f"Status: {status}")
            print(f"Trigger: Webhook")
            print(f"Number of executed nodes: {executed_nodes} (approx)")
            print(f"Failed nodes: {failed_nodes}")
            
        else:
            print("No execution found in n8n DB.")

        print("\n--- Database Verification ---")
        # tasks
        cur.execute("SELECT id, type, status FROM tasks ORDER BY created_at DESC LIMIT 1;")
        print("TASKS:", cur.fetchall())
        
        # task_states
        cur.execute("SELECT id, task_id, current_state FROM task_states ORDER BY updated_at DESC LIMIT 1;")
        print("TASK_STATES:", cur.fetchall())
        
        # event_queue
        cur.execute("SELECT id, queue_name, status FROM event_queue ORDER BY created_at DESC LIMIT 1;")
        print("EVENT_QUEUE:", cur.fetchall())
        
        # logs
        cur.execute("SELECT id, message, event_id FROM logs ORDER BY created_at DESC LIMIT 1;")
        print("LOGS:", cur.fetchall())

if __name__ == '__main__':
    run_tests()
