import cv2
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, OptionMenu, Frame, ttk
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
    elif color_mode == 'yuv':
        return cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    else:
        return image 

def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        global image
        image = cv2.imread(file_path)
        if image is not None:
            
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()

            
            image_height, image_width = image.shape[:2]

            
            if image_width > screen_width or image_height > screen_height:
                aspect_ratio = min(screen_width / image_width, screen_height / image_height)
                new_width = int(image_width * aspect_ratio)
                new_height = int(image_height * aspect_ratio)
                image = resize_image(image, new_width, new_height)

            display_image(image, original_label)
            root.geometry(f"{2 * image.shape[1] + 100}x{image.shape[0] + 300}")

def display_image(image, label):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    label.config(image=img_tk, text="")  
    label.image = img_tk

def process_image():
    global processed_image
    width = width_var.get()
    height = height_var.get()
    color_mode = color_mode_var.get()
    
    width = int(width) if width.isdigit() and int(width) > 0 else None
    height = int(height) if height.isdigit() and int(height) > 0 else None
    
    resized_image = resize_image(image, width, height)
    processed_image = recolor_image(resized_image, color_mode)
    display_image(processed_image, processed_label)

def save_image():
    if processed_image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, processed_image)

root = Tk()
root.title("CoSize - Image Resizer & Recolor Tool")
root.geometry("800x400")
root.configure(bg="#F0F0F0")
root.resizable(True, True)
root.iconbitmap("icon.ico")


control_frame = Frame(root, bg="#F0F0F0", padx=10, pady=10)
control_frame.pack(fill="x")


Button(control_frame, text="Load Image", command=load_image, bg="#4CAF50", fg="white", padx=10, pady=5).grid(row=0, column=0, padx=5)


Button(control_frame, text="Save Image", command=save_image, bg="#2196F3", fg="white", padx=10, pady=5).grid(row=0, column=1, padx=5)


Label(control_frame, text="Width (px):", bg="#F0F0F0").grid(row=0, column=2, padx=5)
width_var = StringVar()
Entry(control_frame, textvariable=width_var, width=10).grid(row=0, column=3, padx=5)


Label(control_frame, text="Height (px):", bg="#F0F0F0").grid(row=0, column=4, padx=5)
height_var = StringVar()
Entry(control_frame, textvariable=height_var, width=10).grid(row=0, column=5, padx=5)


Label(control_frame, text="Color Mode:", bg="#F0F0F0").grid(row=0, column=6, padx=5)
color_mode_var = StringVar(value="none")
OptionMenu(control_frame, color_mode_var, "none", "gray", "hsv", "yuv").grid(row=0, column=7, padx=5)

Button(control_frame, text="Process Image", command=process_image, bg="#FF5722", fg="white", padx=10, pady=5).grid(row=0, column=8, padx=10)


frame = Frame(root, bg="#F0F0F0")
frame.pack()

Label(frame, text="Original Image", bg="#F0F0F0").grid(row=1, column=0)
original_label = Label(frame, bg="#E8E8E8", relief="ridge")
original_label.grid(row=2, column=0)

Label(frame, text="Process Image", bg="#F0F0F0").grid(row=1, column=1)
processed_label = Label(frame, bg="#E8E8E8", relief="ridge")
processed_label.grid(row=2, column=1)

processed_image = None

root.mainloop()
