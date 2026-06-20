import psycopg2
import csv

print("=" * 50)
print("LOADING SHIPPING DATA (FIXED)")
print("=" * 50)

# Connect
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='supply_chain',
    user='admin',
    password='admin'
)
cur = conn.cursor()

# Clear shipping
cur.execute("DELETE FROM raw.tms_shipping;")
conn.commit()
print("✅ Cleared existing shipping")

# Load shipping
count = 0
with open('data/raw/shipping.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        shipping_date = row['shipping date (DateOrders)']
        days = int(row['Days for shipment (scheduled)']) if row['Days for shipment (scheduled)'] else 0
        late_risk = int(row['Late_delivery_risk']) if row['Late_delivery_risk'] else 0
        
        cur.execute("""
            INSERT INTO raw.tms_shipping 
            (order_id, shipping_mode, shipping_date, 
             scheduled_delivery_date, actual_delivery_date,
             delivery_status, carrier_name, late_delivery_risk)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Order Id'],
            row['Shipping Mode'],
            shipping_date,
            shipping_date,
            shipping_date,
            row['Delivery Status'],
            'Unknown',
            late_risk
        ))
        count += 1
        if count % 10000 == 0:
            conn.commit()
            print(f"   Inserted {count:,} rows...")

conn.commit()
print(f"✅ Inserted {count:,} shipping records")

# Verify
cur.execute("SELECT COUNT(*) FROM raw.tms_shipping")
final = cur.fetchone()[0]
print(f"✅ raw.tms_shipping now has {final:,} rows")

cur.close()
conn.close()