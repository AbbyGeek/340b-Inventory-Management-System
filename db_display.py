import tkinter as tk
from tkinter import ttk
from inventorydb import AddMed, OpenDb, CloseDb
from jsonquery import UpcToNdc, DatabaseLookup, MedFormatting

def fetch_data():
    cursor = OpenDb()
    cursor.execute("SELECT ndc_code, generic_name, brand_name, manufacturer, package_info, dosage_form, route, pharm_class, quantity FROM medications")
    rows = cursor.fetchall()
    # CloseDb()
    return rows

def UpdateTable(table):
    """Update inventory table with fresh data from database"""
    for row in table.get_children():
        table.delete(row)
    rows = fetch_data()
    for row in rows:
        table.insert("","end",values=row)

def process_upc(entry, table):
    """Process the UPC input, look up medication, add it to the database"""
    upc_code = entry.get().strip()
    if not upc_code:
        return #Ignore empty inputs
    ndc_code = UpcToNdc(upc_code)
    search_item = DatabaseLookup(ndc_code)
    if search_item:
        med_dict = MedFormatting(search_item, ndc_code)
        AddMed(med_dict) #Add med to database
        UpdateTable(table) #Refresh Table
        entry.delete(0, tk.END) #Clear input field

# GUI setup
def GUISetup():
    """Set up the GUI for inventory display and UPC input"""
    root = tk.Tk()
    root.title("Inventory Viewer")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    cols = ["NDC Code", "Generic Name", "Brand Name", "Manufacturer", "Package Info", "Dosage Form", "Route", "Pharmacy Class", "Quantity"]
    table = ttk.Treeview(frame, columns=tuple(range(len(cols))), show="headings")

    for i, col in enumerate(cols):
        table.heading(i, text=col)
        table.column(i, width=150)
    table.pack()

    #UPC input field
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Enter UPC Code:").pack(side=tk.LEFT)
    upc_entry = tk.Entry(input_frame)
    upc_entry.pack(side=tk.LEFT, padx=5)

    submit_button = tk.Button(input_frame, text="Add Medication", command=lambda: process_upc(upc_entry, table))
    upc_entry.bind("<Return>", lambda event: process_upc(upc_entry, table))
    submit_button.pack(side=tk.LEFT)

    #Initial load
    UpdateTable(table)
    root.mainloop()