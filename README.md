# Local RLHF Viewer

A simple, graphical, local image dataset viewer which allows you to generate human feedback on that data, written in Python!

The script currently implements the following features and can be easily extended/altered to suit your needs:

 - Easy to interpret, user-friendly interface
 - Select a target folder and search it and its subfolders recursively for images
 - Filter out previously rated images and enqueue yet-to-be-rated images for evaluation
 - Run through queued images quickly using "Like", "Dislike", and "Skip" buttons
 - Ratings are stored in real-time, allowing for completion of rating work in convenient chunks
 - To produce a dataset of only "Liked" images, a "Copy Liked to Target Dir" functionality is included
 - A JSON of the rating data is saved to the directory targeted for loading
