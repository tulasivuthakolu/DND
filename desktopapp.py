import time
import tkinter as tk
from tkinter import simpledialog, messagebox
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def block_websites(duration_minutes):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    redirect = "127.0.0.1"
    website_list = ["www.facebook.com", "facebook.com",
                    "www.instagram.com", "instagram.com"]
    
    def add_block():
        try:
            with open(hosts_path, 'r+') as file:
                content = file.read()
                for website in website_list:
                    if website not in content:
                        file.write(redirect + " " + website + "\n")
            print("Websites blocked.")
        except PermissionError:
            messagebox.showerror("Error", "Permission denied. Please run the script as an administrator.")
    
    def remove_block():
        try:
            with open(hosts_path, 'r+') as file:
                content = file.readlines()
                file.seek(0)
                file.truncate()
                for line in content:
                    if not any(website in line for website in website_list):
                        file.write(line)
            print("Websites unblocked.")
        except PermissionError:
            messagebox.showerror("Error", "Permission denied. Please run the script as an administrator.")
    
    def update_timer():
        nonlocal duration_minutes
        minutes, seconds = divmod(duration_minutes, 60)
        time_str = f"{minutes:02}:{seconds:02}"
        timer_label.config(text=f"Remaining Time: {time_str}")
        if duration_minutes > 0:
            duration_minutes -= 1
            root.after(1000, update_timer)
        else:
            remove_block()
            timer_label.config(text="Time's up! Websites unblocked.")
            messagebox.showinfo("Info", "Time's up! Websites unblocked.")
    
    add_block()
    update_timer()

def start_blocking():
    try:
        duration = simpledialog.askinteger("Input", "Enter duration in minutes:")
        if duration is not None:
            global duration_minutes
            duration_minutes = duration * 60  # Convert minutes to seconds
            block_websites(duration)
    except Exception as e:
        print(f"An error occurred: {e}")

if not is_admin():
    messagebox.showwarning("Warning", "Please run this script as an administrator for it to work properly.")
    exit()

# Tkinter setup
root = tk.Tk()
root.title("Do Not Disturb")
root.geometry("400x400")
root.resizable(False, False)

# Frame for the content
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

# Title label
title_label = tk.Label(frame, text="Do Not Disturb", font=("Helvetica", 18, "bold"))
title_label.pack(pady=10)

# Label to show remaining time
timer_label = tk.Label(frame, text="Remaining Time: 00:00", font=("Helvetica", 14))
timer_label.pack(pady=20)

# Button to start blocking
btn_block = tk.Button(frame, text="Start Blocking", command=start_blocking, font=("Helvetica", 12), bg="#4CAF50", fg="white")
btn_block.pack(pady=10)

# Run Tkinter main loop
root.mainloop()