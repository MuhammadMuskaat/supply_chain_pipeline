import pandas as pd
import os

print("=" * 50)
print("SPLITTING DATASET")
print("=" * 50)

# Load original dataset
df = pd.read_csv('data/raw/original_dataset.csv', encoding='latin1')
print(f"✅ Loaded {len(df):,} rows")

# Create orders.csv
print("\n1. Creating orders.csv...")
orders_cols = ['Order Id', 'Customer Id', 'Customer Fname', 'Customer Segment',
               'Product Name', 'Category Name', 'order date (DateOrders)',
               'Sales', 'Order Profit Per Order']
orders = df[orders_cols]
orders.to_csv('data/raw/orders.csv', index=False)
print(f"   ✅ orders.csv: {len(orders):,} rows")

# Create warehouse.csv
print("\n2. Creating warehouse.csv...")
warehouse_cols = ['Product Name', 'Category Name', 'Department Name', 'Product Price']
warehouse = df[warehouse_cols].drop_duplicates(subset=['Product Name'])
warehouse.to_csv('data/raw/warehouse.csv', index=False)
print(f"   ✅ warehouse.csv: {len(warehouse):,} unique products")

# Create shipping.csv
print("\n3. Creating shipping.csv...")
shipping_cols = ['Order Id', 'Shipping Mode', 'shipping date (DateOrders)',
                 'Days for shipment (scheduled)', 'Delivery Status', 'Late_delivery_risk']
shipping = df[shipping_cols]
shipping.to_csv('data/raw/shipping.csv', index=False)
print(f"   ✅ shipping.csv: {len(shipping):,} rows")

# Verify file sizes
print("\n" + "=" * 50)
print("VERIFICATION")
print("=" * 50)

for file in ['orders.csv', 'warehouse.csv', 'shipping.csv']:
    size = os.path.getsize(f'data/raw/{file}')
    size_mb = size / (1024 * 1024)
    print(f"{file}: {size_mb:.2f} MB")

print("\n🎉 DONE! Now run: python ingestion/ingest_windows.py")