import cv2
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, OptionMenu, Frame
from PIL import Image, ImageTk

def resize_image(image, width=None, height=None):
    original_height, original_width = image.shape[:2]
    if width and not height:
        ratio = width / float(original_width)
        dimensions = (width, int(original_height * ratio))
    elif height and not width:
        ratio = height / float(original_height)
        dimensions = (int(original_width * ratio), height)
    elif width and height:
        dimensions = (width, height)
    else:
        return image  
    return cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)

def recolor_image(image, color_mode):
    if color_mode == 'gray':
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif color_mode == 'hsv':
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    elif color_mode == 'lab':
        return cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    else:
        return image 

def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        global image
        image = cv2.imread(file_path)
        if image is not None:
            display_image(image, original_label)
            image_height, image_width = image.shape[:2]
            root.geometry(f"{2 * image_width + 50}x{image_height + 250}")  # Adjust window for both images

def display_image(image, label):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    label.config(image=img_tk)
    label.image = img_tk

def process_image():
    width = width_var.get()
    height = height_var.get()
    color_mode = color_mode_var.get()
    
    width = int(width) if width.isdigit() and int(width) > 0 else None
    height = int(height) if height.isdigit() and int(height) > 0 else None
    
    resized_image = resize_image(image, width, height)
    recolored_image = recolor_image(resized_image, color_mode)
    display_image(recolored_image, processed_label)

root = Tk()
root.title("CoSize")

root.iconbitmap("icon.ico")

root.geometry("400x500")
root.resizable(False, False)

Button(root, text="Load Image", command=load_image).pack()

Label(root, text="Width (px):").pack()
width_var = StringVar()
Entry(root, textvariable=width_var).pack()

Label(root, text="Height (px):").pack()
height_var = StringVar()
Entry(root, textvariable=height_var).pack()

Label(root, text="Color Mode:").pack()
color_mode_var = StringVar(value="none")
OptionMenu(root, color_mode_var, "none", "gray", "hsv", "lab").pack()

Button(root, text="Process Image", command=process_image).pack()


frame = Frame(root)
frame.pack()


original_label = Label(frame, text="Original Image")
original_label.grid(row=0, column=0, padx=10, pady=10)

processed_label = Label(frame, text="Processed Image")
processed_label.grid(row=0, column=1, padx=10, pady=10)

root.mainloop()
