import os
from datetime import datetime

def create_finviz_csv(downloads_folder):
    # Check if the "Downloads" folder exists
    if not os.path.isdir(downloads_folder):
        print(f"The directory {downloads_folder} does not exist.")
        return

    # Get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Convert datetime object to string
    str_current_datetime = str(current_datetime)

    # Original filename
    original_filename = "finviz.csv"
    
    # Create the new filename with datetime
    new_filename = f"finviz_{str_current_datetime}.csv"
    
    # Create the full path for the original and new files
    original_file_path = os.path.join(downloads_folder, original_filename)
    new_file_path = os.path.join(downloads_folder, new_filename)

    # Rename the file with datetime
    os.rename(original_file_path, new_file_path)

    print(f"File renamed from {original_file_path} to {new_file_path}")

# Define the "Downloads" folder path
downloads_folder = "/Users//Downloads"  # Replace "your_username" with your actual username

# Call the function to rename the file
create_finviz_csv(downloads_folder)