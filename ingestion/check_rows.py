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
    
    print('=' * 50)
    print('📊 ROW COUNTS')
    print('=' * 50)
    
    # Check each table
    cur.execute("SELECT COUNT(*) FROM raw.erp_orders")
    erp_count = cur.fetchone()[0]
    print(f'raw.erp_orders:   {erp_count:,} rows')
    
    cur.execute("SELECT COUNT(*) FROM raw.wms_products")
    wms_count = cur.fetchone()[0]
    print(f'raw.wms_products: {wms_count:,} rows')
    
    cur.execute("SELECT COUNT(*) FROM raw.tms_shipping")
    tms_count = cur.fetchone()[0]
    print(f'raw.tms_shipping: {tms_count:,} rows')
    
    print('=' * 50)
    
    # Check if data exists
    if erp_count > 0 and wms_count > 0 and tms_count > 0:
        print('✅ All tables have data!')
    else:
        print('⚠️ Some tables are empty')
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f'Error: {e}')