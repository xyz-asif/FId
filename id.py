https://stackoverflow.com/questions/41912372/dlib-installation-on-windows-10



import face_recognition
import os
import tkinter as tk
from tkinter import Label, filedialog

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb 


# Define a function to open the file dialog and get the path to the image to compare
def open_image():
    global image_to_compare_path
    image_to_compare_path = filedialog.askopenfilename(title='Select image to compare', filetypes=[('Image files', '*.jpg *.jpeg *.png')])

# Define a function to open the folder dialog and get the path to the folder containing the images
def open_folder():
    global folder_path
    folder_path = filedialog.askdirectory(title='Select folder containing images')

# Define a function to compare the face image with the images in the folder
def compare_images():
    # Clear the previous results in the listbox
    result_listbox.delete(0, tk.END)

    # Load the image to compare
    image_to_compare = face_recognition.load_image_file(image_to_compare_path)

    # Find the face location and encoding in the image to compare
    face_locations = face_recognition.face_locations(image_to_compare)
    if len(face_locations) == 0:
        result_listbox.insert(tk.END, 'No face found in the image to compare.')
        return
    face_encoding_to_compare = face_recognition.face_encodings(image_to_compare, face_locations)[0]

    # Initialize a flag to check if any match is found
    match_found = False

    # Loop through all the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
            # Load the image
            current_image = face_recognition.load_image_file(os.path.join(folder_path, filename))

            # Find the face location and encoding in the current image
            face_locations = face_recognition.face_locations(current_image)
            if len(face_locations) == 0:
                continue
            face_encodings = face_recognition.face_encodings(current_image, face_locations)

            # Compare the face encoding in the current image with the encoding in the image to compare
            results = face_recognition.compare_faces([face_encoding_to_compare], face_encodings[0], tolerance=0.6)

            # If the two face images are similar, add the filename to the listbox
            if results[0]:
                result_listbox.insert(tk.END, filename)
                match_found = True

    # If no match is found, display a message in the listbox
    if not match_found:
        result_listbox.insert(tk.END, 'No matches found.')

# Define a function to clear and make new comparisons
def clear_results():
    # Clear the previous results
    result_listbox.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title('Face Identification')
logo = tk.PhotoImage(file='xxx.png')

# Set the background color of the window
root.configure(bg=_from_rgb((255, 255, 255)))

# Create the logo label and place it in the window
logo_label = tk.Label(root, image=logo,borderwidth=0,highlightthickness=0)
logo_label.pack()

# Create the open image button and place it in the window
# Create the open image button and place it in the window
open_image_button = tk.Button(root, text='Select image to compare', command=open_image)
open_image_button.pack(padx=10, pady=10)

# Create the open folder button and place it in the window
open_folder_button = tk.Button(root, text='Select folder containing images', command=open_folder)
open_folder_button.pack(padx=10, pady=10)

# Create the compare button and place it in the window
compare_button = tk.Button(root, text='Compare', command=compare_images)
compare_button.pack(padx=10, pady=10)

# Create the clear button and place it in the window
clear_button = tk.Button(root, text='Clear results', command=clear_results)
clear_button.pack(padx=10, pady=10)

# Create the result listbox and place it in the window
result_listbox = tk.Listbox(root, width=50, height=10, bg=_from_rgb((255, 255, 204)))
result_listbox.pack(padx=10, pady=10)
root.configure(bg=_from_rgb((0, 7, 28))) 
# Start the main loop
root.mainloop()
import face_recognition
import os
import tkinter as tk
from tkinter import Label, filedialog

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb 


# Define a function to open the file dialog and get the path to the image to compare
def open_image():
    global image_to_compare_path
    image_to_compare_path = filedialog.askopenfilename(title='Select image to compare', filetypes=[('Image files', '*.jpg *.jpeg *.png')])

# Define a function to open the folder dialog and get the path to the folder containing the images
def open_folder():
    global folder_path
    folder_path = filedialog.askdirectory(title='Select folder containing images')

# Define a function to compare the face image with the images in the folder
def compare_images():
    # Clear the previous results in the listbox
    result_listbox.delete(0, tk.END)

    # Load the image to compare
    image_to_compare = face_recognition.load_image_file(image_to_compare_path)

    # Find the face location and encoding in the image to compare
    face_locations = face_recognition.face_locations(image_to_compare)
    if len(face_locations) == 0:
        result_listbox.insert(tk.END, 'No face found in the image to compare.')
        return
    face_encoding_to_compare = face_recognition.face_encodings(image_to_compare, face_locations)[0]

    # Initialize a flag to check if any match is found
    match_found = False

    # Loop through all the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
            # Load the image
            current_image = face_recognition.load_image_file(os.path.join(folder_path, filename))

            # Find the face location and encoding in the current image
            face_locations = face_recognition.face_locations(current_image)
            if len(face_locations) == 0:
                continue
            face_encodings = face_recognition.face_encodings(current_image, face_locations)

            # Compare the face encoding in the current image with the encoding in the image to compare
            results = face_recognition.compare_faces([face_encoding_to_compare], face_encodings[0], tolerance=0.6)

            # If the two face images are similar, add the filename to the listbox
            if results[0]:
                result_listbox.insert(tk.END, filename)
                match_found = True

    # If no match is found, display a message in the listbox
    if not match_found:
        result_listbox.insert(tk.END, 'No matches found.')

# Define a function to clear and make new comparisons
def clear_results():
    # Clear the previous results
    result_listbox.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title('Face Identification')
logo = tk.PhotoImage(file='xxx.png')

# Set the background color of the window
root.configure(bg=_from_rgb((255, 255, 255)))

# Create the logo label and place it in the window
logo_label = tk.Label(root, image=logo,borderwidth=0,highlightthickness=0)
logo_label.pack()

# Create the open image button and place it in the window
# Create the open image button and place it in the window
open_image_button = tk.Button(root, text='Select image to compare', command=open_image)
open_image_button.pack(padx=10, pady=10)

# Create the open folder button and place it in the window
open_folder_button = tk.Button(root, text='Select folder containing images', command=open_folder)
open_folder_button.pack(padx=10, pady=10)

# Create the compare button and place it in the window
compare_button = tk.Button(root, text='Compare', command=compare_images)
compare_button.pack(padx=10, pady=10)

# Create the clear button and place it in the window
clear_button = tk.Button(root, text='Clear results', command=clear_results)
clear_button.pack(padx=10, pady=10)

# Create the result listbox and place it in the window
result_listbox = tk.Listbox(root, width=50, height=10, bg=_from_rgb((255, 255, 204)))
result_listbox.pack(padx=10, pady=10)
root.configure(bg=_from_rgb((0, 7, 28))) 
# Start the main loop
root.mainloop()
