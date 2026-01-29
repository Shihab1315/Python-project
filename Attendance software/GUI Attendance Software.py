import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

STUDENT_FILE = "students.csv"
ATTENDANCE_FILE = "attendance.csv"

def add_student():
    roll = roll_entry.get()
    name = name_entry.get()

    if roll == "" or name == "":
        messagebox.showerror("Error", "All fields required")
        return

    with open(STUDENT_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([roll, name])

    messagebox.showinfo("Success", "Student Added")
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)

def mark_attendance():
    roll = roll_entry.get()
    today = datetime.now().strftime("%Y-%m-%d")

    with open(ATTENDANCE_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([roll, today, "Present"])

    messagebox.showinfo("Done", "Attendance Marked")

# GUI
root = tk.Tk()
root.title("Smart Attendance System")
root.geometry("400x300")

tk.Label(root, text="Smart Attendance System", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Roll").pack()
roll_entry = tk.Entry(root)
roll_entry.pack()

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Button(root, text="Add Student", width=20, command=add_student).pack(pady=5)
tk.Button(root, text="Mark Attendance", width=20, command=mark_attendance).pack(pady=5)

root.mainloop()
