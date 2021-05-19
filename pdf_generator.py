"""
File Name: pdf_generator.py
Author: Nathan Brown
Date Created: 05/19/2021
Python Version: 3.9.2
"""

from os.path import basename
from pathlib import Path
from tkinter import *
from tkinter import filedialog


# GLOBAL VARIABLES
file_list = []
current_file_index = None
current_file_dir = None
current_file_title = None


# FUNCTIONS
def add_files():
    global file_list

    files = filedialog.askopenfilenames(initialdir=Path.home(), filetypes=[("Compatible Files", "*.gif *.jpeg *.png *.doc *.docx"),("All Files", "*.*")])
    
    for file in files:
        file_title = basename(file)
        file_list.append(dict(title=file_title, file_dir=file))
        file_listbox.insert(END, file_title)


# APPLICATION GUI
root = Tk()
root.geometry('600x400')
root.title('PDF Generator')

# GUI frames
main_frame = Frame(root)
main_frame.pack(pady=20)

files_controls_frame = LabelFrame(main_frame, text='File Controls')
files_controls_frame.grid(row=0, column=0, padx=25)

files_list_frame = LabelFrame(main_frame, text='File List')
files_list_frame.grid(row=0, column=1, padx=25)

# Control buttons for the files_controls_frame
add_file_button = Button(files_controls_frame, text='Add File(s)')
add_file_button.pack(pady=10)

delete_file_button = Button(files_controls_frame, text='Delete File')
delete_file_button.pack(pady=10)

clear_list_button = Button(files_controls_frame, text='Clear List')
clear_list_button.pack(pady=10)

# File listbox and list order controls for the files_list_frame
file_listbox = Listbox(files_list_frame, width=40)
file_listbox.grid(row=0, column=0, padx=10, pady=10)










root.mainloop()