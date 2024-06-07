import os
import shutil
from datetime import datetime

def rename_finviz_files(directory, old_pattern, new_pattern):
    # Ensure the directory exists
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist.")
        return

    # List all files in the directory
    files = os.listdir(directory)

    for filename in files:
        if old_pattern in filename:
            # Extracting the original file extension
            file_extension = os.path.splitext(filename)[1]

            # Define the new filename
            new_filename = new_pattern.format(datetime.now().strftime("%Y%m%d%H%M%S")) + file_extension

            # Create the full path for the old and new filenames
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)

            # Rename the file
            shutil.move(old_file, new_file)
            print(f"Renamed {old_file} to {new_file}")

# Directory where the Finviz files are located
directory = "/home/Agendia Morfaw/Documents/Finviz"

# Pattern in the old filenames to identify Finviz files
old_pattern = "Finviz"

# New naming convention: e.g., "Finviz_{timestamp}.csv"
new_pattern = "Finviz_{}"

# Call the function to rename the files
rename_finviz_files(directory, old_pattern, new_pattern)