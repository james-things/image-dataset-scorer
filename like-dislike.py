import tkinter as tk
from tkinter import filedialog
import os
import json
import shutil
from PIL import Image, ImageTk

# Utility function to get image files, filtering already rated images
def find_images(directory, ratings):
    images = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                if image_path not in ratings:
                    images.append(image_path)
    return images

# Primary application class
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
        self.create_button(self.buttons_frame, "Back", self.prev_image, "#DEADFF")
        self.create_button(self.buttons_frame, "Copy Liked", self.copy_liked, "#87CEFA")
        self.create_button(self.buttons_frame, "Load", self.load_directory, "#D3D3D3")

        self.directory_entry = tk.Entry(self.buttons_frame)
        self.directory_entry.pack(side='top', padx=5, pady=5, fill='x')

        self.root.geometry('1600x900') # currently hardcoded for a 2k display

        # Attributes
        self.images = []  # list of all image paths
        self.current_image = None  # index of the current image
        self.ratings = {}  # dictionary mapping image paths to ratings
        self.directory = ""
        self.ratings_file_path = ""
        self.prev_image_index = None 
        self.load_directory()

    # Create a tkinter button with the appropriate parameters
    def create_button(self, frame, text, command, color):
        button = tk.Button(frame, text=text, command=command, font=("Arial", 10), bg=color, padx=20, pady=10, width=20)
        button.pack(side='top', padx=5, pady=5)

    # Step user through process to load image data and define ratings file
    def load_directory(self):
        self.directory = filedialog.askdirectory()
        if not self.directory:
            return

        load_or_create = tk.messagebox.askyesno("Ratings File", 
                                                "Would you like to load an existing ratings file?\n"
                                                "Select 'No' to create a new ratings file.")
        if load_or_create:
            # User wants to load an existing file
            self.ratings_file_path = filedialog.askopenfilename(defaultextension=".json",
                                                                filetypes=[("JSON files", "*.json")],
                                                                title="Select existing ratings file")
        else:
            # User wants to create a new file
            self.ratings_file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                                  filetypes=[("JSON files", "*.json")],
                                                                  title="Create new ratings file")
            if self.ratings_file_path:
                # If the file already exists, delete it to enforce the overwrite.
                if os.path.isfile(self.ratings_file_path):
                    os.remove(self.ratings_file_path)

        if not self.ratings_file_path:
            return

        print(f'Ratings File: {self.ratings_file_path}')
        self.load_ratings(self.ratings_file_path)

        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, self.directory)
        self.images = find_images(self.directory, self.ratings)

        self.current_image = -1 if self.images else None
        self.next_image()  # Display the first image

    # Load a target ratings JSON
    def load_ratings(self, ratings_file):
        try:
            with open(ratings_file, 'r') as file:
                self.ratings = json.load(file)
        except Exception:
            pass  # discard any exception

    # Save ratings to the defined ratings file
    def save_ratings(self, ratings_file):
        with open(ratings_file, 'w') as file:
            json.dump(self.ratings, file, indent=4)

    # Resize an image to fit within the display area
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

    # Clear the image in the display area (used when we reach last image)
    def clear_image(self):
        # Create a blank image and display it in the label
        blank_image = ImageTk.PhotoImage(Image.new('RGB', (1, 1)))
        self.image_label.config(image=blank_image)
        self.image_label.image = blank_image  # Keep a reference to avoid garbage collection

    # Advance to the next queued image
    def next_image(self):
        if self.current_image is not None:
            self.prev_image_index = self.current_image
            self.current_image += 1

        if self.current_image is not None and self.current_image < len(self.images):
            # Load and display the next image
            path = self.images[self.current_image]
            photo_image = self.resize_image(path)
            self.image_label.config(image=photo_image)
        else:
            self.current_image = None  # No more images
            self.clear_image()  # Clear the image

    # Step backwards to the previously viewed image
    def prev_image(self):
        # Move to the previous image
        if self.prev_image_index is not None and self.prev_image_index >= 0:
            self.current_image = self.prev_image_index
            self.prev_image_index -= 1

            path = self.images[self.current_image]
            photo_image = self.resize_image(path)
            self.image_label.config(image=photo_image)

    # Rate the currently viewed image
    def rate_image(self, rating):
        if self.current_image is not None:
            path = self.images[self.current_image]
            self.ratings[path] = rating
            self.save_ratings(self.ratings_file_path)  # Save after each rating in case the program terminates unexpectedly

    # Apply a positive rating and advance to the next image
    def like(self):
        self.rate_image('like')
        self.next_image()

    # Apply a negative rating and advance to the next image
    def dislike(self):
        self.rate_image('dislike')
        self.next_image()

    # Copy all positively rated images and associated metadata to target directory
    def copy_liked(self):
        copy_to_dir = filedialog.askdirectory()
        if not copy_to_dir:
            return
        for path, rating in self.ratings.items():
            if rating == 'like':
                # Copy the image
                shutil.copy(path, copy_to_dir)

                # Check if a .txt file exists with the same name, and copy it
                txt_path = os.path.splitext(path)[0] + ".txt"
                if os.path.exists(txt_path):
                    shutil.copy(txt_path, copy_to_dir)

# Script entry point
if __name__ == "__main__":
    app = ImageBrowser()
    app.root.mainloop()
