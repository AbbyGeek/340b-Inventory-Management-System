import tkinter as tk
from tkinter import ttk, StringVar
from tkinter import *
from inventorydb import AddMed, OpenDb, RemoveMed, CloseDb
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

def process_upc(entry, table, mode):
    """Process the UPC input, look up medication, add it to the database"""
    upc_code = entry.get().strip()
    if not upc_code:
        return #Ignore empty inputs
    try:
        ndc_code = UpcToNdc(upc_code)
        if not ndc_code:
            print("Invalid UPC Code or not found.")
            return
        search_item = DatabaseLookup(ndc_code)
        if search_item:
            med_dict = MedFormatting(search_item, ndc_code)
            if mode == "add":
                AddMed(med_dict)
            elif mode == "remove":
                RemoveMed(med_dict)
            UpdateTable(table) #Refresh Table
            entry.delete(0, tk.END) #Clear input field
        else:
            print("No medication found for this UPC.")
    except Exception as e:
        print(f"Error processing UPC: {e}")

# GUI setup
def GUISetup():
    """Set up the GUI for inventory display and UPC input"""
    root = tk.Tk()
    root.title("Inventory Viewer")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    
    frame = tk.Frame(root)
    frame.pack(pady=20, fill="both", expand=True)

    cols = ["NDC Code", "Generic Name", "Brand Name", "Manufacturer", "Package Info", "Dosage Form", "Route", "Pharmacy Class", "Quantity"]
    table = ttk.Treeview(frame, columns=tuple(range(len(cols))), show="headings")

    col_width = screen_width // len(cols)
    for i, col in enumerate(cols):
        table.heading(i, text=col)
        table.column(i, width=col_width, anchor="center", stretch=True)
    table.pack()

    #UPC input field
    input_frame = tk.Frame(root)
    input_frame.pack(side='bottom', pady=10)

    tk.Label(input_frame, text="Enter UPC Code:").pack(side=tk.LEFT)
    upc_entry = tk.Entry(input_frame)
    upc_entry.pack(side=tk.LEFT, padx=5)

    mode_var = tk.StringVar(root, "add") #default to "Add"
    toggle_frame = tk.Frame(root)
    toggle_frame.pack(side = 'bottom', pady=10)

    add_button = tk.Radiobutton(toggle_frame, text="Add", variable=mode_var, value="add")
    remove_button = tk.Radiobutton(toggle_frame, text="Remove", variable=mode_var, value="remove")
    add_button.pack(side=tk.LEFT)
    remove_button.pack(side=tk.LEFT)
    mode_var.set("add")
    
    def on_entry_change(event):
        root.after(100, lambda: process_upc(upc_entry, table, mode_var.get()))
        
    submit_button = tk.Button(input_frame, text="Add Medication", command=lambda: process_upc(upc_entry, table, mode_var.get()))
    upc_entry.bind("<Return>", lambda event: process_upc(upc_entry, table, mode_var.get()))
    upc_entry.bind("<KeyRelease>", on_entry_change)
    submit_button.pack(side=tk.LEFT)
    upc_entry.focus_set()

    #Initial load
    UpdateTable(table)
    root.mainloop()