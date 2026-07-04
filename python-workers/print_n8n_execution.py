import psycopg2, json, sys

def decode_n8n_data(array):
    resolved = {}
    
    def resolve(index):
        if isinstance(index, str) and index.isdigit():
            index = int(index)
        
        if index in resolved:
            return resolved[index]
            
        if index >= len(array):
            return None
            
        value = array[index]
        
        if isinstance(value, str) and value.isdigit():
            return resolve(int(value))
        elif isinstance(value, list):
            res = []
            resolved[index] = res
            for item in value:
                res.append(resolve(item))
            return res
        elif isinstance(value, dict):
            res = {}
            resolved[index] = res
            for k, v in value.items():
                if k not in ['nodeExecutionStack', 'waitingExecution', 'source']: # Skip circular ref potentials
                    res[k] = resolve(v)
            return res
        else:
            resolved[index] = value
            return value

    return resolve(0)

conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute('SELECT "executionId", "data", "status", "startedAt", "stoppedAt" FROM execution_entity JOIN execution_data ON execution_entity.id = "executionId" ORDER BY "executionId" DESC LIMIT 1;')
row = cur.fetchone()
if not row:
    print("No execution found")
    sys.exit(0)

exec_id, raw_data, status, started, stopped = row
data = json.loads(raw_data)
decoded = decode_n8n_data(data)

print("="*60)
print("1. EXECUTION INFORMATION")
print("="*60)
print(f"Execution ID: {exec_id}")
print(f"Execution Status: {status}")
print(f"Execution Started: {started}")
print(f"Execution Stopped: {stopped}")
duration = (stopped - started).total_seconds() if stopped and started else 0
print(f"Execution Duration: {duration}s")

print("\n" + "="*60)
print("2. NODE EXECUTION DETAILS")
print("="*60)

run_data = decoded.get('resultData', {}).get('runData', {})
for node_name, executions in run_data.items():
    print(f"\n--- Node: {node_name} ---")
    for idx, exec_run in enumerate(executions):
        ex_time = exec_run.get('executionTime')
        error = exec_run.get('error')
        
        status_node = 'ERROR' if error else 'SUCCESS'
        print(f"Execution Status: {status_node}")
        print(f"Execution Time: {ex_time}ms")
        
        def safe_print_json(label, obj):
            try:
                # remove non serializable stuff
                clean = json.loads(json.dumps(obj, default=str))
                print(f"{label}:")
                print(json.dumps(clean, indent=2))
            except Exception as e:
                print(f"{label}: [Complex Object or Circular Ref]")

        input_data = []
        if 'data' in exec_run and 'main' in exec_run['data'] and len(exec_run['data']['main']) > 0:
            if exec_run['data']['main'][0]:
                for item in exec_run['data']['main'][0]:
                    if isinstance(item, dict) and 'json' in item:
                        input_data.append(item['json'])

        safe_print_json("Input", input_data)
        
        if error:
            print(f"Error: {error}")
