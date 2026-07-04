import json
import uuid

# Read 01_scheduler.json
with open('d:/work_for workflow/acb/workflows/n8n/01_scheduler.json', 'r') as f:
    wf = json.load(f)

nodes = wf['nodes']

# 1. Replace Postgres Trigger with Cron Trigger
trigger = next(n for n in nodes if n['name'].startswith('Trigger'))
trigger['type'] = 'n8n-nodes-base.cron'
trigger['parameters'] = {
    "triggerTimes": {
        "item": [
            {
                "mode": "custom",
                "cronExpression": "*/5 * * * * *"
            }
        ]
    }
}
# Remove credentials and webhookId from trigger
trigger.pop('credentials', None)
trigger.pop('webhookId', None)

# 2. Modify Consume Queue to select the next queue item, NOT using $json.id
consume_queue = next(n for n in nodes if n['name'] == 'Consume Queue')
consume_queue['parameters']['query'] = """
WITH deleted AS (
  DELETE FROM event_queue
  WHERE id = (
    SELECT id FROM event_queue
    WHERE queue_name = 'q_scheduler' AND status = 'QUEUED'
    ORDER BY created_at ASC
    LIMIT 1
    FOR UPDATE SKIP LOCKED
  )
  RETURNING *
)
SELECT * FROM deleted;
"""

# Regenerate ID to be safe
wf['id'] = str(uuid.uuid4())[:16]

# Save to 01_scheduler.json
with open('d:/work_for workflow/acb/workflows/n8n/01_scheduler.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("01_scheduler.json updated to use Cron successfully!")
