import duckdb
import os

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "autobi.duckdb")

def init_database():
    con = duckdb.connect(DB_PATH)
    
    # 1. Products table
    con.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id VARCHAR PRIMARY KEY,
        name VARCHAR,
        category VARCHAR,
        unit_cost DOUBLE,
        unit_price DOUBLE
    );
    """)
    
    # 2. Orders table
    con.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id VARCHAR PRIMARY KEY,
        order_date DATE,
        customer_id VARCHAR,
        customer_region VARCHAR,
        shipping_mode VARCHAR
    );
    """)
    
    # 3. Order Details
    con.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        item_id VARCHAR PRIMARY KEY,
        order_id VARCHAR,
        product_id VARCHAR,
        quantity INTEGER,
        discount DOUBLE,
        revenue DOUBLE,
        profit DOUBLE
    );
    """)
    
    # Check if empty, then populate seed data
    count = con.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count == 0:
        print("[*] Seeding sample data...")
        con.execute("""
        INSERT INTO products VALUES
            ('P001', 'Ergonomic Desk Chair', 'Furniture', 120.0, 220.0),
            ('P002', 'Standing Desk Converter', 'Furniture', 180.0, 310.0),
            ('P003', 'Wireless Mechanical Keyboard', 'Technology', 45.0, 95.0),
            ('P004', 'Ultra-Wide 34" Monitor', 'Technology', 260.0, 480.0),
            ('P005', 'Noise-Cancelling Headset', 'Technology', 80.0, 160.0),
            ('P006', 'High-Yield Toner Cartridge', 'Office Supplies', 25.0, 65.0),
            ('P007', 'Premium Gel Ink Pens (Pack 10)', 'Office Supplies', 4.0, 15.0);

        INSERT INTO orders VALUES
            ('ORD-101', '2026-07-15', 'CUST-01', 'West', 'Express'),
            ('ORD-102', '2026-08-03', 'CUST-02', 'South', 'Standard'),
            ('ORD-103', '2026-08-21', 'CUST-03', 'North', 'Express'),
            ('ORD-104', '2026-09-10', 'CUST-04', 'East', 'Standard'),
            ('ORD-105', '2026-09-28', 'CUST-05', 'West', 'Same Day'),
            ('ORD-106', '2026-10-05', 'CUST-01', 'West', 'Standard');

        INSERT INTO order_items VALUES
            ('ITM-01', 'ORD-101', 'P004', 2, 0.05, 912.0, 392.0),
            ('ITM-02', 'ORD-101', 'P003', 3, 0.00, 285.0, 150.0),
            ('ITM-03', 'ORD-102', 'P001', 5, 0.10, 990.0, 390.0),
            ('ITM-04', 'ORD-103', 'P005', 4, 0.00, 640.0, 320.0),
            ('ITM-05', 'ORD-104', 'P006', 10, 0.15, 552.5, 302.5),
            ('ITM-06', 'ORD-105', 'P002', 2, 0.00, 620.0, 260.0),
            ('ITM-07', 'ORD-106', 'P007', 20, 0.05, 285.0, 205.0);
        """)
        print(f"[+] Initialized '{DB_PATH}' with sample tables and rows.")
    else:
        print(f"[i] Database '{DB_PATH}' already initialized.")
    con.close()

if __name__ == "__main__":
    init_database()
