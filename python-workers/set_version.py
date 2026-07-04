import psycopg2
conn = psycopg2.connect('postgresql://acb_user:acb_pass@postgres:5432/acb_db')
cur = conn.cursor()
cur.execute('UPDATE workflow_entity SET "activeVersionId" = "versionId" WHERE name = \'ACB - 01_scheduler\';')
conn.commit()
print("Updated activeVersionId successfully")
