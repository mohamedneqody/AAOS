import urllib.request
import json
import time
import sys
import os

def main():
    print("Starting End-to-End Sprint 1 + Sprint 2 Validation...")
    
    # Trigger Sprint 1 workflow
    req = urllib.request.Request(
        'http://n8n:5678/webhook/execute-planning',
        data=b'{"intent": "Analyze customer activity and predict churn"}',
        method='POST',
        headers={'Content-Type': 'application/json'}
    )
    try:
        urllib.request.urlopen(req)
        print("Sprint 1 Webhook triggered. Waiting for completion...")
    except Exception as e:
        print(f"Failed to trigger webhook: {e}")
        sys.exit(1)

    time.sleep(30) # Wait for n8n to finish

    artifact_path = '/app/shared_libs/planning_result.json'
    if not os.path.exists(artifact_path):
        print(f"FAILED: {artifact_path} was not created by Sprint 1.")
        sys.exit(1)

    with open(artifact_path, 'r') as f:
        artifact = json.load(f)

    graph = artifact.get("execution_graph")
    if not graph:
        print("FAILED: No execution_graph in planning_result.json.")
        sys.exit(1)

    print("Sprint 1 Artifact generated. Dispatching ExecutionGraph to Sprint 2...")

    # Send ExecutionGraph to Dispatcher
    dispatch_req = urllib.request.Request(
        'http://localhost:8000/api/execution/dispatch',
        data=json.dumps(graph).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        res = urllib.request.urlopen(dispatch_req)
        execution_result = json.loads(res.read())
        print(f"\nExecution Result Status: {execution_result.get('status')}")
        print(f"Nodes executed: {execution_result.get('execution_metadata', {}).get('nodes_executed')}")
        
        plugins = execution_result.get("plugin_results", [])
        for pr in plugins:
            print(f" - Plugin {pr['plugin']}: {pr['status']} ({len(pr['evidence'])} evidence items)")
            
        print("\nSUCCESS: End-to-End Sprint 1 -> Sprint 2 complete!")
        print(json.dumps(execution_result, indent=2))
        
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.read().decode()}")
        sys.exit(1)
    except Exception as e:
        print(f"Exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
