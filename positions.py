#!/usr/bin/python3

from tkinter import *

root = Tk()
root.title("Grid Layout")

def position_it(positions_array,grid_conf={}):
    # Configure columns to expand proportionally
    max_columns = max(len(row) for row in positions_array)
    for col in range(max_columns):
        root.grid_columnconfigure(col, weight=1)

    # Place widgets in the grid
    for row_i, row in enumerate(positions_array):
        for col_i, widget in enumerate(row):
            # If it's the last widget in the row, set columnspan to fill the remaining space
            if col_i == len(row) - 1:
              widget.grid(row=row_i, column=col_i, columnspan=max_columns - col_i, **grid_conf)
            else:
              widget.grid(row=row_i, column=col_i, **grid_conf)

# Example
label1 = Label(root, text="Label 1",borderwidth=2,relief="solid")
label2 = Label(root, text="Label 2", borderwidth=2,relief="solid")
label3 = Label(root, text="Label 3",borderwidth=2,relief="solid")
label4 = Label(root, text="Label 4", borderwidth=2,relief="solid")
label5 = Label(root, text="Label 5",borderwidth=2,relief="groove")
label6 = Label(root, text="Label 6", borderwidth=2,relief="solid")
entry1 = Entry(root, text="Entry 1", width=30,borderwidth=2,relief="solid")
button1 = Button(root, text="Button 1", bg="orange",fg="black")
listbox1 = Listbox(root, selectmode=SINGLE, height=10, borderwidth=2, relief="solid")
listbox1.insert(1, "Python")
listbox1.insert(2, "Java")
listbox1.insert(3, "C++")
listbox1.insert(4, "Any other")

# Positions array
positions = [ [label1,label2],
              [label3],
              [label5,label6,entry1,label4],
              [button1],
              [listbox1],
            ]

# call the function to position the widgets
position_it(positions,{"sticky":"nsew", "padx":10, "pady":5})

root.mainloop()