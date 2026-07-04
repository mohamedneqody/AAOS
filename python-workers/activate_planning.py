import psycopg2

conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute('UPDATE workflow_entity SET "active" = true, "activeVersionId" = "versionId" WHERE name = \'ACB - 05_planning\';')
conn.commit()
print("Activated ACB - 05_planning")
