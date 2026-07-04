import urllib.request
import json

url = "http://localhost:8000/api/planning/policy"

def test_case(name, profile, capabilities):
    payload = {
        "profile": profile,
        "capabilities": {"capabilities": capabilities}
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method="POST")
    req.add_header('Content-Type', 'application/json')
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read().decode('utf-8'))
        status = "PASS" if data["policy_passed"] else "REJECT"
        print(f"{name}: {status}")
        if data["violations"]:
            print(f"Violations: {data['violations']}")
    except Exception as e:
        print(f"{name}: ERROR {e}")

valid_profile = {
    "columns": ["id", "revenue", "date"],
    "row_count": 100,
    "data_types": {"id": "int", "revenue": "float", "date": "str"},
    "missing_values": {}, "unique_values": {}, "sample_values": {}
}

# Case 1: Missing revenue column
p1 = valid_profile.copy()
p1["columns"] = ["id", "date"]
test_case("Case 1 (Missing revenue)", p1, ["strategic_planning"])

# Case 2: Unknown capability
test_case("Case 2 (Unknown capability)", valid_profile, ["unknown_cap"])

# Case 3: Dataset too large
p3 = valid_profile.copy()
p3["row_count"] = 1000000000
test_case("Case 3 (Dataset too large)", p3, ["strategic_planning"])

# Case 4: Valid dataset
test_case("Case 4 (Valid dataset)", valid_profile, ["strategic_planning"])
