import psycopg2
import json

conn = psycopg2.connect("host=postgres port=5432 dbname=acb_db user=acb_user password=acb_pass")
cur = conn.cursor()
cur.execute('SELECT e.id, e."startedAt", e."stoppedAt", e.status, d.data FROM execution_entity e JOIN execution_data d ON e.id = d."executionId" ORDER BY e."startedAt" DESC LIMIT 1;')
row = cur.fetchone()
if row:
    print(f"Status: {row[3]}")
    data = json.loads(row[4]) if isinstance(row[4], str) else row[4]
    print(f"Status: {row[3]}")
    runData = {}
    if isinstance(data, dict):
        runData = data.get("resultData", {}).get("runData", {})
    elif isinstance(data, list):
        print("Data is a list, possibly compressed or different schema.")
        # Try to parse the execution_entity.data if that's what's needed
    
    for node, node_data in runData.items():
        print(f"Node: {node}")
        print(f"StartTime: {node_data[0].get('startTime')}")
        print(f"ExecutionTime: {node_data[0].get('executionTime')}")
        print("---")

