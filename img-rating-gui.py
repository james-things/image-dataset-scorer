import tkinter as tk
from tkinter import filedialog
import os
import json
import shutil
from PIL import Image, ImageTk

# utility function to get image files
def find_images(directory):
    images = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                images.append(os.path.join(root, file))
    return images

class ImageBrowser:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RLHF")
        self.root.configure(bg='white')
        
        # Create frames for ImagePanel and ButtonsPanel
        self.image_frame = tk.Frame(self.root, bg='white', bd=2, relief='groove')
        self.image_frame.pack(fill='both', expand=True, side='left', padx=(10,5), pady=10)
        
        self.buttons_frame = tk.Frame(self.root, bg='white', bd=2, relief='groove')
        self.buttons_frame.pack(fill='both', expand=False, side='right', padx=(5,10), pady=10)

        # Create label for images and place it in the image frame
        self.image_label = tk.Label(self.image_frame, bg='white')
        self.image_label.pack(fill='both', expand=False)

        # Buttons
        self.create_button(self.buttons_frame, "Like", self.like, "#90EE90")
        self.create_button(self.buttons_frame, "Dislike", self.dislike, "#FF7F7F")
        self.create_button(self.buttons_frame, "Skip", self.next_image, "#FFDEAD")
        self.create_button(self.buttons_frame, "Copy Liked", self.copy_liked, "#87CEFA")
        self.create_button(self.buttons_frame, "Load", self.load_directory, "#D3D3D3")

        self.directory_entry = tk.Entry(self.buttons_frame)
        self.directory_entry.pack(side='top', padx=5, pady=5, fill='x')

        self.root.geometry('1600x900') # This corresponds to a 16:9 ratio

        # Attributes
        self.images = []  # list of all image paths
        self.current_image = None  # index of the current image
        self.ratings = {}  # dictionary mapping image paths to ratings
        self.directory = ""
        self.ratings_file_path = ""
        self.load_directory()

    def create_button(self, frame, text, command, color):
        button = tk.Button(frame, text=text, command=command, font=("Arial", 10), bg=color, padx=20, pady=10, width=20)
        button.pack(side='top', padx=5, pady=5)

    def load_directory(self):
        self.directory = filedialog.askdirectory()
        if not self.directory:
            return
        self.ratings_file_path = f'{self.directory}/rlhf-ratings.json'

        print(self.ratings_file_path)
        self.load_ratings(self.ratings_file_path)

        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, self.directory)
        self.images = find_images(self.directory)
        self.current_image = 0 if self.images else None
        self.next_image()  # Display the first image

    def load_ratings(self, ratings_file):
        try:
            with open(ratings_file, 'r') as file:
                self.ratings = json.load(file)
        except FileNotFoundError:
            pass  # It's okay if the file doesn't exist

    def save_ratings(self, ratings_file):
        with open(ratings_file, 'w') as file:
            json.dump(self.ratings, file)

    def resize_image(self, img_path):
        # Fetch the size of the image panel
        panel_width = self.image_frame.winfo_width()
        panel_height = self.image_frame.winfo_height()

        with Image.open(img_path) as img:
            img_width, img_height = img.size

            if img_width > img_height:
                new_width = panel_width
                new_height = int((new_width * img_height) / img_width)
            else:
                new_height = panel_height
                new_width = int((new_height * img_width) / img_height)
                
            img = img.resize((new_width, new_height))
            self.photo_image = ImageTk.PhotoImage(img)

        return self.photo_image

    def next_image(self):
        if self.current_image is None or self.current_image >= len(self.images):
            self.current_image = None  # No more images
            self.image_label.config(image=None)  # Clear the image
            return

        # Load and display the next image
        path = self.images[self.current_image]
        photo_image = self.resize_image(path)
        self.image_label.config(image=photo_image)
        self.current_image += 1

    def rate_image(self, rating):
        if self.current_image is not None:
            path = self.images[self.current_image - 1]  # The last displayed image
            self.ratings[path] = rating
            self.save_ratings(self.ratings_file_path)  # Save after each rating in case the program crashes

    def like(self):
        self.rate_image('like')
        self.next_image()

    def dislike(self):
        self.rate_image('dislike')
        self.next_image()

    def copy_liked(self):
        copy_to_dir = filedialog.askdirectory()
        if not copy_to_dir:
            return
        for path, rating in self.ratings.items():
            if rating == 'like':
                shutil.copy(path, copy_to_dir)


if __name__ == "__main__":
    app = ImageBrowser()
    app.root.mainloop()
