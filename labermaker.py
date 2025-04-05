import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import Text
from dropdownContents import data_list
from datetime import datetime
import win32print
import win32ui
import customtkinter
    
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
        window.counter += 1
        date_today = datetime.today().strftime('%Y-%m-%d')
        custom_text = item_word + "\n\n\n QTY:" + qty_word + "\n\n\n" + "SKU#:" + sku_word + "\t\t      " + str(window.counter) + "     " + date_today
        word_label.config(text=custom_text)  # Update the label to display the word
        res = messagebox.askquestion('Note',  
                         'Do you want to proceed to print?') 
        if res == 'yes' : 
            print_word()
        else : 
            messagebox.showinfo('Return', 'Returning to edit')
            
            
# Function to trigger printing
def print_word():
    content = word_label.cget("text")  # Get the text of the label (the displayed word)
    if content:  # If there's content in the box, print it
        try:
            # Open the default printer
            printer_name = win32print.GetDefaultPrinter()
            printer_info = win32print.OpenPrinter(printer_name)
            devmode = win32print.GetPrinter(printer_info, 2)  # Get the printer's settings
            
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(printer_name)
            hdc.StartDoc("Tkinter Print Job")
            hdc.StartPage()

            # Define coordinates to print the text on the page (start at the top-left corner)
            x, y = 100, 100
            
            # Print the content of the Text widget, breaking into multiple lines if necessary
            for line in content.splitlines():
                hdc.TextOut(x, y, line)  # Print one line at a time
                y += 45  # Move to the next line (adjust as needed)

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

# Create the main window
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
window = customtkinter.CTk()
window.title("Biondi Label Making App")

# this removes the maximize button
window.resizable(0,0)

# Add logo
p1 = PhotoImage(file = 'labelmaker/logo.png')
window.iconphoto(False, p1)

# Adjust size 
window.geometry( "1400x780" )

# Set the window background
window.configure(bg="white")

# Set counter
window.counter = 0

# icons
check = PhotoImage(file='labelmaker/check.png')

# Resizing image to fit on button 
checkimage = check.subsample(8, 8)
        
# Part Labels
drop_label = tk.Label(window, text=" Item Description", font=("Helvetica", 16, "bold"), justify="left", bg='white')
qty_label = tk.Label(window, text="Quantity", font=("Helvetica", 16, "bold"), justify="left", bg='white')
sku_label = tk.Label(window, text="SKU #", font=("Helvetica", 16, "bold"), justify="left", bg='white')

# Paddings
x_button = tk.Button(window, text="", bg='white', fg='white', borderwidth=0)
b_button = tk.Button(window, text="B Button", bg='white', fg='white', borderwidth=0)
c_button = tk.Button(window, text="C Button", bg='white', fg='white', borderwidth=0)
x_button.grid(row=0, column=1, padx=10, pady=10)
b_button.grid(row=5, column=1, padx=10, pady=10)
c_button.grid(row=7, column=1, padx=10, pady=10)

# Configure grid to center the label
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)
window.columnconfigure(4, weight=1)
window.columnconfigure(5, weight=1)
window.columnconfigure(6, weight=1)
window.columnconfigure(7, weight=1)
window.columnconfigure(8, weight=1)

item_entry = tk.Entry(window, width=25) 
item_listbox = tk.Listbox(window, width=25, height=3)

# Text entries
qty_entry = tk.Entry(window, bd =5)
sku_entry = tk.Entry(window, bd =5)

# Create a button to update the word in the box when a selection is made
update_button = tk.Button(window, command=update_word_display, image=checkimage, text = 'Check', compound="left", 
                          font=("Helvetica", 12, "bold"))

# Create a label to display the edited word
word_label = tk.Label(window, text="", width=50, height=10, relief="solid", font=("Helvetica", 20), justify="left")

# Pattern
drop_label.grid(row=1, column=0)
qty_label.grid(row=1, column=2)
sku_label.grid(row=1, column=7)
item_entry.grid(row=2, column=0)
item_listbox.grid(row=3, column=0)
qty_entry.grid(row=2, column=2)
sku_entry.grid(row=2, column=7)
word_label.grid(row=4, column=2)
update_button.grid(row=6, column=2)

item_entry.bind('<KeyRelease>', check_key)
item_listbox.bind('<<ListboxSelect>>', items_selected)

update(data_list)

# Start the Tkinter event loop
window.mainloop()
