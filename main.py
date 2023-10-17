import tkinter
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import os, sys


# Create a font style with increased font size and bold
custom_font = ("Courier New", 20, "bold")

# Function to restart the software
def restart_software():
    python = sys.executable
    os.execl(python, python, * sys.argv)
    
# Function to toggle between light and dark mode
def toggle_dark_mode():
    background_color = "#1E1E1E"
    text_color = "white"
    text_bt_color = "#1E1E1E"
    window.configure(bg=background_color)
    label_frame.configure(bg=background_color, fg=text_color)
    total_images_label.configure(bg=background_color, fg=text_color)
    image_name_label.configure(bg=background_color, fg=text_color)
    text_label.configure(bg=background_color, fg=text_bt_color)
    text_entry.configure(bg=background_color, fg=text_bt_color)
    button_select_image.configure(bg=background_color, fg=text_bt_color)
    button_enter_data.configure(bg=background_color, fg=text_bt_color)
    button_next_image.configure(bg=background_color, fg=text_bt_color)
    window.update_idletasks()
    
    
window = tkinter.Tk()
window.title("Data Entry Application | Optical Charactor Regonition")
# window.configure(bg="#1E1E1E")  # Set background color for dark mode

# -------------------------------- Custom Menu Bar ----------------------------
# Create a menu bar
menu_bar = tkinter.Menu(window)
window.config(menu=menu_bar)

# Create a File menu
file_menu = tkinter.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Restart", command=restart_software)  # Added Restart option
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

# Create a View menu
view_menu = tkinter.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)
view_menu.add_separator()
view_menu.add_checkbutton(label="Show Image Names", onvalue=True, offvalue=False, variable=tkinter.BooleanVar())

# Create a Help menu
help_menu = tkinter.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "The purpose of this appplication is use for entry data of project OCR only!!!"))
help_menu.add_separator()
help_menu.add_command(label="Help", command=lambda: messagebox.showinfo("Help", "Any error or bugs please contact: Metythorn Penn | 19059"))

# ------------------------- Window Size ------------------------------


def update_label_frame_position(event):
    label_frame.update_idletasks()  # Update the label_frame geometry information
    label_frame_width = label_frame.winfo_width()
    label_frame_height = label_frame.winfo_height()
    x_coordinate = (window_width - label_frame_width) // 2
    y_coordinate = (window_height - label_frame_height) // 2
    label_frame.place(x=x_coordinate, y=y_coordinate)


# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window size to be 80% of the screen width and height
window_width = int(screen_width * 0.99)
window_height = int(screen_height * 0.99)

# Calculate the x and y coordinates to center the window
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Configure rows and columns to be flexible
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# ---------------------- || ---------------------------------

# Variable to store the total number of images
total_images = tkinter.StringVar()
total_images.set("Total Images: 0")



# Variable to track the current image index
current_image_index = 0

# List to store image files and folder path
image_files = []
folder_path = ""


# --------------------------- Action function when user clicks enter ----------------------------------
# Function to handle entering data
def enter_data():
    label = text_entry.get()
    text_entry.delete(0, tkinter.END)
    text_entry.focus()

    global current_image_index

    current_image_index = (current_image_index + 1) % len(image_files)
    if current_image_index == 0:
        messagebox.showinfo("End of Images", "You have reached the last image in the folder.")
    update_image()

    # Save user info and image folder path to text file 
    with open("data_file.txt", "a") as file:
        file.write("train/" + image_files[current_image_index] + " " + label + "\n")


# Function to update the displayed image and its name
def update_image():
    global current_image_index
    if image_files:
        current_image_path = os.path.join(folder_path, image_files[current_image_index])
        original_image = Image.open(current_image_path)
        fixed_height = 300
        width_percent = (fixed_height / float(original_image.size[1]))
        new_width = int((float(original_image.size[0]) * float(width_percent)))
        resized_image = original_image.resize((new_width, fixed_height), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized_image)
        image_label.config(image=photo)
        image_label.image = photo
        image_name_label.config(text="Image : " + image_files[current_image_index])


# Function to update the data file with new information
def update_data_file():
    global current_image_index
    new_label = text_entry.get()
    
    # Update the data file with new information based on the previous image name
    if current_image_index > 0 and current_image_index <= len(image_files):
        previous_image_name = image_files[current_image_index - 1]
        with open("data_file.txt", "r") as file:
            lines = file.readlines()
        with open("data_file.txt", "w") as file:
            for line in lines:
                if previous_image_name in line:
                    file.write("train/" + previous_image_name + " " + new_label + "\n")
                else:
                    file.write(line)
    
    text_entry.delete(0, tkinter.END)
    text_entry.focus()
    messagebox.showinfo("Data Updated", "Data has been updated for the previous image.")



# Function to go to the next image in the folder
def previous_image():
    global current_image_index
    current_image_index = (current_image_index - 1) % len(image_files)
    update_image() 

# Function to display the label from data_file for the previous image
def display_previous_label():
    global current_image_index
    if current_image_index > 0 and current_image_index <= len(image_files):
        previous_image_name = image_files[current_image_index - 1]
        with open("data_file.txt", "r") as file:
            lines = file.readlines()
        for line in lines:
            if previous_image_name in line:
                _, previous_label = line.strip().split(" ", 1)
                text_entry.delete(0, tkinter.END)
                text_entry.insert(0, previous_label)
                break
        else:
            text_entry.delete(0, tkinter.END)


# create function that user can select an image folder from the computer and display the first image in the folder
def select_image_folder():
    global folder_path, image_files, current_image_index
    folder_path = filedialog.askdirectory()
    print(folder_path)
    # messagebox.showinfo("Image Folder", "You have selected " + folder_path)
    
    # save image folder path to text file
    with open("data_file.txt", "a") as file:
        file.write("Image Folder: " + folder_path + "\n")
    
    # Get the list of image files in the selected folder
    files = os.listdir(folder_path)
    image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    # total_images.set("Total Images: " + str(current_image_index + 1) + " / " +str(len(image_files)))  # Update the total image count
    total_images.set("Total Images: " +  str(len(image_files)))
    total_images_label.config(font=custom_font)
    
    # current_image_index.set("Current Image Index: " + str(current_image_index))
    if image_files:
        current_image_index = 0
        update_image()
    else:
        messagebox.showwarning("No Images", "The selected folder does not contain any images.")


# ---------------- Button to enter data ---------------------


label_frame = tkinter.LabelFrame(window, text="Enter Data Area", font=custom_font)
label_frame.grid(row=5, column=0, padx=10, pady=10, sticky="w")

# Select Folder 
button_select_image = tkinter.Button(label_frame, text="Select Image Folder", command=select_image_folder, font=custom_font)
button_select_image.grid(row=0, column=0, padx=20, pady=2, sticky="w")

# Label to display the total number of images
total_images_label = tkinter.Label(label_frame, textvariable=total_images, font=custom_font)
total_images_label.grid(row=1, column=0, padx=20, pady=2, sticky="w")

# Label to display the image name
image_name_label = tkinter.Label(label_frame, text="Image : ", font=custom_font)
image_name_label.grid(row=1, column=1, padx=20, pady=2, sticky="w")

# Label to display the selected image
image_label = tkinter.Label(label_frame)
image_label.grid(row=2, column=0, padx=20, pady=2, sticky="w")

text_label = tkinter.Label(label_frame, text="Label", font=custom_font)
text_label.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="w")

text_entry = tkinter.Entry(label_frame)
text_entry.grid(row=3, column=0, columnspan=2, padx=25, pady=5, sticky="w")

button_enter_data = tkinter.Button(label_frame, text="Enter Data", command=enter_data, font= custom_font)
button_enter_data.grid(row=3, column=1, columnspan=2, padx=20, pady=5, sticky="w")

# Button to navigate to the next image
button_next_image = tkinter.Button(label_frame, text="Previous Image", command=previous_image, font=custom_font)
button_next_image.grid(row=4, column=0, padx=20, pady=5, sticky="w")


for widget in label_frame.winfo_children():
    widget.grid_configure(padx=150, pady=40, sticky="w")

# --------------- Custom Shortcut Key -------------------
# Bind the Enter key to call enter_data function
def enter_data_key(event):
    enter_data()
    
window.bind("<Return>", enter_data_key)


# Bind the Up arrow key to call previous_image function
def previous_image_key(event):
    if event.state == 4:
        previous_image()
window.bind("<Left>", previous_image_key)

# Bind the function to the window's resize event
window.bind("<Configure>", update_label_frame_position)

window.mainloop()


