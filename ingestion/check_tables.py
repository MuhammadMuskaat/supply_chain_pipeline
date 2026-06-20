import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='supply_chain',
        user='admin',
        password='admin'
    )
    cur = conn.cursor()
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='raw' ORDER BY tablename;")
    tables = cur.fetchall()
    print('Tables in raw schema:')
    for table in tables:
        print(f'  ✅ {table[0]}')
    cur.close()
    conn.close()
except Exception as e:
    print(f'Error: {e}')