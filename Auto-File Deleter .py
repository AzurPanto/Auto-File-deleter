import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkbootstrap import Style
import os
from datetime import datetime, timedelta
import threading
import schedule

def close_window():
    root.destroy()

def open_folder_explorer():
    folder_path = filedialog.askdirectory()
    if folder_path:
        result_label.config(text=f"Selected folder: {folder_path}")
        selected_folder.set(folder_path)

def delete_folder():
    folder_path = selected_folder.get()
    frequency = delete_frequency.get()
    time_unit_text = time_unit.get()
    
    if folder_path:
        try:
            delete_datetime = datetime.now() + timedelta(**{time_unit_text: frequency})
            result_label.config(text=f"Contents of folder '{folder_path}' will be deleted every {frequency} {time_unit_text}. Next deletion on {delete_datetime}.")
            
            # Schedule the deletion of the folder contents
            scheduled_job = schedule.every(frequency).minutes.do(delete_folder_contents, folder_path)
        except FileNotFoundError:
            result_label.config(text=f"Folder '{folder_path}' not found.")
        except PermissionError:
            result_label.config(text=f"Permission denied to delete '{folder_path}'")

def delete_folder_contents(folder_path):
    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        result_label.config(text=f"Contents of folder '{folder_path}' have been deleted.")
    except FileNotFoundError:
        result_label.config(text=f"Folder '{folder_path}' not found.")
    except PermissionError:
        result_label.config(text=f"Permission denied to delete '{folder_path}'")

def stop_deletion():
    schedule.clear()
    result_label.config(text="Automatic deletion has been stopped.")

# Create the main window
root = tk.Tk()
root.title("Auto-File Deleter")
root.geometry("400x500+700+200")

# Initialize the ttkbootstrap style
style = Style(theme="vapor")#you can find more themes in the ttkbootstrap website

# Create a button to open the folder explorer
open_button = ttk.Button(root, text="Open Folder Explorer", command=open_folder_explorer)
open_button.pack(pady=10)

# Create a label to display the selected folder
selected_folder = tk.StringVar()
folder_label = ttk.Label(root, textvariable=selected_folder)
folder_label.pack()

# Create a Combobox for specifying the frequency and time unit
delete_frequency_label = ttk.Label(root, text="How often do you want to delete the folder contents?")
delete_frequency_label.pack()
delete_frequency = tk.IntVar()
delete_frequency_combobox = ttk.Combobox(root, textvariable=delete_frequency, values=[1, 7, 30, 365], state="readonly")
delete_frequency_combobox.pack()
delete_frequency_combobox.set(1)  # Default value

# Create a Combobox for specifying the time unit
time_unit_label = ttk.Label(root, text="Select time unit:")
time_unit_label.pack()
time_unit = tk.StringVar()
time_unit_combobox = ttk.Combobox(root, textvariable=time_unit, values=["minutes", "hours", "days", "weeks"], state="readonly")
time_unit_combobox.pack()
time_unit_combobox.set("minutes")  # Default value

# Create a button to schedule the deletion of the folder contents
delete_button = ttk.Button(root, text="Delete Folder Contents", command=delete_folder)
delete_button.pack(pady=10)

# Create a label to display the result
result_label = ttk.Label(root, text="You have not selected a folder!")
result_label.pack()

# Create a button to stop the automatic deletion
stop_button = ttk.Button(root, text="Stop The deletion process", command=stop_deletion)
stop_button.pack(pady=10)

# Create a button to close the window
close_button = tk.Button(root, text="Close", command=close_window)
close_button.pack()

# Start a separate thread for the scheduler
def run_scheduler():
    while True:
        schedule.run_pending()

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# Start the GUI main loop
root.mainloop()
