import psycopg2
conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute('SELECT id, name, active, "versionId", "activeVersionId" FROM workflow_entity;')
for row in cur.fetchall():
    print(row)
