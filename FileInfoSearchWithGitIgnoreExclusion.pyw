#pip install tkinterdnd2
#tkinterdnd2, os, fnmatch, pathspec 

import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog, messagebox
import pathspec

# Function to filter files based on the exclusion patterns using pathspec
def filter_files(folder, patterns):
    matched_files = []
    matched_folders = set()
    total_size = 0

    # Create a pathspec object from the exclusion patterns
    spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns.strip().splitlines())

    for root, dirs, files in os.walk(folder):
        # Skip directories that match the exclusion patterns
        dirs[:] = [d for d in dirs if not spec.match_file(os.path.relpath(os.path.join(root, d), folder))]

        # Filter files based on exclusion patterns
        for file in files:
            file_path = os.path.join(root, file)
            if not spec.match_file(os.path.relpath(file_path, folder)):
                matched_files.append(file_path)
                matched_folders.add(root)
                total_size += os.path.getsize(file_path)

    return matched_files, matched_folders, total_size

# Function to process the dropped folder and calculate results
def process_folder(folder):
    exclusion_patterns = exclusion_text.get("1.0", tk.END)
    if not exclusion_patterns.strip():
        messagebox.showerror("Error", "Please provide exclusion patterns!")
        return

    matched_files, matched_folders, total_size = filter_files(folder, exclusion_patterns)

    # Display results
    file_count = len(matched_files)
    folder_count = len(matched_folders)
    total_size_mb = total_size / (1024 * 1024)

    results = f"Matched Files: {file_count}\n" \
              f"Matched Folders: {folder_count}\n" \
              f"Total Size: {total_size_mb:.2f} MB"

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, results)


# Function to handle the folder drop event
def on_drop_folder(event):
    folder_path = event.data.strip('{""}')  # Clean up the dropped path
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)
    process_folder(folder_path)


# Function to handle the exclusion file drop event
def on_drop_exclusion_file(event):
    file_path = event.data.strip('{""}')  # Clean up the dropped path
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        exclusion_text.delete("1.0", tk.END)
        exclusion_text.insert(tk.END, content)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read the file: {e}")


# Function to handle folder selection via button
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path)
        process_folder(folder_path)


# Set up the main window
root = TkinterDnD.Tk()
root.title("File Size Calculator")
root.geometry("600x450")

# Label for exclusion patterns
label = tk.Label(root, text="Enter exclusion patterns (one per line), or drop a file here:")
label.pack(pady=5)

# Text box for exclusion patterns
exclusion_text = tk.Text(root, height=5, width=80)
exclusion_text.pack(pady=5)

# Enable dropping files into the exclusion pattern text field
exclusion_text.drop_target_register(DND_FILES)
exclusion_text.dnd_bind('<<Drop>>', on_drop_exclusion_file)

# Label for drag-and-drop area
drag_drop_label = tk.Label(root, text="Drag and drop a folder below or use the button:")
drag_drop_label.pack(pady=5)

# Entry for folder path
folder_path_entry = tk.Entry(root, width=80)
folder_path_entry.pack(pady=5)

# Drag-and-drop area for folder
folder_path_entry.drop_target_register(DND_FILES)
folder_path_entry.dnd_bind('<<Drop>>', on_drop_folder)

# Button to manually select folder
select_button = tk.Button(root, text="Select Folder", command=select_folder)
select_button.pack(pady=5)

# Label for result area
result_label = tk.Label(root, text="Results:")
result_label.pack(pady=5)

# Text box for displaying the results
result_text = tk.Text(root, height=5, width=80, state='normal')
result_text.pack(pady=5)

# Start the GUI main loop
root.mainloop()
