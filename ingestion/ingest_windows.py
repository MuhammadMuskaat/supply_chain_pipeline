import psycopg2
import csv

print("=" * 50)
print("LOADING DATA INTO DATABASE")
print("=" * 50)

# Connect to database
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='supply_chain',
    user='admin',
    password='admin'
)
cur = conn.cursor()

# ============================================
# 1. LOAD ORDERS
# ============================================
print("\n1. Loading ORDERS (ERP system)...")

# Clear existing data
cur.execute("DELETE FROM raw.erp_orders;")
conn.commit()
print("   Cleared existing orders")

# Load data
count = 0
with open('data/raw/orders.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            cur.execute("""
                INSERT INTO raw.erp_orders 
                (order_id, customer_id, customer_name, customer_segment, 
                 product_name, product_category, order_date, sales, profit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['Order Id'],
                row['Customer Id'],
                row['Customer Fname'],
                row['Customer Segment'],
                row['Product Name'],
                row['Category Name'],
                row['order date (DateOrders)'],
                float(row['Sales']) if row['Sales'] else 0,
                float(row['Order Profit Per Order']) if row['Order Profit Per Order'] else 0
            ))
            count += 1
            if count % 10000 == 0:
                conn.commit()
                print(f"   Inserted {count:,} rows...")
        except Exception as e:
            print(f"   Error on row {count}: {e}")

conn.commit()
print(f"   ✅ Inserted {count:,} orders")

# ============================================
# 2. LOAD PRODUCTS
# ============================================
print("\n2. Loading PRODUCTS (WMS system)...")

cur.execute("DELETE FROM raw.wms_products;")
conn.commit()
print("   Cleared existing products")

count = 0
with open('data/raw/warehouse.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            cur.execute("""
                INSERT INTO raw.wms_products 
                (product_name, product_category, department, product_price)
                VALUES (%s, %s, %s, %s)
            """, (
                row['Product Name'],
                row['Category Name'],
                row['Department Name'],
                float(row['Product Price']) if row['Product Price'] else 0
            ))
            count += 1
        except Exception as e:
            print(f"   Error: {e}")

conn.commit()
print(f"   ✅ Inserted {count:,} products")

# ============================================
# 3. LOAD SHIPPING
# ============================================
print("\n3. Loading SHIPPING (TMS system)...")

cur.execute("DELETE FROM raw.tms_shipping;")
conn.commit()
print("   Cleared existing shipping")

count = 0
with open('data/raw/shipping.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            cur.execute("""
                INSERT INTO raw.tms_shipping 
                (order_id, shipping_mode, shipping_date, delivery_status, 
                 days_for_shipment, late_delivery_risk)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                row['Order Id'],
                row['Shipping Mode'],
                row['shipping date (DateOrders)'],
                row['Delivery Status'],
                int(row['Days for shipment (scheduled)']) if row['Days for shipment (scheduled)'] else 0,
                int(row['Late_delivery_risk']) if row['Late_delivery_risk'] else 0
            ))
            count += 1
            if count % 10000 == 0:
                conn.commit()
                print(f"   Inserted {count:,} rows...")
        except Exception as e:
            print(f"   Error: {e}")

conn.commit()
print(f"   ✅ Inserted {count:,} shipping records")

# ============================================
# 4. VERIFY
# ============================================
print("\n" + "=" * 50)
print("VERIFICATION")
print("=" * 50)

cur.execute("SELECT COUNT(*) FROM raw.erp_orders")
orders = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM raw.wms_products")
products = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM raw.tms_shipping")
shipping = cur.fetchone()[0]

print(f"raw.erp_orders:   {orders:,} rows")
print(f"raw.wms_products: {products:,} rows")
print(f"raw.tms_shipping: {shipping:,} rows")
print("=" * 50)

if orders > 0 and products > 0 and shipping > 0:
    print("🎉 ALL DATA LOADED SUCCESSFULLY!")
else:
    print("⚠️ Some tables are still empty")

cur.close()
conn.close()