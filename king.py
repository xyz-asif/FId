import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from deepface import DeepFace

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
    
    def create_widgets(self):
        # Create the face image selection button and label
        self.face_image_button = tk.Button(self)
        self.face_image_button["text"] = "Select face image"
        self.face_image_button["command"] = self.select_face_image
        self.face_image_button.pack(side="top")
        self.face_image_label = tk.Label(self)
        self.face_image_label.pack(side="top")
        
        # Create the folder selection button and label
        self.folder_button = tk.Button(self)
        self.folder_button["text"] = "Select folder"
        self.folder_button["command"] = self.select_folder
        self.folder_button.pack(side="top")
        self.folder_label = tk.Label(self)
        self.folder_label.pack(side="top")
        
        # Create the compare button
        self.compare_button = tk.Button(self)
        self.compare_button["text"] = "Compare"
        self.compare_button["command"] = self.compare_images
        self.compare_button.pack(side="top")
        
        # Create the result label
        self.result_label = tk.Label(self)
        self.result_label.pack(side="top")
        
        # Set the window title and size
        self.master.title("Face Image Comparison")
        self.master.geometry("400x400")
    
    def select_face_image(self):
        # Open a file dialog to select the face image file
        self.face_image_path = filedialog.askopenfilename(title="Select face image",
                                                          filetypes=[("Image Files", ".jpg .jpeg .png")])
        # Load the selected image and display it on the label
        self.face_image = Image.open(self.face_image_path)
        self.face_image = self.face_image.resize((200, 200))
        self.face_image_tk = ImageTk.PhotoImage(self.face_image)
        self.face_image_label.config(image=self.face_image_tk)
    
    def select_folder(self):
        # Open a file dialog to select the folder containing the images
        self.folder_path = filedialog.askdirectory(title="Select folder")
        self.folder_label.config(text=f"Selected folder: {self.folder_path}")
    
    def compare_images(self):
        # Check if both face image and folder have been selected
        if not hasattr(self, "face_image_path") or not hasattr(self, "folder_path"):
            messagebox.showerror("Error", "Please select both face image and folder.")
            return
        
        # Load the face image
        face_image = DeepFace.detectFace(self.face_image_path)
        
        # Loop through each image in the folder and compare with the face image
        match_found = False
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
                image_path = os.path.join(self.folder_path, filename)
                result = DeepFace.verify(self.face_image_path, image_path)
                
                # Check if the result indicates a match
                if result["verified"]:
                    match_found = True
                    self.result_label.config(text=f"Found a match with {filename}!")
                    break
        
        # If no match was found, display a message
        if not match_found:
            self.result_label.config(text="No similar images were found in the folder")
                                     

root = tk.Tk()
app = Application(master=root)
app.mainloop()





























































