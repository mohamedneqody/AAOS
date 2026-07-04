import json

with open('d:/work_for workflow/acb/workflows/n8n/00_bootstrap.json', 'r') as f:
    wf = json.load(f)

# Change workflow name
wf['name'] = 'ACB - 01_scheduler'

nodes = wf['nodes']
connections = wf['connections']

# 1. Replace Trigger
trigger = next(n for n in nodes if n['name'].startswith('Trigger'))
trigger['name'] = 'Trigger (01_scheduler)'
trigger['type'] = 'n8n-nodes-base.postgresTrigger'
trigger['parameters'] = {
    "schema": "public",
    "table": "event_queue",
    "events": ["insert"]
}
trigger['credentials'] = {
    "postgres": {"id": "creds_postgres_1", "name": "ACB Postgres"}
}

# 2. Add Consume Queue node
consume_queue = {
    "id": "1b",
    "name": "Consume Queue",
    "type": "n8n-nodes-base.postgres",
    "position": [trigger['position'][0] + 200, trigger['position'][1]],
    "typeVersion": 1,
    "parameters": {
        "operation": "executeQuery",
        "query": "WITH deleted AS (\n  DELETE FROM event_queue\n  WHERE id = '{{ $json.id }}' AND queue_name = 'q_scheduler' AND status = 'QUEUED'\n  RETURNING *\n)\nSELECT * FROM deleted;"
    },
    "credentials": {
        "postgres": {"id": "creds_postgres_1", "name": "ACB Postgres"}
    }
}
nodes.append(consume_queue)

# 3. Update Event Envelope Validation
env_val = next(n for n in nodes if n['name'] == 'Event Envelope Validation')
env_val['type'] = 'n8n-nodes-base.code'
env_val['parameters'] = {
    "jsCode": """
const qRow = $('Consume Queue').first().json || {};
return {
  event_id: qRow.id,
  task_id: qRow.payload.task_id,
  correlation_id: qRow.payload.correlation_id || qRow.payload.task_id,
  timestamp: new Date().toISOString(),
  payload: qRow.payload
};
"""
}
env_val['position'][0] += 200  # Shift it

# Fix connections
# Old: Trigger -> Event Envelope Validation
# New: Trigger -> Consume Queue -> Event Envelope Validation
connections['Trigger (01_scheduler)'] = {
    "main": [[{"node": "Consume Queue", "type": "main", "index": 0}]]
}
del connections['Trigger (00_bootstrap)']

connections['Consume Queue'] = {
    "main": [[{"node": "Event Envelope Validation", "type": "main", "index": 0}]]
}

# Update other nodes
for n in nodes:
    if n['name'] == 'Execute 00_bootstrap':
        n['name'] = 'Execute 01_scheduler'
        n['parameters']['jsCode'] = n['parameters']['jsCode'].replace('Bootstrap', 'Scheduler')
    elif n['name'] == 'Postgres: Push to Next Queue':
        n['parameters']['query'] = n['parameters']['query'].replace('q_scheduler', 'q_dispatcher')
    elif n['name'] == 'Logging':
        n['parameters']['query'] = n['parameters']['query'].replace('Bootstrap', 'Scheduler')

# Re-link Execute 00_bootstrap -> Execute 01_scheduler
if 'Execute 00_bootstrap' in connections:
    connections['Execute 01_scheduler'] = connections.pop('Execute 00_bootstrap')
for k, v in connections.items():
    for conn_arr in v.get('main', []):
        for conn_item in conn_arr:
            if conn_item['node'] == 'Execute 00_bootstrap':
                conn_item['node'] = 'Execute 01_scheduler'

# Save to 01_scheduler.json
with open('d:/work_for workflow/acb/workflows/n8n/01_scheduler.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("01_scheduler.json updated successfully!")
