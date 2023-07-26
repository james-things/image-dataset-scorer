# Local RLHF Viewer

A simple, graphical, local image dataset viewer which allows you to generate human feedback on that data, written in Python!

The script currently implements the following features and can be easily extended/altered to suit your needs:

 - Easy to interpret, user-friendly interface
 - `Create` or `Load` a ratings file (JSON) to associate with a particular dataset or objective
 - Select a target folder and search it and its subfolders recursively for images
 - Filter out previously rated images and enqueue yet-to-be-rated images for evaluation
 - Run through queued images quickly using `Like`, `Dislike`, `Skip`, and `Back` buttons
 - Ratings are stored in real-time, allowing for completion of rating work in convenient chunks
 - Images re-rated after traversing backwards in a session have their ratings data updated appropriately
 - To produce a dataset of only "Liked" images, a `Copy Liked to Target Dir` functionality is included
 - When copying liked images, automatically copy metadata (.txt) files with matching names
