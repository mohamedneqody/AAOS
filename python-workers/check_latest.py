import psycopg2
conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM execution_entity WHERE \"workflowId\" = '2d2d1910-dcb2-45'")
print(cur.fetchall())
