import psycopg2
import json

conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute('SELECT CAST("data" AS TEXT) FROM execution_entity WHERE id = 199;')
row = cur.fetchone()
if row:
    print(row[0])
