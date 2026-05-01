import tkinter as tk
import math

# ---------------- GLOBALS ---------------- #
expression = ""
history = []
dark_mode = True

# ---------------- FUNCTIONS ---------------- #

def press(value):
    global expression
    expression += str(value)
    equation.set(expression)

def clear():
    global expression
    expression = ""
    equation.set("")

def evaluate():
    global expression
    try:
        expr = expression.replace('√', 'math.sqrt')
        expr = expr.replace('sin', 'math.sin')
        expr = expr.replace('cos', 'math.cos')
        expr = expr.replace('tan', 'math.tan')
        expr = expr.replace('log', 'math.log10')

        result = str(eval(expr))
        history.append(expression + " = " + result)

        equation.set(result)
        expression = result
        update_history()
    except:
        equation.set("Error")
        expression = ""

def update_history():
    history_box.delete(0, tk.END)
    for item in history[-10:]:
        history_box.insert(tk.END, item)

# ---------------- KEYBOARD SUPPORT ---------------- #

def key_input(event):
    key = event.char

    if key in "0123456789+-*/().":
        press(key)
    elif key == "\r":  # Enter
        evaluate()
    elif key == "\x08":  # Backspace
        backspace()

def backspace():
    global expression
    expression = expression[:-1]
    equation.set(expression)

# ---------------- THEME ---------------- #

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    if dark_mode:
        bg = "#222"
        fg = "white"
        btn = "#333"
    else:
        bg = "#f0f0f0"
        fg = "black"
        btn = "#ddd"

    root.config(bg=bg)
    entry.config(bg=bg, fg=fg)

    for b in buttons_list:
        b.config(bg=btn, fg=fg)

    history_box.config(bg=bg, fg=fg)

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Scientific Calculator 🔥")
root.geometry("400x600")

equation = tk.StringVar()

# Entry
entry = tk.Entry(root, textvariable=equation, font=("Arial", 20), justify="right")
entry.pack(fill="both", padx=10, pady=10, ipady=10)

# Button Frame
frame = tk.Frame(root)
frame.pack()

buttons = [
    ['7','8','9','/'],
    ['4','5','6','*'],
    ['1','2','3','-'],
    ['0','.','=','+']
]

buttons_list = []

for row in buttons:
    f = tk.Frame(frame)
    f.pack(expand=True, fill='both')
    for btn in row:
        if btn == "=":
            action = evaluate
        else:
            action = lambda x=btn: press(x)

        b = tk.Button(f, text=btn, font=("Arial", 14),
                      command=action, height=2, width=5)
        b.pack(side="left", expand=True, fill="both")
        buttons_list.append(b)

# Scientific Buttons
sci_frame = tk.Frame(root)
sci_frame.pack()

sci_buttons = ["sin(", "cos(", "tan(", "√(", "log("]

for btn in sci_buttons:
    b = tk.Button(sci_frame, text=btn, font=("Arial", 12),
                  command=lambda x=btn: press(x))
    b.pack(side="left", expand=True, fill="both")
    buttons_list.append(b)

# Control Buttons
control_frame = tk.Frame(root)
control_frame.pack(fill="both")

tk.Button(control_frame, text="C", command=clear, bg="red", fg="white").pack(side="left", expand=True, fill="both")
tk.Button(control_frame, text="⌫", command=backspace).pack(side="left", expand=True, fill="both")
tk.Button(control_frame, text="🌙 Toggle Theme", command=toggle_theme).pack(side="left", expand=True, fill="both")

# History Panel
tk.Label(root, text="History").pack()
history_box = tk.Listbox(root, height=10)
history_box.pack(fill="both", padx=10, pady=10)

# Keyboard binding
root.bind("<Key>", key_input)

# Default theme
toggle_theme()

root.mainloop()