import psycopg2, json
conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute('SELECT "data" FROM execution_data ORDER BY "executionId" DESC LIMIT 1;')
row = cur.fetchone()
if row:
    data = json.loads(row[0])
    print('Let me find the error message directly:')
    for idx, item in enumerate(data):
        if isinstance(item, dict) and 'message' in item:
            print(f'Index {idx}: {item["message"]}')
        if isinstance(item, str) and 'Access to the file' in item:
            print(f'Index {idx}: {item}')
        if isinstance(item, str) and 'error' in item.lower() and 'registry' in item.lower():
            print(f'Index {idx}: {item}')
