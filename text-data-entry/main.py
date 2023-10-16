import tkinter
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import os

window = tkinter.Tk()
window.title("Data Entry Form")

# Set the window size to be 80% of the screen width and height
# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window size to be 80% of the screen width and height
window_width = int(screen_width * 0.999)
window_height = int(screen_height * 0.999)
window.geometry(f"{window_width}x{window_height}")


frame = tkinter.Frame(window)
frame.grid(row=0, column=0, sticky="nsew")



# Variable to store the total number of images
total_images = tkinter.StringVar()
total_images.set("Total Images: 0")

# Variable to track the current image index
current_image_index = 0

# List to store image files and folder path
image_files = []
folder_path = ""

# --------------- Action function when user clicks enter ----------
def enter_data():
    label = text_entry.get()
    text_entry.delete(0, tkinter.END)
    text_entry.focus()
    
    # save user info and image folder path to text file 
    with open("data_file.txt", "a") as file:
        file.write("Image Folder: " + folder_path + ", Label: " + label + "\n")
    
    # messagebox.showinfo("Data Entry Form", "Data has been entered")

# Function to update the displayed image and its name
def update_image():
    global current_image_index
    if image_files:
        current_image_path = os.path.join(folder_path, image_files[current_image_index])
        image = Image.open(current_image_path)
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo
        image_name_label.config(text="Image : " + image_files[current_image_index])

# Function to go to the next image in the folder
def next_image():
    global current_image_index
    current_image_index = (current_image_index + 1) % len(image_files)
    if current_image_index == 0:
        messagebox.showinfo("End of Images", "You have reached the last image in the folder.")
    update_image()

# create function that user can select an image folder from the computer and display the first image in the folder
def select_image_folder():
    global folder_path, image_files, current_image_index
    folder_path = filedialog.askdirectory()
    print(folder_path)
    messagebox.showinfo("Image Folder", "You have selected " + folder_path)
    
    # save image folder path to text file
    with open("data_file.txt", "a") as file:
        file.write("Image Folder: " + folder_path + "\n")
    
    # Get the list of image files in the selected folder
    files = os.listdir(folder_path)
    image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    total_images.set("Total Images: " + str(len(image_files)))  # Update the total image count
    
    if image_files:
        current_image_index = 0
        update_image()
    else:
        messagebox.showwarning("No Images", "The selected folder does not contain any images.")

# --------------- Button to select image folder ---------------
button_select_image = tkinter.Button(frame, text="Select Image Folder", command=select_image_folder)
button_select_image.grid(row=0, column=0, padx=40, pady=20, sticky="w")

# Label to display the total number of images
total_images_label = tkinter.Label(frame, textvariable=total_images)
total_images_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

# Label to display the selected image
image_label = tkinter.Label(frame)
image_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

# Label to display the image name
image_name_label = tkinter.Label(frame, text="Image : ")
image_name_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

# Button to navigate to the next image
button_next_image = tkinter.Button(frame, text="Next Image", command=next_image)
button_next_image.grid(row=4, column=0, padx=20, pady=10, sticky="w")

# ---------------- Button to enter data ---------------------
label_frame = tkinter.LabelFrame(frame, text="Enter Data Area")
label_frame.grid(row=0, column=2, padx=40, pady=20, rowspan=5, sticky="nsew")

text_label = tkinter.Label(label_frame, text="Label")
text_label.grid(row=0, column=1, columnspan=2, padx=20, pady=10, sticky="w")

text_entry = tkinter.Entry(label_frame)
text_entry.grid(row=0, column=2)

for widget in label_frame.winfo_children():
    widget.grid_configure(padx=100, pady=50, sticky="w")

# ---------------- Button to enter data ---------------------
button_enter_data = tkinter.Button(label_frame, text="Enter Data", command=enter_data)
button_enter_data.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="w")

window.mainloop()