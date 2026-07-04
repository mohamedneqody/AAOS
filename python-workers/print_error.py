import psycopg2, json
conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute('SELECT data FROM execution_data ORDER BY "executionId" DESC LIMIT 1;')
row = cur.fetchone()
if row:
    data = row[0]
    if isinstance(data, str):
        data = json.loads(data)
    with open('/app/latest_error.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("Saved to latest_error.json")
