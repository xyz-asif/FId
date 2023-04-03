import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import dlib
import numpy as np
import cv2
import pickle

# Load pre-trained face recognition model
face_recognition_model = dlib.face_recognition_model_v1('asif.dat')

# Function to compute face embeddings
def compute_face_encodings(image, face_locations):
    face_encodings = []
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        face_encodings.append(face_recognition_model.compute_face_descriptor(face_image))
    return face_encodings

# Function to compare face embeddings
def compare_face_encodings(known_face_encodings, face_encoding_to_check):
    return np.linalg.norm(known_face_encodings - face_encoding_to_check, axis=1)

# Load known face embeddings from pickle file
known_face_encodings = []
known_face_names = []
if os.path.isfile('face_encodings.pickle'):
    with open('face_encodings.pickle', 'rb') as f:
        known_face_encodings, known_face_names = pickle.load(f)

# Create GUI
root = tk.Tk()
root.title('Face Recognition')
root.geometry('500x350')

# Create input image path label and entry
image_path_label = tk.Label(root, text='Input Image:')
image_path_label.pack()
image_path_entry = tk.Entry(root)
image_path_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
image_path_button = tk.Button(root, text='Browse', command=lambda: select_image_file(image_path_entry))
image_path_button.pack(side=tk.RIGHT)

# Create directory path label and entry
directory_path_label = tk.Label(root, text='Directory of Images:')
directory_path_label.pack()
directory_path_entry = tk.Entry(root)
directory_path_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
directory_path_button = tk.Button(root, text='Browse', command=lambda: select_directory(directory_path_entry))
directory_path_button.pack(side=tk.RIGHT)

# Create find most similar face button
find_button = tk.Button(root, text='Find Most Similar Face', command=lambda: find_most_similar_face(image_path_entry.get(), directory_path_entry.get(), known_face_encodings, known_face_names))
find_button.pack()

# Create most similar face image label
most_similar_image_label = tk.Label(root)
most_similar_image_label.pack()

# Create most similar face name label
most_similar_name_label = tk.Label(root, font=('Helvetica', 14))
most_similar_name_label.pack()

# Function to select input image file
def select_image_file(image_path_entry):
    image_path = filedialog.askopenfilename(filetypes=[('Image Files', ('*.jpg', '*.jpeg', '*.png'))])
    image_path_entry.delete(0, tk.END)
    image_path_entry.insert(0, image_path)

# Function to select directory of images
def select_directory(directory_path_entry):
    directory_path = filedialog.askdirectory()
    directory_path_entry.delete(0, tk.END)
    directory_path_entry.insert(0, directory_path)

# Function to find most similar face in directory of images
def find_most_similar_face(input_image_path, directory_path, known_face_encodings, known_face_names):
    # Load input image and detect faces
    input_image = cv2.imread(input_image_path)
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    # Check if input image has non-zero height
    if input_image.shape[0] == 0:
        messagebox.showerror('Error', 'Input image has zero height')
        return

    # Resize input image
    scale_factor = 0.5
    resized_image = cv2.resize(input_image, None, fx=scale_factor, fy=scale_factor)

    input_face_locations = dlib.get_frontal_face_detector()(resized_image, 1)

    # Compute face embeddings for input image
    input_face_encodings = compute_face_encodings(resized_image, input_face_locations)

    # Load images from directory and compute face embeddings
    directory_images = os.listdir(directory_path)
    directory_face_encodings = []
    for directory_image in directory_images:
        directory_image_path = os.path.join(directory_path, directory_image)
        directory_image = cv2.imread(directory_image_path)
        directory_image = cv2.cvtColor(directory_image, cv2.COLOR_BGR2RGB)
        directory_image_face_locations = dlib.get_frontal_face_detector()(directory_image, 1)
        directory_image_face_encodings = compute_face_encodings(directory_image, directory_image_face_locations)
        directory_face_encodings.extend(directory_image_face_encodings)

    # Compare input face embeddings to directory face embeddings
    distances = compare_face_encodings(directory_face_encodings, input_face_encodings[0])
    min_distance_idx = np.argmin(distances)

    # Display most similar face image and name
    most_similar_image = Image.open(os.path.join(directory_path, directory_images[min_distance_idx]))
    most_similar_image = most_similar_image.resize((150, 150), Image.ANTIALIAS)
    most_similar_image = ImageTk.PhotoImage(most_similar_image)
    most_similar_image_label.config(image=most_similar_image)
    most_similar_image_label.image = most_similar_image

    most_similar_name = known_face_names[min_distance_idx]
    most_similar_name_label.config(text=most_similar_name)


root.mainloop()

# import dlib
# import os
# import cv2
# import numpy as np
# from tensorflow import keras
# from keras.models import Model, load_model
# import tkinter as tk
# from tkinter import filedialog
# from PIL import Image, ImageTk
# from PIL import Image
# import numpy as np

# # Load ResNet model
# model = dlib.face_recognition_model_v1('asif.dat')

# # Function to preprocess image
# def preprocess_image(img_path):
#     img = Image.open(img_path)
#     img = img.resize((500, 500))
#     x = np.array(img)
#     x = x/255.0
#     return x

# # Function to get the embedding of an image using ResNet
# def get_embedding(img_path):
#     img = preprocess_image(img_path)
#     embedding = model.predict(img)[0]
#     return embedding

# # Function to find similar faces in a folder
# def find_similar_faces(face_embedding, folder_path, threshold=0.5):
#     similar_faces = []
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.jpg') or filename.endswith('.png'):
#             img_path = os.path.join(folder_path, filename)
#             embedding = get_embedding(img_path)
#             distance = np.linalg.norm(face_embedding-embedding)
#             if distance < threshold:
#                 similar_faces.append(img_path)
#     return similar_faces

# # Function to display the similar faces
# def display_similar_faces(similar_faces):
#     root = tk.Tk()
#     root.title("Similar Faces")
#     root.geometry("500x500")

#     for i in range(len(similar_faces)):
#         img = Image.open(similar_faces[i])
#         img = img.resize((250, 250), Image.ANTIALIAS)
#         img = ImageTk.PhotoImage(img)

#         label = tk.Label(root, image=img)
#         label.image = img
#         label.pack(pady=10)

#     root.mainloop()

# # Function to handle the button click event
# def handle_button():
#     face_path = face_textbox.get()
#     folder_path = folder_textbox.get()
#     face_embedding = get_embedding(face_path)
#     similar_faces = find_similar_faces(face_embedding, folder_path)
#     display_similar_faces(similar_faces)

# # Create the GUI using Tkinter
# root = tk.Tk()
# root.title("Face Recognition App")
# root.geometry("400x200")

# face_label = tk.Label(root, text="Face Image:")
# face_label.grid(row=0, column=0, padx=5, pady=5)

# face_textbox = tk.Entry(root, width=30)
# face_textbox.grid(row=0, column=1, padx=5, pady=5)

# face_button = tk.Button(root, text="Browse", command=lambda: face_textbox.insert(tk.END, filedialog.askopenfilename()))
# face_button.grid(row=0, column=2, padx=5, pady=5)

# folder_label = tk.Label(root, text="Folder of Images:")
# folder_label.grid(row=1, column=0, padx=5, pady=5)

# folder_textbox = tk.Entry(root, width=30)
# folder_textbox.grid(row=1, column=1, padx=5, pady=5)

# folder_button = tk.Button(root, text="Browse", command=lambda: folder_textbox.insert(tk.END, filedialog.askdirectory()))
# folder_button.grid(row=1, column=2, padx=5, pady=5)

# submit_button = tk.Button(root, text="Submit", command=handle_button)
# submit_button.grid(row=2, column=1, padx=5, pady=5)

# root.mainloop()
# from tensorflow.keras.applications.resnet50 import ResNet50,preprocess_input
# from cgitb import text
# import dlib
# import os
# import cv2
# import numpy as np
# import tkinter as tk
# from tkinter import filedialog
# import numpy as np



# # Load ResNet50 model

# model = ResNet50(weights='resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5',
#                  include_top=False, input_shape=(500, 500, 3))

# # Load face detector and shape predictor models
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor('sss.dat')

# # Define function to resize image to 500x500 pixels
# def resize_image(img):
#     height, width = img.shape[:2]
#     if height > width:
#         scale = 500/height
#         new_height = 500
#         new_width = int(scale * width)
#     else:
#         scale = 500/width
#         new_width = 500
#         new_height = int(scale * height)
#     resized_img = cv2.resize(img, (new_width, new_height))
#     return resized_img

# # Define function to extract features from face image using ResNet50 model
# def extract_features(img):
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img = cv2.resize(img, (224, 224))
#     img = preprocess_input(img)
#     features = model.predict(np.array([img]))
#     return features

# # Define function to find similar faces in folder
# def find_similar_faces(face_features, folder_path):
#     # Loop over images in folder
#     for file_name in os.listdir(folder_path):
#         if not file_name.endswith('.jpg'):
#             continue
#         image_path = os.path.join(folder_path, file_name)
#         # Load image
#         image = cv2.imread(image_path)
#         # Resize image
#         image = resize_image(image)
#         # Detect faces in image
#         faces = detector(image, 1)
#         if len(faces) == 0:
#             continue
#         # Extract features from each face in image
#         for face in faces:
#             landmarks = predictor(image, face)
#             face_img = image[face.top():face.bottom(), face.left():face.right()]
#             face_features_other = extract_features(face_img)
#             # Compute distance between face features
#             distance = np.linalg.norm(face_features - face_features_other)
#             # If distance is below threshold, add image path to list of similar faces
#             if distance < 0.6:
#                 text.insert(tk.END, image_path + '\n')
#                 break

# # Define function to select face image
# def select_face_image():
#     global face_image
#     face_image_path = filedialog.askopenfilename()
#     face_image = cv2.imread(face_image_path)
#     face_image = resize_image(face_image)

# # Define function to select folder of images
# def select_folder():
#     global folder_path
#     folder_path = filedialog.askdirectory()

# # Define function to find similar faces
# def find_similar():
#     # Extract features from face image
#     face_features = extract_features(face_image)
#     # Find similar faces in folder
#     find_similar_faces(face_features, folder_path)

# # Create GUI window
# root = tk.Tk()
# root.title('Find Similar Faces')

# # Create button to select face image
# select_face_image_button = tk.Button(root, text='Select Face Image', command=select_face_image)
# select_face_image_button.pack(side=tk.LEFT, padx=20, pady=20)

# # Create button to select folder of images
# select_folder_button = tk.Button(root, text='Select Folder', command=select_folder)
# select_folder_button.pack(side=tk.LEFT, padx=20, pady=20)

# find_similar_button = tk.Button(root, text='Find Similar Faces', command=find_similar)
# find_similar_button.pack(side=tk.LEFT, padx=20, pady=20)

# text = tk.Text(root, height=20, width=50)
# text.pack(side=tk.LEFT, padx=20, pady=20)
# root.mainloop()