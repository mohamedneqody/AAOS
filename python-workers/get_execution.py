import psycopg2
conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute('SELECT "data" FROM execution_data ORDER BY "executionId" DESC LIMIT 1;')
row = cur.fetchone()
if row:
    print(row[0][:1000])
