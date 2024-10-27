# main.py
import os
import shutil
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, Checkbutton, IntVar, Toplevel, StringVar
import subprocess
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


DEFAULT_LOCATION_FILE = Path.home() / "default_locations.json"

LICENSE_STATUS_FILE = Path.home() / ".license_status"

selected_folder = None
default_folder_1 = None
default_folder_2 = None
default_folder_3 = None
selected_extensions = []


def check_license_in_db(license_key):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute('SELECT is_active FROM licenses WHERE license_key = %s', (license_key,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result[0]  # Returns True if active, False otherwise
        else:
            return False  # License key not found
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
        return False
    
    def enter_license_key():
        global license_status
        
        def submit_license():
            key = license_entry.get().strip(
            if not key:
                messagebox.showwarning("Input Error", "Please enter a license key.")
            return
        if check_license_in_db(key):
            license_status.set("Active")
            messagebox.showinfo("License Activated", "Your license is now active.")
            # Save the license status locally
            with open(LICENSE_STATUS_FILE, 'w') as file:
                file.write('active')
            license_window.destroy()
        else:
            messagebox.showerror("Invalid License", "The license key is invalid or inactive.")
            license_window.destroy()

    license_window = Toplevel(root)
    license_window.title("Enter License Key")
    license_window.geometry("350x150")
    license_window.resizable(False, False)

    tk.Label(license_window, text="Enter License Key:", font=("Arial", 12)).pack(pady=10)
    license_entry = tk.Entry(license_window, width=30, font=("Arial", 12))
    license_entry.pack(pady=5)
    license_entry.focus()

    submit_button = tk.Button(license_window, text="Submit", command=submit_license, font=("Arial", 12))
    submit_button.pack(pady=10)

# Function to load default folder locations from a file
def load_default_locations():
    global default_folder_1, default_folder_2, default_folder_3
    if DEFAULT_LOCATIONS_FILE.exists():
        try:
            with open(DEFAULT_LOCATIONS_FILE, 'r') as file:
                data = json.load(file)
                default_folder_1_path = data.get("default_folder_1", None)
                default_folder_2_path = data.get("default_folder_2", None)
                default_folder_3_path = data.get("default_folder_3", None)

                if default_folder_1_path:
                    default_folder_1 = Path(default_folder_1_path)
                    default_folder_1_label.config(text=f"Default Folder 1: {default_folder_1}")
                    default_folder_1_label.pack(side=tk.LEFT)

                if default_folder_2_path:
                    default_folder_2 = Path(default_folder_2_path)
                    default_folder_2_label.config(text=f"Default Folder 2: {default_folder_2}")
                    default_folder_2_label.pack(side=tk.LEFT)

                if default_folder_3_path:
                    default_folder_3 = Path(default_folder_3_path)
                    default_folder_3_label.config(text=f"Default Folder 3: {default_folder_3}")
                    default_folder_3_label.pack(side=tk.LEFT)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to load default folder locations. The JSON is corrupted.")
            # Function to save default folder locations to a file
def save_default_locations():
    global default_folder_1, default_folder_2, default_folder_3
    data = {
        "default_folder_1": str(default_folder_1) if default_folder_1 else None,
        "default_folder_2": str(default_folder_2) if default_folder_2 else None,
        "default_folder_3": str(default_folder_3) if default_folder_3 else None
    }
    try:
        with open(DEFAULT_LOCATIONS_FILE, 'w') as file:
            json.dump(data, file)
        messagebox.showinfo("Saved", "Default folder locations have been saved.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save default locations: {e}")

# Function to move files with the selected extensions
def move_files_with_extensions(source_folder, extensions):
    try:
        if not source_folder or not source_folder.exists():
            messagebox.showerror("Folder Error", "The selected folder no longer exists.")
            return

        downloads_folder = Path.home() / "Downloads"
        files_moved_total = 0

        for ext in extensions:
            new_folder = downloads_folder / f"moved_files_{ext.strip('.')}"
            new_folder.mkdir(exist_ok=True)

            files_moved = 0
            for file in source_folder.glob(f"*.{ext.strip('.')}"):
                shutil.move(str(file), new_folder)
                files_moved += 1
                files_moved_total += 1

        if files_moved_total > 0:
            messagebox.showinfo("Success", f"Moved {files_moved_total} files with selected extensions to {downloads_folder}")
        else:
            messagebox.showinfo("No Files Found", "No files with the selected extensions were found in the selected folder.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to select a folder
def select_folder():
    global selected_folder
    selected_folder_path = filedialog.askdirectory(title="Select Folder")

    if selected_folder_path:
        selected_folder = Path(selected_folder_path)
        folder_label.config(text=f"Current Folder: {selected_folder}")
    else:
        messagebox.showwarning("Folder Error", "No folder selected!")

# Functions to select Default Folders
def select_default_folder_1():
    global default_folder_1
    selected_default_folder_path = filedialog.askdirectory(title="Select Default Folder 1")
    if selected_default_folder_path:
        default_folder_1 = Path(selected_default_folder_path)
        default_folder_1_label.config(text=f"Default Folder 1: {default_folder_1}")
        default_folder_1_label.pack(side=tk.LEFT)

def select_default_folder_2():
    global default_folder_2
    selected_default_folder_2_path = filedialog.askdirectory(title="Select Default Folder 2")

    if selected_default_folder_2_path:
        default_folder_2 = Path(selected_default_folder_2_path)
        default_folder_2_label.config(text=f"Default Folder 2: {default_folder_2}")
        default_folder_2_label.pack(side=tk.LEFT)

def select_default_folder_3():
    global default_folder_3
    selected_default_folder_3_path = filedialog.askdirectory(title="Select Default Folder 3")

    if selected_default_folder_3_path:
        default_folder_3 = Path(selected_default_folder_3_path)
        default_folder_3_label.config(text=f"Default Folder 3: {default_folder_3}")
        default_folder_3_label.pack(side=tk.LEFT)