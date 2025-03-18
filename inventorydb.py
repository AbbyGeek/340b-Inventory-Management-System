import sqlite3
import tkinter as tk
from tkinter import simpledialog
conn = None


def AddMed(med_dict):
    """Insert medication data into the database, or update quantity if already exists."""
    cursor = OpenDb()
    #Check if med is already in db
    cursor.execute("SELECT quantity FROM medications WHERE ndc_code=?", (med_dict["ndc_code"],))
    result = cursor.fetchone()
    if result:
        #Medication exists, update quantity
        new_qty = result[0] + med_dict["quantity"]
        cursor.execute("UPDATE medications SET quantity = ? WHERE ndc_code = ?", (new_qty, med_dict["ndc_code"]))
    else:
        #Insert new medication quantity
        cursor.execute("""
            INSERT INTO medications (ndc_code, generic_name, brand_name, manufacturer, package_info, dosage_form, route, pharm_class, quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
              med_dict["ndc_code"],
              med_dict["generic_name"],
              med_dict["brand_name"],
              med_dict["manufacturer"],
              med_dict["package_info"],
              med_dict["dosage_form"],
              med_dict["route"],
              med_dict["pharm_class"],
              med_dict["quantity"]
            ))
    CloseDb()

#Simple Tkinter button to trigger scan
root = tk.Tk()
root.withdraw() #Hide main window

def CreateDb():
    cursor = OpenDb()
    #temp line to drop table if exists. REMOVE BEFORE PROD
    cursor.execute("DROP TABLE IF EXISTS medications")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ndc_code TEXT,
    generic_name TEXT,
    brand_name TEXT,
    manufacturer TEXT,
    package_info TEXT,
    dosage_form TEXT,
    route TEXT,
    pharm_class TEXT,
    quantity INTEGER DEFAULT 0
    )
    ''')

def OpenDb():
    global conn
    if conn is None:
        conn = sqlite3.connect("inventory.db")
        print("DB connection open")
    return conn.cursor()

def CloseDb():
    global conn
    if conn is not None:
        conn.commit()
        conn.close()
        conn = None
        print("DB connection closed")