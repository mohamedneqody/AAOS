import psycopg2, json
conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute('SELECT data FROM execution_data WHERE "executionId" = 124;')
res = cur.fetchone()
if res: print(json.dumps(res[0])[:2000])
else: print('No data')
