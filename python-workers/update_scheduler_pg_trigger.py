import json
import uuid

with open('d:/work_for workflow/acb/workflows/n8n/01_scheduler.json', 'r') as f:
    wf = json.load(f)

nodes = wf['nodes']

# Replace Schedule Trigger with Postgres Trigger using correct v1+ syntax
trigger = next(n for n in nodes if n['name'].startswith('Trigger'))
trigger['type'] = 'n8n-nodes-base.postgresTrigger'
trigger['parameters'] = {
  "triggerMode": "createTrigger",
  "schema": {
    "mode": "name",
    "value": "public"
  },
  "tableName": {
    "mode": "name",
    "value": "event_queue"
  },
  "firesOn": "INSERT",
  "additionalFields": {
    "replaceIfExists": True,
    "channelName": "n8n_scheduler_queue",
    "functionName": "n8n_scheduler_trigger_fn",
    "triggerName": "n8n_scheduler_trigger"
  }
}
trigger['credentials'] = {
  "postgres": {
    "id": "creds_postgres_1",
    "name": "ACB Postgres"
  }
}

# The Queue consumption is still using SELECT ... FOR UPDATE SKIP LOCKED
# which is good.

wf['id'] = str(uuid.uuid4())[:16]

with open('d:/work_for workflow/acb/workflows/n8n/01_scheduler.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("01_scheduler.json updated to use PostgresTrigger with correct schema/tableName resourceLocator!")
