import tkinter as tk
from tkinter import messagebox
import random
import datetime

# ---------------- DATA ---------------- #

subjects = [
    "Government", "Aliens", "Scientists", "Local Man", "Celebrity",
    "Tech Company", "Politician", "Student", "Robot", "Influencer"
]

actions = [
    "discovers", "bans", "destroys", "creates", "reveals",
    "hides", "launches", "investigates", "controls", "predicts"
]

objects = [
    "new planet", "secret project", "AI system", "hidden treasure",
    "ancient mystery", "viral app", "time machine", "ghost city",
    "unknown virus", "parallel universe"
]

extras = [
    "overnight", "in secret", "by accident", "shocking everyone",
    "during experiment", "without warning", "for the first time",
    "in public", "with strange results", "under pressure"
]

tones = {
    "Normal": "",
    "Shocking": "BREAKING: ",
    "Funny": "😂 LOL: "
}

categories = {
    "Tech": ["AI system", "robot", "software", "app"],
    "Politics": ["government", "law", "election"],
    "Science": ["experiment", "space", "discovery"],
    "Funny": ["banana", "meme", "cat"]
}

history = []

# ---------------- LOGIC ---------------- #

def generate_headline():
    category = category_var.get()
    tone = tone_var.get()

    subject = random.choice(subjects)
    action = random.choice(actions)
    obj = random.choice(objects)
    extra = random.choice(extras)

    headline = f"{tones[tone]}{subject} {action} {obj} {extra}!"

    result_label.config(text=headline)
    history.append(headline)


def save_headline():
    headline = result_label.cget("text")
    
    if headline == "":
        messagebox.showwarning("Warning", "No headline to save!")
        return

    with open("headlines.txt", "a") as file:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{time}] {headline}\n")

    messagebox.showinfo("Saved", "Headline saved successfully!")


def show_history():
    if not history:
        messagebox.showinfo("History", "No headlines generated yet!")
        return

    history_text = "\n".join(history[-10:])
    messagebox.showinfo("Last 10 Headlines", history_text)


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Fake News Headline Generator 📰")
root.geometry("500x400")
root.config(bg="#1e1e1e")

# Title
title = tk.Label(root, text="Fake News Generator", font=("Arial", 18, "bold"), fg="white", bg="#1e1e1e")
title.pack(pady=10)

# Category Dropdown
category_var = tk.StringVar(value="Tech")
tk.Label(root, text="Select Category", fg="white", bg="#1e1e1e").pack()
tk.OptionMenu(root, category_var, *categories.keys()).pack(pady=5)

# Tone Dropdown
tone_var = tk.StringVar(value="Normal")
tk.Label(root, text="Select Tone", fg="white", bg="#1e1e1e").pack()
tk.OptionMenu(root, tone_var, *tones.keys()).pack(pady=5)

# Result
result_label = tk.Label(root, text="", wraplength=400, font=("Arial", 12), fg="yellow", bg="#1e1e1e")
result_label.pack(pady=20)

# Buttons
btn_generate = tk.Button(root, text="Generate Headline", command=generate_headline, bg="green", fg="white")
btn_generate.pack(pady=5)

btn_save = tk.Button(root, text="Save Headline", command=save_headline, bg="blue", fg="white")
btn_save.pack(pady=5)

btn_history = tk.Button(root, text="Show History", command=show_history, bg="purple", fg="white")
btn_history.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", command=root.quit, bg="red", fg="white")
btn_exit.pack(pady=10)

# Run app
root.mainloop()