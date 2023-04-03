import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import face_recognition


class ImageComparator:
    def __init__(self):
        self.target_image_path = None
        self.image_folder_path = None

        self.window = tk.Tk()
        self.window.title("Image Comparator")
        self.window.geometry("800x600")

        self.target_image_label = tk.Label(self.window, text="Target Image")
        self.target_image_label.pack(pady=10)

        self.target_image_button = tk.Button(self.window, text="Select Image", command=self.select_target_image)
        self.target_image_button.pack()

        self.image_folder_label = tk.Label(self.window, text="Image Folder")
        self.image_folder_label.pack(pady=10)

        self.image_folder_button = tk.Button(self.window, text="Select Folder", command=self.select_image_folder)
        self.image_folder_button.pack()

        self.compare_button = tk.Button(self.window, text="Compare Images", command=self.compare_images)
        self.compare_button.pack(pady=10)

        self.most_similar_label = tk.Label(self.window, text="Most Similar Image")
        self.most_similar_label.pack(pady=10)

        self.window.mainloop()

    def select_target_image(self):
        self.target_image_path = filedialog.askopenfilename(
            title="Select Image", filetypes=[("Image Files", "*.jpg *.png")]
        )

    def select_image_folder(self):
        self.image_folder_path = filedialog.askdirectory(title="Select Folder")

    def compare_images(self):
        if self.target_image_path and self.image_folder_path:
            # Load the target image and convert to encoding
            target_image = face_recognition.load_image_file(self.target_image_path)
            target_encoding = face_recognition.face_encodings(target_image, num_jitters=100)[0]

            # Load the images in the image folder and compare to target image
            matches = {}
            for filename in os.listdir(self.image_folder_path):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    # Load the image and convert to encoding
                    image_path = os.path.join(self.image_folder_path, filename)
                    image = face_recognition.load_image_file(image_path)
                    encodings = face_recognition.face_encodings(image, num_jitters=100)

                    # Calculate the similarity between the target face and the image face
                    if encodings:
                        face_distance = face_recognition.face_distance(encodings, target_encoding)
                        similarity = 1 - face_distance

                        # Check if any of the face distances are less than the threshold
                        if (similarity >= 0.6).any():
                            # The image contains a face that is similar enough to the target face
                            # Add the filename and similarity score to the matches dictionary
                            matches[filename] = similarity[0]

            # Sort the matches by descending similarity score
            sorted_matches = sorted(matches.items(), key=lambda x: x[1], reverse=True)

            # Display the most similar image, if any
            if sorted_matches:
                most_similar_path = os.path.join(self.image_folder_path, sorted_matches[0][0])
                most_similar_image = Image.open(most_similar_path)
                most_similar_resized = most_similar_image.resize((600, 400), Image.ANTIALIAS)
                most_similar_tk = ImageTk.PhotoImage(most_similar_resized)
                self.most_similar_label.config(image=most_similar_tk)
                self.most_similar_label.image = most_similar_tk


if __name__ == "__main__":
    app = ImageComparator()
