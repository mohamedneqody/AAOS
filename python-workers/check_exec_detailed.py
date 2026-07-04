import psycopg2
conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute('SELECT w.name, e.status, e."startedAt", e."stoppedAt" FROM execution_entity e JOIN workflow_entity w ON e."workflowId" = w.id ORDER BY e."startedAt" DESC LIMIT 5;')
for row in cur.fetchall():
    print(row)
