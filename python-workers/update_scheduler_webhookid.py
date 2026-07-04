import json
import uuid

with open('d:/work_for workflow/acb/workflows/n8n/01_scheduler.json', 'r') as f:
    wf = json.load(f)

nodes = wf['nodes']

# Add webhookId to Postgres Trigger
trigger = next(n for n in nodes if n['name'].startswith('Trigger'))
trigger['webhookId'] = str(uuid.uuid4())

wf['id'] = str(uuid.uuid4())[:16]

with open('d:/work_for workflow/acb/workflows/n8n/01_scheduler.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("01_scheduler.json updated to include webhookId!")
