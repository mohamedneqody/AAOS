import json
import uuid

def create_http_node(name, url, position_x, previous_node=None):
    node_id = str(uuid.uuid4())
    node = {
        "id": node_id,
        "name": name,
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.1,
        "position": [position_x, 300],
        "parameters": {
            "method": "POST",
            "url": url,
            "sendBody": True,
            "specifyBody": "json"
        }
    }
    return node_id, node

nodes = []
connections = {}

# Trigger
trigger_id = str(uuid.uuid4())
nodes.append({
    "id": trigger_id,
    "name": "Webhook",
    "type": "n8n-nodes-base.webhook",
    "typeVersion": 1.1,
    "position": [100, 300],
    "webhookId": str(uuid.uuid4()),
    "parameters": {
        "path": "execute-planning",
        "httpMethod": "POST",
        "options": {}
    }
})

# Steps
steps = [
    ("Profiler Runtime", "http://python-worker:8000/api/planning/profiler", False),
    ("Semantic Runtime", "http://python-worker:8000/api/planning/semantic", True),
    ("Planner Agent", "http://python-worker:8000/api/planning/planner", True),
    ("Policy Runtime", "http://python-worker:8000/api/planning/policy", True),
    ("Execution Planner", "http://python-worker:8000/api/planning/execution-planner", True),
    ("Save Result", "http://python-worker:8000/api/planning/save-result", True)
]

prev_id = trigger_id
prev_name = "Webhook"
x = 300

for name, url, use_prev in steps:
    nid, node = create_http_node(name, url, x, prev_name if use_prev else None)
    
    # We must propagate "intent" and outputs to the next steps.
    # The webhook provides "intent" or we default to "Analyze customer activity".
    # We'll use n8n expressions to grab from Webhook and previous nodes.
    
    if name == "Profiler Runtime":
        node["parameters"]["jsonBody"] = "={ \"file_path\": \"/app/shared_libs/Book1.xlsx\" }"
    elif name == "Semantic Runtime":
        node["parameters"]["jsonBody"] = "={{ JSON.stringify({ profile: $json, intent: $('Webhook').item.json.body.intent || 'Analyze dataset and extract meaningful patterns' }) }}"
    elif name == "Planner Agent":
        node["parameters"]["jsonBody"] = "={{ JSON.stringify({ semantic_model: $json, profile: $('Profiler Runtime').item.json, intent: $('Webhook').item.json.body.intent || 'Analyze dataset and extract meaningful patterns' }) }}"
    elif name == "Policy Runtime":
        node["parameters"]["jsonBody"] = "={{ JSON.stringify({ capabilities: $json, profile: $('Profiler Runtime').item.json }) }}"
    elif name == "Execution Planner":
        # $json coming from Policy Runtime has {capabilities, policy_passed, violations}
        node["parameters"]["jsonBody"] = "={{ JSON.stringify({ capabilities: $json.capabilities }) }}"
    elif name == "Save Result":
        node["parameters"]["jsonBody"] = "={{ JSON.stringify($json) }}"
        
    nodes.append(node)
    
    if prev_name not in connections:
        connections[prev_name] = {"main": [[]]}
    connections[prev_name]["main"][0].append({"node": name, "type": "main", "index": 0})
    
    prev_id = nid
    prev_name = name
    x += 200

workflow = {
    "id": "plan123456789abc",
    "name": "ACB - 05_planning",
    "nodes": nodes,
    "connections": connections,
    "active": False,
    "settings": {
        "executionOrder": "v1"
    }
}

with open("d:/work_for workflow/acb/workflows/n8n/05_planning.json", "w") as f:
    json.dump(workflow, f, indent=2)

print("05_planning.json created")
