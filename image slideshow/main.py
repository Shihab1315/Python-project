import tkinter as tk
from PIL import Image, ImageTk

# Main application window
root = tk.Tk()
root.title("Photo Slideshow Album")
root.geometry("900x900")

# List of image paths (FIXED: added C:)
image_path = [
    r"C:\Users\HP\OneDrive\Pictures\Camera Roll\img1.jpg",
    r"C:\Users\HP\OneDrive\Pictures\Camera Roll\img2.png",
    r"C:\Users\HP\OneDrive\Pictures\Camera Roll\img3.jpeg",
    r"C:\Users\HP\OneDrive\Pictures\Camera Roll\img4.avif",
]

image_size = (700, 700)

# Load and resize images
images = []
for path in image_path:
    try:
        img = Image.open(path)
        img = img.resize(image_size)
        images.append(img)
    except Exception as e:
        print(f"Error loading {path}: {e}")

# Convert PIL images to Tkinter images
final_images = []
for img in images:
    photo = ImageTk.PhotoImage(img)
    final_images.append(photo)

# Label to display images
image_label = tk.Label(root)
image_label.pack(pady=30)

# Slideshow function (FIXED: no sleep, using after)
def start_slideshow(index=0):
    if len(final_images) == 0:
        return
    
    photo = final_images[index]
    image_label.config(image=photo)
    image_label.image = photo

    next_index = (index + 1) % len(final_images)  # loop slideshow
    root.after(2000, start_slideshow, next_index)  # 2 sec delay

# Button (FIXED: added pack)
play_button = tk.Button(
    root,
    text="Play Slideshow",
    font=("Arial", 17),
    command=start_slideshow
)
play_button.pack(pady=20)

# Run app
root.mainloop()