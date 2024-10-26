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
                messagebox.showwarning(input error", "please enter License Key")
            )
