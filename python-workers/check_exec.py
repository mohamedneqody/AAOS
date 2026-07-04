import psycopg2
conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute('SELECT COUNT(*), w.name FROM execution_entity e JOIN workflow_entity w ON e."workflowId" = w.id GROUP BY w.name;')
print(cur.fetchall())
