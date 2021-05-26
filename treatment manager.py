from tkinter import *
from tkinter import ttk
import csv
from datetime import datetime


####################################################################################################################

# Get timestamp
def get_time():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    dt_object: datetime = datetime.fromtimestamp(timestamp)
    timestr = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return str(timestr)


def add_to_file():
    keys = ['Timestamp', 'Patient name', 'Therapist name', 'ID number']
    with open('treatments.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writerow(
            {'Timestamp': get_time(), 'Patient name': patient_box.get(), 'Therapist name': therapist_box.get(),
             'ID number': id_box.get()})


# Add Record
def add_record():
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    global count
    if count % 2 == 0:
        my_tree.insert(parent='', index='end', iid=count, text="",
                       values=(get_time(), patient_box.get(), therapist_box.get(), id_box.get()), tags=('evenrow',))
    else:
        my_tree.insert(parent='', index='end', iid=count, text="",
                       values=(get_time(), patient_box.get(), therapist_box.get(), id_box.get()), tags=('oddrow',))

    count += 1

    add_to_file()

    # Clear the boxes
    timestamp_box.delete(0, END)
    patient_box.delete(0, END)
    therapist_box.delete(0, END)
    id_box.delete(0, END)


# Remove all records
def remove_all():
    for record in my_tree.get_children():
        my_tree.delete(record)


# Remove one selected
def remove_one():
    x = my_tree.selection()[0]
    my_tree.delete(x)


# Remove many selected
def remove_many():
    x = my_tree.selection()
    for record in x:
        my_tree.delete(record)


# Select Record
def select_record():
    global valueglobal
    # Clear entry boxes
    timestamp_box.config(state=NORMAL)
    timestamp_box.delete(0, END)
    patient_box.delete(0, END)
    therapist_box.delete(0, END)
    id_box.delete(0, END)

    # Grab record number
    selected = my_tree.focus()
    # Grab record values


    try:
        values = my_tree.item(selected, 'values')
        # output to entry boxes
        timestamp_box.insert(0, values[0])
        timestamp_box.config(state=DISABLED)
        patient_box.insert(0, values[1])
        therapist_box.insert(0, values[2])
        id_box.insert(0, values[3])
        valueglobal = values
    except:
        values = valueglobal
        # output to entry boxes
        timestamp_box.insert(0, values[0])
        timestamp_box.config(state=DISABLED)
        patient_box.insert(0, values[1])
        therapist_box.insert(0, values[2])
        id_box.insert(0, values[3])


# Save updated record
def update_record():
    # Grab record number
    selected = my_tree.focus()
    # Save new data
    my_tree.item(selected, text="", values=(get_time(), patient_box.get(), therapist_box.get(), id_box.get()))

    # Clear entry boxes
    timestamp_box.delete(0, END)
    patient_box.delete(0, END)
    therapist_box.delete(0, END)
    id_box.delete(0, END)


# Create Binding Click function
def clicker(e):
    select_record()


# Move Row up
def up():
    rows = my_tree.selection()
    for row in rows:
        my_tree.move(row, my_tree.parent(row), my_tree.index(row) - 1)


# Move Row Down
def down():
    rows = my_tree.selection()
    for row in reversed(rows):
        my_tree.move(row, my_tree.parent(row), my_tree.index(row) + 1)


# Get data from file
def get_data_from_file():
    with open("treatments.csv", newline="") as file:
        reader = csv.reader(file)
        r = 0
        for col in reader:
            c = 0
            for row in col:
                if r != 0:
                    tmp.append(row)
                c += 1
            if r != 0:
                data.append(tuple(tmp))
                tmp.clear()
            r += 1
    return data


def sorte_by_data(sortby):
    global count
    count = 0
    global data
    remove_all()
    data.clear()
    # for record in my_tree.get_children():
    #     my_tree.delete(record)
    # for record in my_tree.get_children():
    #     print((my_tree.item(record)['values']))
    data = get_data_from_file()
    if sortby == 0:
        if sorte_by_data.date_click:
            data = sorted(data, key=lambda row: datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'), reverse=True)
        else:
            data = sorted(data, key=lambda row: datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))
        sorte_by_data.date_click = not sorte_by_data.date_click

    elif sortby == 1 or sortby == 2 or sortby == 3:
        if sorte_by_data.date_click:
            data = sorted(data, key=lambda row: row[sortby], reverse=True)
        else:
            data = sorted(data, key=lambda row: row[sortby])
        sorte_by_data.date_click = not sorte_by_data.date_click

    for record in data:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text="",
                           values=(record[0], record[1], record[2], record[3]),
                           tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text="",
                           values=(record[0], record[1], record[2], record[3]),
                           tags=('oddrow',))
        count += 1

    # # Grab record number
    # selected = my_tree.focus()
    # print(selected)
    # # Grab record values
    # values = my_tree.item(selected, 'values')
    # print(values)


def update_record():
    # Grab record number
    selected = my_tree.focus()
    # Save new data
    my_tree.item(selected, text="", values=(get_time(), patient_box.get(), therapist_box.get(), id_box.get()))

    # Clear entry boxes
    timestamp_box.delete(0, END)
    patient_box.delete(0, END)
    therapist_box.delete(0, END)
    id_box.delete(0, END)


####################################################################################################################

tmp = []
data = []
global count
count = 0
sorte_by_data.date_click = True
valueglobal = ['','','','']
####################################################################################################################


root = Tk()
root.title('Treatment')
# root.iconbitmap('c:/gui/codemy.ico')
root.geometry("500x800")

# Add some style
style = ttk.Style()
# Pick a theme
style.theme_use("default")
# Configure our treeview colors

style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3",
                )
# Change selected color
style.map('Treeview',
          background=[('selected', 'blue')])

add_frame = Frame(root)
add_frame.pack(pady=20)

# Labels
nl1 = Label(add_frame, text="Timestamp")
nl1.grid(row=0, column=0)

nl = Label(add_frame, text="Patient name")
nl.grid(row=0, column=1)

il = Label(add_frame, text="Therapist name")
il.grid(row=0, column=2)

tl = Label(add_frame, text="ID")
tl.grid(row=0, column=3)

# Entry boxes
timestamp_box = Entry(add_frame)
timestamp_box.config(state=DISABLED)
timestamp_box.grid(row=1, column=0)

patient_box = Entry(add_frame)
patient_box.grid(row=1, column=1)

therapist_box = Entry(add_frame)
therapist_box.grid(row=1, column=2)

id_box = Entry(add_frame)
id_box.grid(row=1, column=3)

button_frame = Frame(root)
button_frame.pack(pady=10)

# Buttons
# Creat Edit button
update_button = Button(button_frame, text="Edit Record", command=update_record)
update_button.config(height=1, width=12)
update_button.grid(padx=15, row=2, column=0)

# Add new Record
add_record = Button(button_frame, text="Add Record", command=add_record)
add_record.config(height=1, width=12)
add_record.grid(padx=15, row=2, column=1)

# Remove One
remove_one = Button(button_frame, text="Start Treatment", command=remove_one)
remove_one.config(height=1, width=12)
remove_one.grid(padx=15, row=2, column=2)

# Remove Many Selected
open_but = Button(button_frame, text="open", command=lambda: sorte_by_data(5))
open_but.config(height=1, width=12)
open_but.grid(padx=15, row=2, column=3)

# Create Treeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=20)

# Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended",
                       height=20)  # height num of rows
# Pack to the screen
my_tree.pack()

# Configure the scrollbar
tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ('Timestamp', 'Patient name', 'Therapist name', 'ID number')

# Formate Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Timestamp", anchor=W, width=140)
my_tree.column("Patient name", anchor=CENTER, width=100)
my_tree.column("Therapist name", anchor=W, width=140)
my_tree.column("ID number", anchor=W, width=140)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Timestamp", text="Timestamp", anchor=W, command=lambda: sorte_by_data(0))
my_tree.heading("Patient name", text="Patient name", anchor=CENTER, command=lambda: sorte_by_data(1))
my_tree.heading("Therapist name", text="Therapist name", anchor=W, command=lambda: sorte_by_data(2))
my_tree.heading("ID number", text="ID number", anchor=W, command=lambda: sorte_by_data(3))

# Add Data
# Data from csv
data = get_data_from_file()

# Create striped row tags
my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")

sorte_by_data(5)

# Bindings
#my_tree.bind("<Double-1>", clicker)
my_tree.bind("<ButtonRelease-1>", clicker)

root.mainloop()
