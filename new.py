# import face_recognition
# import os
# import tkinter as tk
# from tkinter import filedialog
# old one.,,,,,

# def open_image():
#     global image_to_compare_path
#     image_to_compare_path = filedialog.askopenfilename(title='Select image to compare', filetypes=[('Image files', '*.jpg *.jpeg *.png')])

# #  open the folder dialog and get the path to the folder containing the images
# def open_folder():
#     global folder_path
#     folder_path = filedialog.askdirectory(title='Select folder containing images')

# # compare the face image with the images in the folder
# def compare_images():

#     image_to_compare = face_recognition.load_image_file(image_to_compare_path)

 
#     face_encoding_to_compare = face_recognition.face_encodings(image_to_compare)[0]

#     # Loop through all the files in the folder
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.jpg') or filename.endswith('.png'):
#             # Load the image
#             current_image = face_recognition.load_image_file(os.path.join(folder_path, filename))

#             # Find the face location and encoding in the current image
#             face_locations = face_recognition.face_locations(current_image)
#             face_encodings = face_recognition.face_encodings(current_image, face_locations)

#             # Compare the face encoding in the current image with the encoding in the image to compare
#             results = face_recognition.compare_faces([face_encoding_to_compare], face_encodings[0], tolerance=0.6)

#             # If the two face images are similar, print the filename
#             if results[0]:
#                 result_listbox.insert(tk.END, filename)

# # Create the main window
# root = tk.Tk()
# root.title('Face Image Comparison')

# # Create the widgets
# image_button = tk.Button(root, text='Select Target', command=open_image)
# folder_button = tk.Button(root, text='Select DB', command=open_folder)
# compare_button = tk.Button(root, text='Compare images', command=compare_images)
# result_listbox = tk.Listbox(root, width=50)

# # Add the widgets to the window
# image_button.pack(pady=5)
# folder_button.pack(pady=5)
# compare_button.pack(pady=5)
# result_listbox.pack(pady=5)

# # Run the main loop
# root.mainloop()