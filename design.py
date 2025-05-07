import customtkinter
from CTkListbox import *
from CTkScrollableDropdown import *
from dropdownContents import data_list
from tkinter import messagebox
from datetime import datetime
import win32print
import win32ui
import win32gui
import tkinter as tk
import pandas as pd
from tkinter import ttk
import numpy as np
import json

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)
    
def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

def check_key(event: bool) -> bool:
    value = event.widget.get()
    if value == '':
        data = data_list
    else:
        data = [item for item in data_list if value.lower() in item.lower()]
                                    
    update(data)

def update(data: str) -> None:  
    item_listbox.delete(0, 'end')

    for item in data:
        item_listbox.insert('end', item)

def items_selected(event: None) -> None:
    selected_langs = ",".join([item_listbox.get(i) for i in item_listbox.curselection()])
    item_entry.delete(0, tk.END)
    item_entry.insert(0, selected_langs)

def on_tree_click(event):
    # Identify which row and column were clicked
    item_id = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    
    if item_id and column == '#5':  # 5th column is "Delete"
        print(f"Deleting item: {tree.item(item_id)['values']}")
        tree.delete(item_id)

def quantity_input(event=None):
    # Get selected row
    item_id = tree.focus()
    column = '#2'  # Fixed to second column
    
    if item_id and column == '#2':
        x, y, width, height = tree.bbox(item_id, column)
        
        # Get current value
        cell_value = tree.set(item_id, column)
        
        # Create Entry widget
        entry = tk.Entry(app)
        entry.place(x=700, y=y + tree.winfo_y(), width=width, height=height)
        entry.insert(0, cell_value)
        entry.focus()

        def save_edit(event=None):
            new_value = entry.get()
            tree.set(item_id, column, new_value)
            entry.destroy()
            move_to_next_row()  # After saving, move to next

        entry.bind("<Tab>", save_edit)      # Save on Tab
        # entry.bind("<Return>", save_edit)  # Save on Enter
        entry.bind("<FocusOut>", lambda e: entry.destroy())  # Destroy if focus is lost 

def move_to_next_row():
    children = tree.get_children()
    current_item = tree.focus()
    
    if current_item in children:
        idx = children.index(current_item)
        next_idx = idx + 1
        if next_idx < len(children):
            next_item = children[next_idx]
            tree.selection_set(next_item)
            tree.focus(next_item)
            quantity_input()  # Start editing next row
        else:
            # No more rows
            pass
        
def add_row_from_listbox(event):
    # Get the selected item from the Listbox
    selected_item = item_listbox.get(item_listbox.curselection())
    
    # Load the JSON file
    with open('items.json', 'r') as f:
        data = json.load(f)

    for d in data:
        if selected_item == d['ITEM DESCRIPTION']:
            row_number = len(tree.get_children()) + 1
            tree.insert("", "end", values=(row_number, "", d["ITEM DESCRIPTION"], str(d["Id"]).replace(".0", ""), "DELETE"))


def delete_all():
    for row in tree.get_children():
        tree.delete(row)
    
# Function to handle the word selection from dropdown
def update_word_display():
    # Iterate over all rows and get their values
    for item_id in tree.get_children():
        # Get the data of the current row
        row_data = tree.item(item_id)["values"]
        if row_data[1] == "":
            messagebox.showerror("Error", f"Quantity is empty.")
        else:
            app.counter += 1
            date_today = datetime.today().strftime('%Y-%m-%d')
            custom_item = " " + row_data[2] + "\n"
            custom_qty = " QTY: " + str(row_data[1]) + "\n"
            custom_text = " SKU#:" + str(row_data[3]) + "    " + str(app.counter) + "    " + date_today
            first_row = custom_item
            second_row = custom_qty
            third_row = custom_text
            print_word(first_row, second_row, third_row)
    
# Function to trigger printing
def print_word(first_row, second_row, third_row):
    if first_row:
        if len(first_row) > 25:
            f_row = first_row
            first_row = f_row[:25]
            added_row = " " + f_row[25:]
        else:
            first_row = first_row
            added_row = ""
        try:
            # Open the default printer
            printer_name = win32print.GetDefaultPrinter()
            printer_info = win32print.OpenPrinter(printer_name)
            properties = win32print.GetPrinter(printer_info, 2)  # Get the printer's settings
            pDevModeObj = properties["pDevMode"]
            pDevModeObj.Orientation = 2
            
            # label size 70mm x 50mm
            pDevModeObj.PaperLength = 5
            pDevModeObj.PaperWidth = 7

            font_data = {'name':'Arial', 'height':50}
            font_data2 = {'name':'Arial', 'height':30}
            
            wdc = win32gui.CreateDC("Gprinter GP-1324D", printer_name, pDevModeObj)
            font = win32ui.CreateFont(font_data)
            font2 = win32ui.CreateFont(font_data2)
            hdc = win32ui.CreateDCFromHandle(wdc)
            hdc.CreatePrinterDC(printer_name)
            hdc.StartDoc("Tkinter Print Job")
            hdc.StartPage()

            # Define coordinates to print the text on the page (start at the top-left corner no margin)
            x, y = 0, 0
            
            hdc.SelectObject(font)
            # Print the content of the Text widget, breaking into multiple lines if necessary
            hdc.TextOut(x, y, first_row)  # Print one line at a time
            y += 50  # Move to the next line (adjust as needed)
            hdc.TextOut(x, y, added_row)  # Print one line at a time
            y += 150  # Move to the next line (adjust as needed)
            hdc.TextOut(x, y, second_row)  # Print one line at a time
            y += 150  # Move to the next line (adjust as needed)
            hdc.SelectObject(font2)
            hdc.TextOut(x, y, third_row)  # Print one line at a time

            hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()
            
            print("Printing....", f"Content has been sent to the printer.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print: {str(e)}")
    else:
        messagebox.showwarning("No Content", "Please fill in the textbox first.")
    
# ================================================================================================================================

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()

# configure window
app.title("BIT Label Making App")

# Get screen width and height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Set window size
app.geometry(f"{screen_width}x{screen_height}+0+0")

# Set counter
app.counter = 0
app.count = 0

# Configure two columns: column 0 (left) and column 1 (right)
app.grid_columnconfigure(0, weight=4)  # 40%
app.grid_columnconfigure(1, weight=6)  # 60%
app.grid_rowconfigure(0, weight=1)     # Make row stretchable too

# create sidebar frame with widgets (left)
sidebar_frame = customtkinter.CTkFrame(app)
sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")

# Ensure the frame does not shrink to fit its content
sidebar_frame.grid_propagate(False)

biondi_label = customtkinter.CTkLabel(sidebar_frame, text="BIT Label Making App", font=customtkinter.CTkFont(size=30, weight="bold"))
biondi_label.grid(row=2, column=0, padx=20, pady=(20, 10))
drop_label = customtkinter.CTkLabel(sidebar_frame, text="Item Description", font=customtkinter.CTkFont(size=18, weight="bold"))
drop_label.grid(row=4, column=0, padx=20, pady=(20, 10))
item_entry = tk.Entry(sidebar_frame, width=80) 
item_listbox = tk.Listbox(sidebar_frame, width=80, height=32)
item_entry.grid(row=5, column=0, padx=80)
item_listbox.grid(row=6, column=0, padx=80)
item_entry.bind('<KeyRelease>', check_key)
item_listbox.bind('<<ListboxSelect>>', items_selected)

# Bind the click event to the function
item_listbox.bind("<Double-1>", add_row_from_listbox)

update_button = customtkinter.CTkButton(sidebar_frame, text="Print", command=update_word_display)
update_button.grid(row=13, column=0, padx=20, pady=20)

delete_button = customtkinter.CTkButton(sidebar_frame, text="Delete All", command=delete_all)
delete_button.grid(row=14, column=0, padx=20, pady=20)

appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=16, column=0, padx=20, pady=(20, 0))
appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"],
                                                                command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=17, column=0, padx=20, pady=(20, 20))

# ========================================================================
# create sidebar frame with widgets (right)
right_frame = customtkinter.CTkFrame(app)
right_frame.grid(row=0, column=1, rowspan=7, sticky="nsew")

# Create Treeview
columns = ("Item No.", "Quantity", "Item Description", "SKU#", "Action")
tree = ttk.Treeview(right_frame, columns=columns, show="headings")

# Define a style
style = ttk.Style(right_frame)
style.configure("Treeview", font=("Helvetica", 14), rowheight=40)           # <-- Table text
style.configure("Treeview.Heading", font=("Helvetica", 20, "bold")) # <-- Column headers

# Define headings
tree.heading("Item No.", text="Item No.")
tree.heading("Quantity", text="Quantity")
tree.heading("Item Description", text="Item Description")
tree.heading("SKU#", text="SKU#")
tree.heading("Action", text="Action")

# Set column widths (optional)
tree.column("Item No.", anchor="center", width=30)
tree.column("Quantity", anchor="center", width=50)
tree.column("Item Description", anchor="center", width=400)
tree.column("SKU#", anchor="center", width=50)
tree.column("Action", anchor="center", width=100)

# Pack the Treeview
tree.pack(fill="both", expand=True, padx=(0, 20), pady=(30, 100))     # <-- Top + Right + bottom margin

# Bind a click
tree.bind("<Button-1>", on_tree_click)

# Bind one click to create entry, Bind Enter and Tab key to start editing
tree.bind("<ButtonRelease-1>", quantity_input)
tree.bind("<Tab>", lambda event: quantity_input())
# tree.bind("<Return>", lambda event: quantity_input())

# ========================================================================
app.mainloop()
