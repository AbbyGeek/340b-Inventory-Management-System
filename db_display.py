import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
from inventorydb import AddMed, OpenDb, RemoveMed, CloseDb
from jsonquery import UpcToNdc, DatabaseLookup, MedFormatting
import concurrent.futures

executor = concurrent.futures.ThreadPoolExecutor(max_workers=3) #Background worker thread
update_in_progress = False #global flag

def FetchDataAsync(callback):
    """Fetch data in a background thread to prevent UI freezing"""
    def db_task():
        import sqlite3
        conn = sqlite3.connect("inventory.db") #new connection to DB
        cursor = conn.cursor()
        cursor.execute("SELECT ndc_code, generic_name, brand_name, manufacturer, package_info, dosage_form, route, pharm_class, quantity FROM medications")
        rows = cursor.fetchall()
        conn.close() #close after fetching
        return rows
    future = executor.submit(db_task)
    future.add_done_callback(lambda fut: callback(fut.result()))

def UpdateTable(table):
    """Update inventory table with fresh data from database"""
    global update_in_progress
    if update_in_progress:
        return #skip update if another is in progress
    update_in_progress = True
    def UpdateUI(rows):
        global update_in_progress
        existing_items = {table.item(child)["values"][0]: child for child in table.get_children()} # get existing rows by NDC code
        for row in rows:
            ndc_code = row[0]
            quantity = row[8]
            tag = "low_stock" if quantity < 4 else ""
            if ndc_code in existing_items:
                    #update row if exists
                    item_id=existing_items[ndc_code]
                    table.item(item_id,values=row, tags=(tag,))
                    del existing_items[ndc_code] #Remove from existing_items to track processed rows
            else:
                table.insert("","end", values=row, tags=(tag,))
        #remove any rows that no longer exist in DB
        for item_id in existing_items.values():
            try:
                table.delete(item_id)
            except tk.TclError:
                pass #ignore if the item is already gone
        #configure tag colors
        table.tag_configure("low_stock",background="red", foreground="white")
        update_in_progress = False #unlock update
        
    #Schedule next update in 2 seconds to keep UI responsive
    FetchDataAsync(UpdateUI) #async fetch with callback
    table.after(2000, lambda: UpdateTable(table)) #refresh every 2 seconds

def process_upc(entry, table, mode):
    """Process the UPC input, look up medication, add it to the database"""
    upc_code = entry.get().strip()
    if not upc_code:
        return #Ignore empty inputs
    try:
        ndc_code = UpcToNdc(upc_code)
        if not ndc_code:
            messagebox.showwarning("UPC Not Found", "Invalid UPC Code or not found")
            entry.delete(0, tk.END) #Clear input field

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
            messagebox.showwarning("Medication Not Found", "No medication found for this UPC")
            entry.delete(0, tk.END) #Clear input field

    except Exception as e:
        messagebox.showerror("Error", f"Failed to process UPC: {e}")
        entry.delete(0, tk.END) #Clear input field

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

    tk.Label(input_frame, text="UPC Code:").pack(side=tk.LEFT)
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
        
    # submit_button = tk.Button(input_frame, text="Add Medication", command=lambda: process_upc(upc_entry, table, mode_var.get()))
    upc_entry.bind("<Return>", lambda event: process_upc(upc_entry, table, mode_var.get()))
    upc_entry.bind("<KeyRelease>", on_entry_change)
    # submit_button.pack(side=tk.LEFT)
    upc_entry.focus_set()

    #Initial load
    UpdateTable(table)
    root.mainloop()