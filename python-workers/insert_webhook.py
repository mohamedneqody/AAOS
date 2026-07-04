import psycopg2
import json

with open('/workflows/n8n/05_planning.json', 'r') as f:
    wf = json.load(f)

webhook_id = ''
for node in wf['nodes']:
    if node['type'] == 'n8n-nodes-base.webhook':
        webhook_id = node['webhookId']
        break

conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute("DELETE FROM webhook_entity WHERE \"webhookPath\" = 'execute-planning';")
cur.execute("INSERT INTO webhook_entity (\"webhookPath\", \"method\", \"node\", \"webhookId\", \"pathLength\", \"workflowId\") VALUES ('execute-planning', 'POST', 'Webhook', %s, 1, 'plan123456789abc');", (webhook_id,))
conn.commit()
print(f"Webhook inserted with ID {webhook_id}")
