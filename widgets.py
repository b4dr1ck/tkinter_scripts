#!/usr/bin/python3

from tkinter import *
from tkinter import ttk, messagebox, filedialog

# Create the main window
root = Tk()
root.title("Tkinter Widgets Example")

def on_button_click(widget):
    top = Toplevel(root)
    top.geometry("400x300")
    top.title(f"{widget} Example")
    
    match widget:
        case "label":
            label = Label(top, text="This is a Label", font=("Arial", 14), borderwidth=2, relief="solid", bg="red", fg="white")
            label.pack(padx=10, pady=10)
        case "button":
            button = Button(top, text="Click Me", command=lambda: messagebox.showinfo("Button Clicked", "You clicked the button!", parent=top))
            button.pack(padx=10, pady=10)
        case "entry":
            entry_label = Label(top, text="Enter your name:")
            entry_label.pack()
            entry = Entry(top, width=30)
            entry.pack(pady=5, padx=10)
            def on_submit():
                name = entry.get()
                messagebox.showinfo("Name Entered", f"You entered: {name}", parent=top)
            submit = Button(top, text="Submit", command=on_submit)
            submit.pack(pady=10)
        case "text":
            text = Text(top, height=5, width=40, bg="beige")
            text.pack(pady=5, padx=10)
            text.insert(INSERT, "This is a Text widget example")
        case "checkbutton":
            check_var = BooleanVar()
            checkbutton = Checkbutton(top, text="Check me", variable=check_var)
            checkbutton.pack(pady=10)
            def on_check():
                checked = "checked" if check_var.get() else "unchecked"
                messagebox.showinfo("Checkbutton", f"Checkbutton is {checked}", parent=top)
            checkbutton.config(command=on_check)
        case "radiobutton":
            radio_var = StringVar(value="Option 1")
            Label(top, text="Choose an option:").pack()
            Radiobutton(top, text="Option 1", variable=radio_var, value="Option 1").pack()
            Radiobutton(top, text="Option 2", variable=radio_var, value="Option 2").pack()
            def on_radio():
                selected = radio_var.get()
                messagebox.showinfo("Radiobutton", f"You selected: {selected}", parent=top)
            Button(top, text="Submit", command=on_radio).pack(pady=10)
        case "listbox":
            listbox = Listbox(top, height=5)
            listbox.insert(1, "Item 1")
            listbox.insert(2, "Item 2")
            listbox.insert(3, "Item 3")
            listbox.pack(pady=10)
            def on_select():
                selected = listbox.get(listbox.curselection())
                messagebox.showinfo("Listbox", f"You selected: {selected}", parent=top)
            Button(top, text="Submit", command=on_select).pack(pady=10)
        case "combobox":
            Label(top, text="Choose from the dropdown:").pack()
            combo = ttk.Combobox(top, values=["Option 1", "Option 2", "Option 3"])
            combo.pack(pady=10)
            def on_select():
                selected = combo.get()
                messagebox.showinfo("Combobox", f"You selected: {selected}", parent=top)
            Button(top, text="Submit", command=on_select).pack(pady=10)
        case "scale":
            val = IntVar()
            Label(top, text="Adjust the scale:").pack()
            Scale(top, from_=0, to=100, orient=HORIZONTAL,variable = val).pack(pady=10)
            def on_scale():
                value = val.get()
                messagebox.showinfo("Scale", f"Scale value: {value}", parent=top)
            Button(top, text="Submit", command=on_scale).pack(pady=10)
        case "spinbox":
          Label(top, text="Choose a number:").pack()
          spinbox = Spinbox(top, from_=1, to=10)
          spinbox.pack(pady=10)
          def on_spinbox():
              value = spinbox.get()
              messagebox.showinfo("Spinbox", f"Spinbox value: {value}", parent=top)
          Button(top, text="Get Value", command=on_spinbox).pack(pady=10)
        case "progressbar":
            Label(top, text="Progress Bar:").pack()
            progress = ttk.Progressbar(top, orient=HORIZONTAL, length=200, mode="determinate")
            progress.pack(pady=10)
            progress["value"] = 50
            def add_progress():
                progress["value"] += 10
            Button(top, text="Add Progress", command=add_progress).pack(pady=10)
            def subs_progress():
                progress["value"] -= 10
            Button(top, text="Subtract Progress", command=subs_progress).pack(pady=10)
        case "canvas":
            Label(top, text="Canvas Example:").pack()
            canvas = Canvas(top, width=200, height=100, bg="lightgray")
            canvas.pack(pady=10)
            canvas.create_rectangle(50, 25, 150, 75, fill="blue")
            canvas.create_line(0, 0, 200, 100, fill="red", width=2)
        case "scrollbar":
            Label(top, text="Text with Scrollbar:").pack()
            scroll_frame = Frame(top)
            scroll_frame.pack(pady=10)
            scroll_text = Text(scroll_frame, height=5, width=40)
            for i in range(20):
                scroll_text.insert(INSERT, f"Line {i}\n")
            scroll_text.pack(side=LEFT)
            scrollbar = Scrollbar(scroll_frame, command=scroll_text.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            scroll_text.config(yscrollcommand=scrollbar.set)
        case "menubutton":
            Label(top, text="Menu Button Example:").pack()
            mb = Menubutton(top, text="Menu", relief=RAISED)
            mb.pack(pady=10)
            mb.menu = Menu(mb, tearoff=0)
            mb["menu"] = mb.menu
            mb.menu.add_command(label="Option 1", command=lambda: messagebox.showinfo("Option 1", "You selected Option 1", parent=top))
            mb.menu.add_command(label="Option 2", command=lambda: messagebox.showinfo("Option 2", "You selected Option 2", parent=top))
            mb.menu.add_command(label="Option 3", command=lambda: messagebox.showinfo("Option 3", "You selected Option 3", parent=top))
            mb.menu.add_separator()
            mb.menu.add_command(label="Exit", command=top.destroy)
            mb.pack()
        case "open and save":
          Label(top, text="Open and Save File Example:").pack()
          
          def open_file():
              file = filedialog.askopenfile(parent=top)
              if file:
                  content = file.read()
                  text.delete(1.0, END)
                  text.insert(1.0, content)
                  file.close()
          def save_file():
              file = filedialog.asksaveasfile(mode="w", defaultextension=".txt",parent=top)
              if file:
                  content = text.get(1.0, END)
                  file.write(content)
                  file.close()
                  
          text_frame = Frame(top)
          text_frame.pack()
          text = Text(text_frame, height=8, width=40)
          text.insert(INSERT, "Open a text-file to show it's content...")
          text.pack(side=LEFT)
          scrollbar = Scrollbar(text_frame, command=text.yview)
          scrollbar.pack(side=RIGHT, fill=Y)
          text.config(yscrollcommand=scrollbar.set)
          
          open_btn = Button(top, text="Open File", command=open_file)
          open_btn.pack(side=LEFT,padx=5,expand=True,fill=X)
          save_btn = Button(top, text="Save File", command=save_file)
          save_btn.pack(side=LEFT,padx=5,expand=True,fill=X)
        case "messagebox":
          Label(top, text="Messagebox Example:").pack()
          def show_info():
              messagebox.showinfo("Information", "This is an information message", parent=top)
          def show_warning():
              messagebox.showwarning("Warning", "This is a warning message", parent=top)
          def show_error():
              messagebox.showerror("Error", "This is an error message", parent=top)
          def ask_question(): 
              response = messagebox.askquestion("Question", "Do you like Python?", parent=top)
              messagebox.showinfo("Response", f"You answered: {response}", parent=top)
          def ask_okcancel(): 
              response = messagebox.askokcancel("Ok or Cancel", "Press OK to continue or Cancel to stop", parent=top)
              messagebox.showinfo("Response", f"You answered: {response}", parent=top)
          def ask_yesno():    
              response = messagebox.askyesno("Yes or No", "Press Yes or No", parent=top)
              messagebox.showinfo("Response", f"You answered: {response}", parent=top)
          def ask_retrycancel():
              response = messagebox.askretrycancel("Retry or Cancel", "Press Retry or Cancel", parent=top)
              messagebox.showinfo("Response", f"You answered: {response}", parent=top)
          info_btn = Button(top, text="Show Info", command=show_info)
          info_btn.pack(pady=5)
          warning_btn = Button(top, text="Show Warning", command=show_warning)
          warning_btn.pack(pady=5)
          error_btn = Button(top, text="Show Error", command=show_error)
          error_btn.pack(pady=5)
          question_btn = Button(top, text="Ask Question", command=ask_question)
          question_btn.pack(pady=5)
          okcancel_btn = Button(top, text="Ask Ok/Cancel", command=ask_okcancel)
          okcancel_btn.pack(pady=5)
          yesno_btn = Button(top, text="Ask Yes/No", command=ask_yesno)
          yesno_btn.pack(pady=5)
          retrycancel_btn = Button(top, text="Ask Retry/Cancel", command=ask_retrycancel)
          retrycancel_btn.pack(pady=5)
        case _:
            pass

# Header
head = Label(root, text="Tkinter Widgets Example", font=("Arial", 16))
head.pack()

# Description
desc = Label(root, text="Click a button to see the widget example")
desc.pack(pady=10)

# Buttons Frame
btns_frame = Frame(root)
btns_frame.pack(expand=True, fill=X)

widgets=["label","button", "entry", "text", "checkbutton", "radiobutton", "listbox",
        "combobox", "scale", "spinbox", "progressbar", "canvas", "scrollbar", 
        "menubutton", "open and save", "messagebox"]


# Place buttons in a grid layout
for n, widget in enumerate(widgets):
    btn = Button(btns_frame, text=widget.capitalize(), command=lambda w=widget: on_button_click(w))
    # Use grid to place buttons in rows and columns
    btn.grid(row=n // 5, column=n % 5, padx=5, pady=5, sticky="ew")

for col in range(5):  
    btns_frame.grid_columnconfigure(col, weight=1)
    
# Run the application
root.mainloop()