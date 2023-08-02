# Local RLHF Viewer

A simple, graphical, local image dataset viewer which allows you to generate human feedback on that data, written in Python!

The script currently implements the following features and can be easily extended/altered to suit your needs:

 - Rate images as either `Liked` or `Disliked`
 - Easy to interpret, user-friendly interface
 - `Create` or `Load` a ratings file (JSON) to associate with a particular dataset or objective
 - Select a target folder and search it and its subfolders recursively for images
 - Filter out previously rated images and enqueue yet-to-be-rated images for evaluation
 - Run through queued images quickly using `Like`, `Dislike`, `Skip`, and `Back` buttons
 - Ratings are stored in real-time, allowing for completion of rating work in convenient chunks
 - Images re-rated after traversing backwards in a session have their ratings data updated appropriately
 - To produce a dataset of only "Liked" images, a `Copy Liked to Target Dir` functionality is included
 - When copying liked images, automatically copy metadata (.txt) files with matching names

## Demo

Creating ratings file:
![demo-img-1](https://github.com/james-things/local-rlhf-viewer/assets/71165873/51314569-1be1-4f9b-b6c4-7f2d8a4790cb)

Rating images:
![demo-img-2](https://github.com/james-things/local-rlhf-viewer/assets/71165873/b9e0f3a3-6403-4f8d-92f9-5875cfe8a487)

Save rating data:
![rating-data](https://github.com/james-things/local-rlhf-viewer/assets/71165873/fce74746-7495-48dd-9ba8-7009a43351f6)

Convenient keybinds: 
![new-keybinds](https://github.com/james-things/local-rlhf-viewer/assets/71165873/a67d3761-40d5-4cc5-89a4-55804faa3085)
