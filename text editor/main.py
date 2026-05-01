#import thinter for creating  GUI apps 
import tkinter as tk


from tkinter import filedialog,messagebox
root=tk.Tk()
root.title("Text Editor")
root.geometry("800x650")

text=tk.Text(
    root,
    wrap=tk.WORD,
    font=("Helvetica",12)
)
text.pack(expand=True, fill=tk.BOTH)
# main logic
#function 1-to create a new file
def new_file():
    text.delete(1.0,tk.END)

#function 2-to open a new file
def open_file():
    #open file diologe
    file_path=filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("text Files", "*.txt")]
    )

    if file_path:
        #open file
        with open(file_path,"r") as file:
            text.delete(1.0,tk.END)
            text.insert(tk.END,file.read())

#function 3-save the file
def save_file():
    file_path=filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files","*.txt")]
    )
    if file_path:
     with open(file_path,"w") as file:
        file.write(text.get(1.0,tk.END))
    messagebox.showinfo("Info", "File saved successfully")

# create menu bar

menu=tk.Menu(root)
root.config(menu=menu)

file_menu=tk.Menu(menu)

#new ,open,save, open files
#add filemenu for menu bar
menu.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New",command=new_file)
file_menu.add_command(label="open",command=open_file)
file_menu.add_command(label="Save",command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=root.quit)


root.mainloop()