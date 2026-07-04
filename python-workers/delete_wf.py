import psycopg2
conn = psycopg2.connect('postgresql://acb_user:acb_pass@localhost:5432/acb_db')
cur = conn.cursor()
cur.execute("DELETE FROM execution_entity WHERE \"workflowId\" = '1030c44d-a323-42'")
cur.execute("DELETE FROM workflow_entity WHERE id = '1030c44d-a323-42'")
conn.commit()
