"""
File Name: pdf_generator.py
Author: Nathan Brown
Date Created: 05/19/2021
Python Version: 3.9.2
"""

import PyPDF2
import os
from os import path
from PIL import Image
from tkinter import *
from tkinter import filedialog


# GLOBAL VARIABLES
file_list = []
converted_list = []

home_dir = path.expanduser('~')
temp_dir = home_dir + '/pdf_temp/'

current_file_index = None
current_file_dir = None
current_file_title = None


# FUNCTIONS
def add_files():
    global file_list, home_dir

    files = filedialog.askopenfilenames(initialdir=home_dir, filetypes=[("Compatible Files", "*.gif *.jpeg *.png *.doc *.docx"),("All Files", "*.*")])
    
    if files:
        for file in files:
            file_title = path.basename(file)
            file_list.append(dict(title=file_title, file_dir=file))
            file_listbox.insert(END, file_title)
        

def delete_file():
    global file_list

    index = file_listbox.curselection()

    if index:
        file_list.pop(index[0])
        file_listbox.delete(index[0])
        file_listbox.selection_clear(0, END)
        file_listbox.activate(index[0])
        file_listbox.selection_set(index[0], last=None)


def clear_list():
    global file_list

    file_list.clear()
    file_listbox.delete(0, END)


def move_up():
    current_selection = file_listbox.curselection()

    if current_selection:
        index = current_selection[0]
        if index == 0:
            pass
        else:
            to_move = file_list[index]
            file_list.pop(index)
            file_list.insert(index-1, to_move)

            file_listbox.delete(0, END)
            for file in file_list:
                file_listbox.insert(END, file['title'])

            file_listbox.activate(index-1)
            file_listbox.selection_set(index-1, last=None)


def move_down():
    global file_list

    current_selection = file_listbox.curselection()

    if current_selection:
        index = current_selection[0]
        if index == len(file_list)-1:
            pass
        else:
            to_move = file_list[index]
            file_list.pop(index)
            file_list.insert(index+1, to_move)

            file_listbox.delete(0, END)
            for file in file_list:
                file_listbox.insert(END, file['title'])

            file_listbox.activate(index+1)
            file_listbox.selection_set(index+1, last=None)


def convert_to_pdf():
    global file_list, converted_list, temp_dir

    if len(file_list) > 0:
        if os.path.exists(temp_dir):
            pass
        else:
            os.mkdir(temp_dir)

        for file in file_list:
            file_name = path.basename(file)
            file_info = file_name.split('.')
            new_file_name = file_info[0]+'.pdf'
            converted_list.append(new_file_name)
            open_file = Image.open(file)
            open_file.save(temp_dir + new_file_name, "pdf")
            open_file.close()

    generate_pdf()


def generate_pdf():
    global converted_list, temp_dir

    if len(converted_list) > 0:
        merger = PyPDF2.PdfFileMerger()

        for file in converted_list:
            merger.append(temp_dir + file)

        merger.write('test.pdf')
        merger.close()

        for file in converted_list:
            os.remove(temp_dir + file)

    if not os.listdir(temp_dir):
        os.rmdir(temp_dir)



# APPLICATION GUI
root = Tk()
root.geometry('600x400')
root.title('PDF Generator')

# GUI frames
main_frame = Frame(root)
main_frame.pack(pady=10)

files_controls_frame = LabelFrame(main_frame, text='File Controls')
files_controls_frame.grid(row=0, column=0, padx=25)

files_list_frame = LabelFrame(main_frame, text='File List')
files_list_frame.grid(row=0, column=1, padx=25)

list_controls_frame = Frame(files_list_frame)
list_controls_frame.grid(row=0, column=1)

output_frame = LabelFrame(root, text='Output')
output_frame.pack(pady=10)

file_output_frame = Frame(output_frame, padx=10, pady=10)
file_output_frame.grid(row=0, column=0)


# Control buttons for the files_controls_frame
add_file_button = Button(files_controls_frame, text='Add File(s)', command=add_files)
add_file_button.pack(padx=10, pady=10)

delete_file_button = Button(files_controls_frame, text='Delete File', command=delete_file)
delete_file_button.pack(padx=10, pady=10)

clear_list_button = Button(files_controls_frame, text='Clear List', command=clear_list)
clear_list_button.pack(padx=10, pady=10)

# File listbox and list order controls for the files_list_frame
file_listbox = Listbox(files_list_frame, width=40)
file_listbox.grid(row=0, column=0, padx=10, pady=10)

list_control_up = Button(list_controls_frame, text='Up', command=move_up)
list_control_up.pack(padx=10, pady=10)

list_control_down = Button(list_controls_frame, text='Down', command=move_down)
list_control_down.pack(padx=10, pady=10)

# Label and entry box for file_name_frame
file_name_label = Label(file_output_frame, text='File Name: ')
file_name_label.grid(row=0, column=0)

new_file_name = StringVar()
file_name_entry = Entry(file_output_frame, textvariable=new_file_name)
file_name_entry.grid(row=0, column=1)

# Label, entry, and browse button for file_destination_frame
file_destination_label = Label(file_output_frame, text='Destination: ')
file_destination_label.grid(row=1, column=0)

new_file_destination = StringVar()
file_destination_entry = Entry(file_output_frame, textvariable=new_file_destination)
file_destination_entry.grid(row=1, column=1)

file_destination_browse = Button(file_output_frame, text='Browse')
file_destination_browse.grid(row=1, column=2)




root.mainloop()