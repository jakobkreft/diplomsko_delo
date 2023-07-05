import os

# Directory containing the images to be renamed
FOL = "5"

dir_path = "posnetki/teren{FOL}AB/t{FOL}B".format(FOL = FOL)

# Loop over each file in the directory
for filename in os.listdir(dir_path):
    # Check if the file is a JPEG image
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        # Get the old and new file paths
        old_path = os.path.join(dir_path, filename)
        new_path = os.path.join(dir_path, f"frameCt5B{filename[6:]}")
        # Rename the file
        os.rename(old_path, new_path)
