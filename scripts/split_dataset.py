import pandas as pd

print("=" * 50)
print("LOADING DATASET...")
print("=" * 50)

# Try different encodings automatically
encodings = ['latin1', 'ISO-8859-1', 'cp1252', 'utf-8']

df = None
for encoding in encodings:
    try:
        print(f"Trying encoding: {encoding}...")
        df = pd.read_csv('data/raw/original_dataset.csv', encoding=encoding)
        print(f"✅ Success with {encoding} encoding!")
        break
    except:
        print(f"❌ Failed with {encoding}, trying next...")
        continue

if df is None:
    print("ERROR: Could not read the file with any encoding")
    exit(1)

print(f"✅ Loaded {len(df)} rows")
print(f"✅ Loaded {len(df.columns)} columns")
print()

# ============================================
# Create orders.csv (ERP System)
# ============================================
print("Creating orders.csv...")

orders_cols = ['order_id', 'customer_id', 'customer_name', 'customer_segment', 
               'product_name', 'product_category', 'order_date', 'sales', 'profit']

# Only use columns that exist
existing_cols = [col for col in orders_cols if col in df.columns]
orders_df = df[existing_cols]
orders_df.to_csv('data/raw/orders.csv', index=False)

print(f"✅ orders.csv created with {len(orders_df)} rows")

# ============================================
# Create warehouse.csv (WMS System)
# ============================================
print("Creating warehouse.csv...")

warehouse_cols = ['product_name', 'product_category', 'department', 'product_price']

existing_cols = [col for col in warehouse_cols if col in df.columns]
warehouse_df = df[existing_cols].drop_duplicates(subset=['product_name'])
warehouse_df.to_csv('data/raw/warehouse.csv', index=False)

print(f"✅ warehouse.csv created with {len(warehouse_df)} unique products")

# ============================================
# Create shipping.csv (TMS System)
# ============================================
print("Creating shipping.csv...")

shipping_cols = ['order_id', 'shipping_mode', 'shipping_date', 
                 'scheduled_delivery_date', 'actual_delivery_date', 
                 'delivery_status', 'carrier_name']

existing_cols = [col for col in shipping_cols if col in df.columns]
shipping_df = df[existing_cols].drop_duplicates(subset=['order_id'])
shipping_df.to_csv('data/raw/shipping.csv', index=False)

print(f"✅ shipping.csv created with {len(shipping_df)} rows")

print()
print("=" * 50)
print("🎉 ALL DONE! 3 files created in data/raw/")
print("=" * 50)
print()
print("Files created:")
print("   1. data/raw/orders.csv")
print("   2. data/raw/warehouse.csv")
print("   3. data/raw/shipping.csv")