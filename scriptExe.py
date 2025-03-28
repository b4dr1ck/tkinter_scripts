#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os

def load_scripts_from_file(file_path):
    """Load shell script paths from a file."""
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        messagebox.showwarning("Warning", f"Failed to load {scripts_file_path}\nCreate an empty one...")
        open(file_path, "w").close()
        return []

def save_script_to_file(file_path, script_path):
    """Save a script path to the file if it doesn't already exist."""
    try:
        with open(file_path, "a+") as file:
            file.seek(0)
            existing_scripts = [line.strip() for line in file if line.strip()]
            if script_path not in existing_scripts:
                file.write(script_path + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save script: {e}")

def on_combobox_select(event):
    """Set the script_entry value when a combobox item is selected."""
    selected_script = script_combobox.get()
    script_entry.delete(0, tk.END)
    script_entry.insert(0, selected_script)

def browse_script():
    """Open a file dialog to select a shell script."""
    script_path = filedialog.askopenfilename(filetypes=[("Shell Scripts", "*.sh"), ("All Files", "*.*")])
    if script_path:
        script_entry.delete(0, tk.END)
        script_entry.insert(0, script_path)

def execute_script():
    """Execute the selected shell script with parameters."""
    script_path = script_entry.get()
    params = params_entry.get()
    if not script_path:
        messagebox.showerror("Error", "Please select or enter a valid script path.")
        return

    if not os.path.exists(script_path):
        messagebox.showerror("Error", "The script path does not exist.")
        return
        
    # Save the script to the file if the checkbox is selected
    if save_checkbox_var.get():
        save_script_to_file(scripts_file_path, script_path)
        # Reload the combobox with the updated list
        scripts_list = load_scripts_from_file(scripts_file_path)
        script_combobox["values"] = scripts_list

    try:
        # Execute the shell script with parameters and capture the output
        command = ["/bin/bash", script_path] + params.split()
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_text.delete(1.0, tk.END)  # Clear previous output
        output_text.insert(tk.END, f"{result.stdout}\n")
        if result.stderr:
            output_text.insert(tk.END, f"Errors:\n{result.stderr}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to execute script: {e}")

# Create the main window
root = tk.Tk()
root.title("Shell Script Executor")

# Configure rows and columns to expand
root.grid_rowconfigure(6, weight=1)  # Make the output frame row expandable
root.grid_columnconfigure(1, weight=1)  # Make the middle column (entries and text) expandable

# Load shell scripts from a file
scripts_file_path = f"{os.getenv('HOME')}/scriptsExe.sav"  # Replace with the path to your file
scripts_list = load_scripts_from_file(scripts_file_path)

desc="""
This is a simple GUI application that allows you to execute shell scripts with parameters.

You can select a script from the available list or enter a custom path to execute.
The output of the script execution is displayed in the text area below.
Save the script to the list by checking the checkbox.
"""

# Create and place widgets
tk.Label(root, text="Shell Script Executor", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
tk.Label(root, text=desc).grid(row=1, column=0, columnspan=4)

tk.Label(root, text="Available Scripts:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
script_combobox = ttk.Combobox(root, values=scripts_list, state="readonly", width=47)
script_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
script_combobox.bind("<<ComboboxSelected>>", on_combobox_select)

tk.Label(root, text="Script Path:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
script_entry = tk.Entry(root, width=50)
script_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

browse_button = tk.Button(root, text="...", command=browse_script)
browse_button.grid(row=3, column=2, padx=10, pady=10)

tk.Label(root, text="Script Parameter:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
params_entry = tk.Entry(root, width=50)
params_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

# Add a checkbox to save the script to the file
save_checkbox_var = tk.BooleanVar()
save_checkbox = tk.Checkbutton(root, text="Save script to list", variable=save_checkbox_var)
save_checkbox.grid(row=5, column=0, columnspan=3, pady=5)

execute_button = tk.Button(root, text="Execute", command=execute_script)
execute_button.grid(row=6, column=0, columnspan=3, pady=10)

# Add a frame for the Text widget and scrollbar
output_frame = tk.Frame(root)
output_frame.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Add a Text widget with a vertical scrollbar
output_text = tk.Text(output_frame, bg="black", fg="white", wrap="word")
output_scrollbar = tk.Scrollbar(output_frame, orient="vertical", command=output_text.yview)
output_text.configure(yscrollcommand=output_scrollbar.set)
output_text.insert(tk.END,"Output:\n")
output_text.pack(side="left", fill="both", expand=True)
output_scrollbar.pack(side="right", fill="y")

# Run the application
root.mainloop()