import tkinter as tk
from tkinter import ttk
import sqlite3

def fetch_data():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medications")
    rows = cursor.fetchall()
    return rows

def update_table():
    for row in table.get_children():
        table.delete(row)
    rows = fetch_data()
    for row in rows:
        table.insert("","end",values=row)

# GUI setup
root = tk.Tk()
root.title("Inventory Viewer")

frame = tk.Frame(root)
frame.pack(pady=20)

cols = ["NDC Code", "Name", "Brand", "Manufacturer", "Package Info", "Active Ingredients", "Quantity"]
table = ttk.Treeview(frame, columns=tuple(range(len(cols))), show="headings")

for i, col in enumerate(["NDC Code", "Generic Name", "Brand Name", "Manufacturer", "Package Info", "Active Ingredients", "Quantity"]):
    table.heading(i, text=col)
    table.column(i, width=150)

for row in fetch_data():
    table.insert("", "end", values=row)

table.pack()

#add refresh button
refresh_button = tk.Button(root, text="Refresh Inventory", command=update_table)
refresh_button.pack(pady=10)

root.mainloop()