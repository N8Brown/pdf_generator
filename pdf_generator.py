"""
File Name: pdf_generator.py
Version: 1.2.0
Author: Nathan Brown
Version Created: 06/16/2021
Application Created: 05/19/2021
Python Version: 3.9.2
"""
import PIL.Image
import PyPDF2
import os
import re
import shutil
from docx2pdf import convert
from fpdf import FPDF
from os import path
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox



# GLOBAL VARIABLES
file_list = []
converted_list = []
home_dir = path.expanduser('~')
temp_dir = home_dir + '/pdf_temp/'
output_dir = None


# FUNCTIONS
def add_files():
    global file_list, home_dir

    files = filedialog.askopenfilenames(initialdir=home_dir, filetypes=[("Compatible Files", "*.docx *.gif *.jpeg *.jpg *.pdf *.png *.txt"),("Image Files", "*.gif *.jpeg *.jpg *.png"),("Text Files", "*.docx *.pdf *.txt")])
    
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

        file_listbox.yview_moveto((index-1)/len(file_list))


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

        file_listbox.yview_moveto((index+1)/len(file_list))


def get_output_directory():
    global home_dir
    new_file_destination.set(filedialog.askdirectory(initialdir=home_dir))


def start_validation():
    global file_list
    if len(file_list) > 0:
        validate_file_name()
    else:
        messagebox.showwarning('PDF Generator', 'Please add at least one file to convert to PDF.')


def validate_file_name():
    if new_file_name.get():
        illegal_chars = re.compile('[*<>"?/\|:]')
        if illegal_chars.search(new_file_name.get()):
            messagebox.showerror('PDF Generator', 'File name cannot contain any of the following characters:\n\n | * " ? < > / \\ :\n\nPlease correct and try again.')
        else:
            validate_directory()
    else:
        messagebox.showwarning('PDF Generator', 'Please enter a valid file name.\n\nFile name cannot contain any of the following characters:\n\n | * " ? < > / \\ :\n ')


def validate_directory():
    if new_file_destination.get():
        convert_to_pdf()
    else:
        messagebox.showwarning('PDF Generator', 'Please choose an output desitination for the file.')

def convert_to_pdf():
    global file_list, converted_list, temp_dir

    if os.path.exists(temp_dir):
        pass
    else:
        os.mkdir(temp_dir)

    for file in file_list:
        file_name = file['title'].split('.')[0]
        file_type = file['title'].split('.')[1]
        new_file_name = file_name + '.pdf'
        converted_list.append(new_file_name)

        if file_type == 'txt':
            try:
                text = open(file['file_dir'], "r")
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                for line in text:
                    pdf.cell(200, 10, txt=line, ln=1, align='L')

                pdf.output(temp_dir + new_file_name)
            except:
                messagebox.showerror('PDF Generator', 
                'There was an error converting\n\n' + 
                file['title'] + '\n\n' +
                'This file will be skipped')

        elif file_type == 'docx':
            try:
                convert(file['file_dir'], temp_dir + new_file_name)
            except:
                messagebox.showerror('PDF Generator', 
                'There was an error converting\n\n' + file['title'] + '\n\n' + 'Please ensure that Word is installed and the file is not corrupt.\n\nThis file will be skipped.')

        elif file_type == 'pdf':
            shutil.copy(file['file_dir'], temp_dir + file['title'])

        else:
            open_file = PIL.Image.open(file['file_dir'])
            open_file.save(temp_dir + new_file_name, "pdf")
            open_file.close()

    generate_pdf()


def generate_pdf():
    global converted_list, temp_dir

    if len(converted_list) > 0:
        merger = PyPDF2.PdfFileMerger()

        for file in converted_list:
            merger.append(temp_dir + file)

        merger.write(new_file_destination.get() + "/" + new_file_name.get() + ".pdf")
        merger.close()

        for file in converted_list:
            os.remove(temp_dir + file)

    if not os.listdir(temp_dir):
        os.rmdir(temp_dir)

    messagebox.showinfo('PDF Generator', 'File "' + new_file_name.get() + '" was created successfully and saved to:\n\n' + new_file_destination.get())
    
    new_file_name.set('')
    new_file_destination.set('')
    

def about():
    messagebox.showinfo(
        'PDF Generator',
        'PDF GENERATOR\n\n'+
        'Version: 1.2.0\n'+
        'Release Date: 2021-06-16\n'+
        'Author: Nathan Brown\n\n'+
        'https://github.com/N8Brown/pdf_generator\n\n'+
        u'\u00A9' + ' 2021'
    )


# APPLICATION GUI
root = Tk()
root.geometry('630x480')
root.title('PDF Generator')
app_icon = PhotoImage(file='assets/logo.png')
root.iconphoto(False, app_icon)

# GUI Window Menus
main_menu = Menu(root)
root.config(menu=main_menu)

file_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Add File(s)', command=add_files)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.destroy)

help_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='About', command=about)

# GUI frames

main_frame_1 = Frame(root)
main_frame_1.pack(pady=20, anchor=W)

logo_frame = Frame(main_frame_1)
logo_frame.grid(row=0, column=0)

files_frame = LabelFrame(main_frame_1, text='Files to Convert')
files_frame.grid(row=0, column=1, sticky=NE)

logo = PhotoImage(file='assets/logo.png')
logo_label = Label(logo_frame, image=logo)
logo_label.pack(padx= [20, 20], pady=20)

files_controls_frame = Frame(files_frame)
files_controls_frame.grid(row=0, column=1, pady=[5,0], padx=10, sticky=NW)

files_list_frame = Frame(files_frame)
files_list_frame.grid(row=0, column=2)

list_components_frame = Frame(files_list_frame)
list_components_frame.grid(row=0, column=0, pady=[0, 10])

list_controls_frame = LabelFrame(files_list_frame, text='Move')
list_controls_frame.grid(row=0, column=1, padx=10)

output_frame = LabelFrame(root, text='Output')
output_frame.pack(padx=25, pady=10, anchor=W)

file_output_frame = Frame(output_frame, padx=10, pady=10)
file_output_frame.grid(row=0, column=0)

# Control buttons for the files_controls_frame
add_file_button = Button(files_controls_frame, text='Add File(s)', command=add_files, width=10)
add_file_button.pack(pady=5)

delete_file_button = Button(files_controls_frame, text='Delete File', command=delete_file, width=10)
delete_file_button.pack(pady=5)

clear_list_button = Button(files_controls_frame, text='Clear List', command=clear_list, width=10)
clear_list_button.pack(pady=5)

# File listbox and list order controls for the files_list_frame
file_listbox = Listbox(list_components_frame, width=45)
file_listbox.pack(pady=10, side=LEFT, fill=BOTH)

listbox_scrollbar = Scrollbar(list_components_frame)
listbox_scrollbar.pack(pady=10, side=RIGHT, fill=BOTH)

file_listbox.config(yscrollcommand=listbox_scrollbar.set)
listbox_scrollbar.config(command=file_listbox.yview)


up_arrow = PhotoImage(file='assets/arrow-up.png')
down_arrow = PhotoImage(file='assets/arrow-down.png')

list_control_up = Button(list_controls_frame,image=up_arrow, command=move_up)
list_control_up.pack(pady=10)

list_control_down = Button(list_controls_frame, image=down_arrow, command=move_down)
list_control_down.pack(pady=10)

# Label and entry box for file_name_frame
file_name_label = Label(file_output_frame, text='File Name: ')
file_name_label.grid(row=0, column=0, pady=5)

new_file_name = StringVar()
file_name_entry = Entry(file_output_frame, textvariable=new_file_name, width=81)
file_name_entry.grid(row=0, column=1, columnspan=2, pady=5)

# Label, entry, and browse button for file_destination_frame
file_destination_browse = Button(file_output_frame, text='Save To', command=get_output_directory)
file_destination_browse.grid(row=1, column=0, pady=5)

new_file_destination = StringVar()
file_destination_entry = Entry(file_output_frame, textvariable=new_file_destination, state=DISABLED, width=81)
file_destination_entry.grid(row=1, column=1, columnspan=2, pady=5)

generate_pdf_button = Button(file_output_frame, text='Generate PDF', command=start_validation)
generate_pdf_button.grid(row=2, column=2, pady=10, sticky=SE)





root.mainloop()