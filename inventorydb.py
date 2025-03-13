import sqlite3

# connect/create the DB
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

#Drop the old table
cursor.execute("DROP TABLE IF EXISTS medications")

#create table for medications
cursor.execute('''
CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ndc_code TEXT UNIQUE,
    generic_name TEXT,
    brand_name TEXT,
    manufacturer TEXT,
    package_info TEXT,
    active_ingredients TEXT,
    quantity INTEGER DEFAULT 0
)
''')
conn.commit()
conn.close()
print("Database and table created successfully.")

def add_medication(ndc_code, generic_name, brand_name, manufacturer, package_info, active_ingredients, quantity):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO medications (ndc_code, generic_name, brand_name, manufacturer, package_info, active_ingredients, quantity)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(ndc_code) DO UPDATE SET quantity = quantity + ?
    ''', (ndc_code, generic_name, brand_name, manufacturer, package_info, active_ingredients, quantity, quantity))
    conn.commit()
    conn.close()

def get_inventory():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medications")
    rows = cursor.fetchall()
    conn.close()
    return rows

def dispense_medication(ndc_code, amount):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE medications
    SET quantity = quantity - ?
    WHERE ndc_code = ? AND quantity >= ?
    ''', (amount, ndc_code, amount))
    conn.commit()
    conn.close()