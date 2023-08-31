# Image Dataset Scorer

A simple, graphical, local image dataset viewer which allows you to generate human feedback ("RLHF") metadata, written in Python

The script currently implements the following features and can be easily extended/altered to suit your needs:

 - Rate images as either `Liked` or `Disliked`
 - Easy to interpret, user-friendly interface
 - `Create` or `Select` a ratings file (JSON) to associate with a particular dataset or objective
 - Load altenate datasets on the fly with `Load Dataset` 
 - Select a target folder and search it and its subfolders recursively for images
 - Filter out previously rated images and enqueue yet-to-be-rated images for evaluation
 - Run through queued images quickly using `Like`, `Dislike`, `Skip`, and `Back` buttons
 - Automatically display contents of associated `imgfilename.txt` metadata file if found, when viewing images
 - Ratings are stored in real-time, allowing for completion of rating work in convenient chunks
 - Images re-rated after traversing backwards in a session have their ratings data updated appropriately
 - To produce a dataset of only "Liked" or "Disliked" images, a `Copy [Rating] to Target Dir` functionality is included
 - When copying rated images, automatically copy metadata (.txt) files with matching names
 - Filtering modes: `all`, `portrait`, `landscape`, `square`

## Demo

Rating images:
![demo-img-2](https://github.com/james-things/image-dataset-scorer/assets/71165873/999b815c-0124-40ee-8d7d-2978096be83e)

Save rating data:
![rating-data](https://github.com/james-things/local-rlhf-viewer/assets/71165873/fce74746-7495-48dd-9ba8-7009a43351f6)

Convenient keybinds: 
![new-keybinds](https://github.com/james-things/local-rlhf-viewer/assets/71165873/a67d3761-40d5-4cc5-89a4-55804faa3085)
