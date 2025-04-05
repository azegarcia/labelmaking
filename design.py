import customtkinter
from CTkListbox import *
from CTkScrollableDropdown import *
from dropdownContents import data_list
from CTkMessagebox import CTkMessagebox
from tkinter import messagebox
from datetime import datetime
import win32print
import win32ui
import tkinter as tk

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)
    
def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)
    
# Function to handle the word selection from dropdown
def update_word_display():
    item_word = item_entry.get()  # Get the selected word from the dropdown
    qty_word = qty_entry.get()
    sku_word = sku_entry.get()
    if not qty_word.isdigit():
        messagebox.showerror("Error", f"Quantity number contains a word")
    elif not sku_word.isdigit():
        messagebox.showerror("Error", f"SKU # contains a word")
    elif item_word == "":
        messagebox.showerror("Error", f"Item description is missing")
    else:
        app.counter += 1
        date_today = datetime.today().strftime('%Y-%m-%d')
        custom_qty = "QTY: " + qty_word
        custom_text = "SKU#:" + sku_word + "                                                                                          " + str(app.counter) + "     " + date_today
        first_row.configure(text=item_word, justify="left", font=("Arial", 24))
        second_row.configure(text=custom_qty, justify="left", font=("Arial", 24))
        res = messagebox.askquestion('Note',  
                         'Do you want to proceed to print?') 
        if res == 'yes' : 
            third_row.configure(text=custom_text, font=("Arial", 10))
            print_word(first_row, second_row, third_row)
        else : 
            messagebox.showinfo('Return', 'Returning to edit')
            
            
# Function to trigger printing
def print_word(first_row, second_row, third_row):
    if first_row:
        try:
            # Open the default printer
            printer_name = win32print.GetDefaultPrinter()
            printer_info = win32print.OpenPrinter(printer_name)
            devmode = win32print.GetPrinter(printer_info, 2)  # Get the printer's settings
            font_data = {'name':'Arial', 'height':60}
            font_data2 = {'name':'Arial', 'height':30}
            
            hdc = win32ui.CreateDC()
            font = win32ui.CreateFont(font_data)
            font2 = win32ui.CreateFont(font_data2)
            hdc.CreatePrinterDC(printer_name)
            hdc.StartDoc("Tkinter Print Job")
            hdc.StartPage()

            # Define coordinates to print the text on the page (start at the top-left corner)
            x, y = 100, 100
            
            hdc.SelectObject(font)
            # Print the content of the Text widget, breaking into multiple lines if necessary
            hdc.TextOut(x, y, first_row.cget("text"))  # Print one line at a time
            y += 130  # Move to the next line (adjust as needed)
            hdc.TextOut(x, y, second_row.cget("text"))  # Print one line at a time
            y += 130  # Move to the next line (adjust as needed)
            hdc.SelectObject(font2)
            hdc.TextOut(x, y, third_row.cget("text"))  # Print one line at a time

            hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()
            
            messagebox.showinfo("Printing", f"Content has been sent to the printer.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print: {str(e)}")
    else:
        messagebox.showwarning("No Content", "Please fill in the textbox first.")

def check_key(event: bool) -> bool:
   if (value := event.widget.get()) =='':
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
# ================================================================================================================================


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
customtkinter.CTkToplevel = None

# configure window
app.title("Biondi Label Making App")
app.geometry(f"{1200}x{700}")

# configure grid layout (4x4)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure((0, 1, 2), weight=1)

# this removes the maximize button
app.resizable(0,0)

# Set counter
app.counter = 0

# create sidebar frame with widgets (left)
sidebar_frame = customtkinter.CTkFrame(app, width=250)
sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
sidebar_frame.grid_rowconfigure(8, weight=1)

drop_label = customtkinter.CTkLabel(sidebar_frame, text="Item Description", font=customtkinter.CTkFont(size=18, weight="bold"))
drop_label.grid(row=0, column=0, padx=20, pady=(20, 10))
item_entry = tk.Entry(sidebar_frame, width=40) 
item_listbox = tk.Listbox(sidebar_frame, width=40, height=3)
item_entry.grid(row=1, column=0, padx=20)
item_listbox.grid(row=2, column=0, padx=20)
item_entry.bind('<KeyRelease>', check_key)
item_listbox.bind('<<ListboxSelect>>', items_selected)

qty_label = customtkinter.CTkLabel(sidebar_frame, text="Quantity", font=customtkinter.CTkFont(size=18, weight="bold"))
qty_label.grid(row=4, column=0, padx=20, pady=(20, 10))
qty_entry = customtkinter.CTkEntry(sidebar_frame, width=250) 
qty_entry.grid(row=5, column=0, padx=20, pady=10)

sku_label = customtkinter.CTkLabel(sidebar_frame, text="SKU #", font=customtkinter.CTkFont(size=18, weight="bold"))
sku_label.grid(row=6, column=0, padx=20, pady=(20, 10))
sku_entry = customtkinter.CTkEntry(sidebar_frame, width=250) 
sku_entry.grid(row=7, column=0, padx=20, pady=10)

update_button = customtkinter.CTkButton(sidebar_frame, text="Check/Print", command=update_word_display)
update_button.grid(row=8, column=0, padx=20, pady=20)

appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=9, column=0, padx=20, pady=(20, 0))
appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"],
                                                                command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=10, column=0, padx=20, pady=(20, 20))

# create sidebar frame with widgets (right)
r_sidebar_frame = customtkinter.CTkFrame(app, fg_color="white", width=70, height=50)
r_sidebar_frame.grid(row=0, column=1, rowspan=8)

first_row = customtkinter.CTkLabel(r_sidebar_frame, text="Item Description", font=customtkinter.CTkFont(size=22, weight="bold"))
first_row.grid(row=3, column=1, padx=20, pady=(20, 10), sticky="w")
second_row = customtkinter.CTkLabel(r_sidebar_frame, text="QTY:", font=customtkinter.CTkFont(size=22, weight="bold"))
second_row.grid(row=4, column=1, padx=20, pady=(20, 10), sticky="w")
third_row = customtkinter.CTkLabel(r_sidebar_frame, text="SKU#: Print No.     Date Printed", font=customtkinter.CTkFont(size=14, weight="bold"))
third_row.grid(row=5, column=1, padx=20, pady=(20, 10), sticky="w")


# ========================================================================
app.mainloop()