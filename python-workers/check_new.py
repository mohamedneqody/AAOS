import psycopg2
conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM execution_entity WHERE \"workflowId\" = 'b71e7604-e41e-41'")
print(cur.fetchall())
