#!/usr/bin/python3

import sshCaller
from tkinter import *
from tkinter import messagebox, filedialog
import os
import threading
from tkinter import ttk
import re


inventory_file=f"{os.getenv('HOME')}/bin/inventory.toml"

# Function to save the output to a file
def save_output():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Ausgabe Speichern als"
    )
    if file_path:
        try:
            with open(file_path, "w") as file:
                file.write(output_text.get(1.0, END))  
            messagebox.showinfo("Success", f"Ausgabe gespeichert in: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Fehler beim Speichern:\n{e}")

# Function to filter the Listbox based on the search query
def search_hosts(*args):
    search_query = search_var.get().lower()  
    host_listbox.delete(0, END) 
    for item in get_hostnames(inventory_file):  
        if re.search(search_query,item.lower()): 
            host_listbox.insert(END, item)  

# Function to browse for a shell script
def browse_script():
    file_path = filedialog.askopenfilename(filetypes=[("Shell Scripts", "*.sh"), ("All Files", "*.*")])
    if file_path:
        command_entry.delete(0, END)  
        command_entry.insert(0, file_path) 

# Function to browse for an inventory file
def browse_inventory():
    global inventory_file
    inventory_file = filedialog.askopenfilename(filetypes=[("TOML Files", "*.toml"), ("All Files", "*.*")])
    if inventory_file:
        host_listbox.delete(0, END)
        for item in get_hostnames(inventory_file):
            host_listbox.insert(END, item)
        

# get hostnames from the inventory file
def get_hostnames(file):
    items = []
    try:
        fh = open(file,"r")
        for line in fh:
            if "servers" in line:
                items.append(line.strip().replace("[servers.","").replace("]",""))
        return items
    except Exception as e:
        messagebox.showerror("Error", f"Fehler beim Lesen des Inventory-Fle:\n {e}")
    
# Execute the remotecommander.rb script and capture the output
def exe_remotecommander():
    def run_ssh_calls():
        try:
            command = command_entry.get()
            host = host_entry.get()
                    
            host_list = sshCaller.parse_inventory(inventory_file, host)
            
            # Validate inputs
            if not host:
                messagebox.showerror("Error", "Host angeben!")
                return
            if not command:
                messagebox.showerror("Error", "Befehl oder Skript angeben!")
                return
            if not host_list and use_inv.get():
                messagebox.showerror("Error", f"Host {host} nicht in {inventory_file} gefunden!")
                return
            
            output_text.delete(1.0, END)
            
            # Configure tags for different colors
            output_text.tag_configure("host_info", foreground="yellow")
            output_text.tag_configure("result_info", foreground="white")
            output_text.tag_configure("error", foreground="red")
            
            progress_bar["maximum"] = len(host_list)
            progress_bar["value"] = 0
            progress_bar.grid(row=6, column=0, sticky="ew", pady=5)  
            
            load_profile_cmd=""
            
            if load_profile.get():
                load_profile_cmd = f". ~/.profile &&"
                                
            if not use_inv.get():
                username = username_entry.get()
                if not username:
                    messagebox.showerror("Error", "Benutzername angeben!")
                    return

                host_list = {"custom": {"host": host, "user": username}}
                
            # Loop through the hosts and execute the command
            for group in host_list:
                host = host_list[group]["host"]
                username = host_list[group]["user"]
                      
                if os.path.exists(command):
                    command = sshCaller.script_as_command(command)
                                    
                result = sshCaller.ssh_call(host, f"{load_profile_cmd} {command}", username)
                
                output_text.insert(END, f"{username}@{host}\n", "host_info")
                
                # Check for errors in the result to set color to error
                if (
                    "Authentication failed" in result  or 
                    "SSH error" in result or 
                    "An error occurred:" in result or 
                    "Error executing SSH command" in result
                    ):
                    output_text.insert(END, f"{result}\n\n", "error")
                else:
                    output_text.insert(END, f"{result}\n\n", "result_info")
                
                progress_bar["value"] += 1  
                root.update_idletasks()  
                
        except Exception as e:
            messagebox.showerror("Error", f"Fehler beim Ausführen des Scripts:\n{e}")
            print(e)
        finally:
            progress_bar.grid_remove()  

    # Run the SSH calls in a separate thread
    threading.Thread(target=run_ssh_calls, daemon=True).start()

# Function to handle double-click event
def on_host_double_click(event):
    # Get the selected item
    selected_index = host_listbox.curselection()
    if selected_index:
        selected_host = host_listbox.get(selected_index)
        host_entry.delete(0, END)
        host_entry.insert(0, selected_host)
        
# Function to toggle the username and host_listbox field based on use_inv      
def toggle_username_field():
    if use_inv.get():
        username_entry.config(state="disabled")  
        host_listbox.config(state="normal")  
    else:
        username_entry.config(state="normal")  
        host_listbox.config(state="disabled")  
        
        
# Create the main window
root = Tk()
root.title("SSH-Caller")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(3, weight=1)

# header
header_label = Label(root, text="SSH-Caller",font=("Arial", 16, "bold"),borderwidth=2, relief="groove")
header_label.grid(row=0, column=0,columnspan=2,pady=10)

# Host-list label
available_hosts_label = Label(root, text="Verfügbare Hosts (inventory.toml):")
available_hosts_label.grid(row=1, column=0)

# Search Frame
search_frame = Frame(root)
search_frame.grid_columnconfigure(1, weight=1)  
search_frame.grid_columnconfigure(2, weight=1) 
search_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
search_label = Label(search_frame, text="Suche:", anchor="w")
search_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
search_var = StringVar()  
search_var.trace_add("write", search_hosts)  
search_entry = Entry(search_frame, textvariable=search_var)
search_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

options_btn_frame=Frame(search_frame)
options_btn_frame.grid(row=0, padx=5,pady=5,column=2,sticky="w")
browse_inv_button = Button(options_btn_frame, text="Neues Inventory laden", command=browse_inventory)
browse_inv_button.grid(row=0, column=0)
use_inv = BooleanVar(value=True)
inv_chkbtn = Checkbutton(options_btn_frame, text="Inventory benutzen", variable=use_inv,command=toggle_username_field)
inv_chkbtn.grid(row=0, column=1)

# Hostlist Frame
hostlist_frame = Frame(root)
hostlist_frame.grid(row=3, column=0, padx=5,pady=5, sticky="nsew")
hostlist_frame.grid_columnconfigure(0, weight=1)
hostlist_frame.grid_rowconfigure(0, weight=1)
host_listbox = Listbox(hostlist_frame)
host_listbox.bind("<Double-1>", on_host_double_click)
host_listbox.grid(row=1, column=0, sticky="nsew")
hostlist_scroll = Scrollbar(hostlist_frame, orient=VERTICAL, command=host_listbox.yview)
hostlist_scroll.grid(row=1, column=1, sticky="ns")
host_listbox.config(yscrollcommand=hostlist_scroll.set)
host_listbox.delete(0, END)
for item in get_hostnames(inventory_file):
    host_listbox.insert(END, item)

# Parameter Frame (Host, Command)  
param_frame = Frame(root)
param_frame.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")
param_frame.grid_columnconfigure(1, weight=1) 
param_frame.grid_columnconfigure(2, weight=1)  
username_label = Label(param_frame, text="Benutzername?", anchor="w")
username_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
username_entry = Entry(param_frame, state="disabled")
username_entry.grid(row=0, column=1,columnspan=2, padx=10, pady=5, sticky="ew")  
host_label = Label(param_frame, text="Host?", anchor="w")
host_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
host_entry = Entry(param_frame, width=40)
host_entry.grid(row=1, column=1,columnspan=2, padx=10, pady=5, sticky="ew")  
command_label = Label(param_frame, text="Command oder Shell-Script?", anchor="w")
command_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
command_entry = Entry(param_frame, width=40)
command_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="ew") 
browse_button = Button(param_frame, text="Durchsuchen", command=browse_script)
browse_button.grid(row=2, column=3, padx=10, pady=5)

# Buttons Frame
button_frame = Frame(root)
button_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="w")  
exe_btn = Button(button_frame, text="Ausführen", command=exe_remotecommander)
exe_btn.grid(row=0, column=0, padx=5, pady=5)
save_btn = Button(button_frame, text="Ausgabe Speichern", command=save_output)
save_btn.grid(row=0, column=1, padx=5, pady=5)
load_profile = BooleanVar(value=False)
profile_chkbtn = Checkbutton(button_frame, text="Profile sourcen", variable=load_profile)
profile_chkbtn.grid(row=0, column=2, padx=5, pady=5)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")

# Output Frame
output_frame = Frame(root)
output_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
output_text = Text(output_frame, bg="black", fg="white", wrap="word")
output_scroll = Scrollbar(output_frame, orient="vertical", command=output_text.yview)
output_text.configure(yscrollcommand=output_scroll.set)
output_text.pack(side="left", fill="both", expand=True)
output_scroll.pack(side="right", fill="y")

root.mainloop()