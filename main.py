import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageDraw
from tkcolorpicker import askcolor
import os

selected_color = "#FF0000"
original_image = None
new_image = None
image_paths = []
image_index = 0

root = tk.Tk()
root.title("Profile Picture Creator")
root.geometry("800x600")

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

image_info_label = ttk.Label(root)
image_info_label.pack()

# image preview thing that doesnt even fucking work
image_preview_frame = ttk.Frame(root, width=600, height=400)
image_preview_frame.pack()

# label 
image_label = ttk.Label(image_preview_frame)
image_label.pack(fill="both", expand=True)

def list_images():
    global image_paths
    image_paths = [os.path.join(root, file) for root, _, files in os.walk("images") for file in files if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

def load_image(index):
    global original_image, new_image
    if 0 <= index < len(image_paths):
        image_path = image_paths[index]
        original_image = Image.open(image_path)
        original_image.thumbnail((600, 400))
        color_image(original_image, selected_color)
        update_image_info_label(index)

def load_next_image():
    global image_index
    if image_index < len(image_paths) - 1:
        image_index += 1
        load_image(image_index)

def load_previous_image():
    global image_index
    if image_index > 0:
        image_index -= 1
        load_image(image_index)

def choose_color():
    global selected_color
    selected_color = askcolor()[1]
    color_image(original_image, selected_color)

def color_image(img, color):
    global new_image
    new_image = img.copy()
    draw = ImageDraw.Draw(new_image)
    color_tuple = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    for x in range(new_image.width):
        for y in range(new_image.height):
            pixel = img.getpixel((x, y))
            if pixel[3] == 0:
                draw.point((x, y), fill=color_tuple)
    update_image(new_image)

def update_image(img):
    global displayed_image
    displayed_image = ImageTk.PhotoImage(img)
    image_label.config(image=displayed_image)
    image_label.image = displayed_image

def update_image_info_label(index):
    total_images = len(image_paths)
    image_info_label.config(text=f"Image {index + 1}/{total_images}")

def export_image():
    global new_image
    if new_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            new_image.save(file_path)

list_images()

style = ttk.Style()
style.configure("TButton", padding=10, font=("Arial", 12))

previous_button = ttk.Button(button_frame, text="Previous", command=load_previous_image)
previous_button.grid(row=0, column=0, padx=10)

next_button = ttk.Button(button_frame, text="Next", command=load_next_image)
next_button.grid(row=0, column=1, padx=10)

color_picker_button = ttk.Button(button_frame, text="Choose Color", command=choose_color)
color_picker_button.grid(row=0, column=2, padx=10)

export_button = ttk.Button(button_frame, text="Export Image", command=export_image)
export_button.grid(row=0, column=3, padx=10)

if image_paths:
    load_image(0)

root.mainloop()
