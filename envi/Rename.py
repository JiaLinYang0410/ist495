from datetime import datetime
from tabulate import tabulate
import shutil
import os
import pandas as pd

# Get current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Path to the Downloads folder on a Mac
downloads_folder = os.path.expanduser("~/Downloads")
# Look for files named "finviz" in the Downloads folder
file_found = False
for file_name in os.listdir(downloads_folder):
    if file_name.startswith("finviz") and file_name.endswith(".csv"):
        file_found = True
        file_path = os.path.join(downloads_folder, file_name)
        # Generate new filename with current datetime appended
        new_file_name = f"finviz_{current_datetime}.csv"
        new_file_path = os.path.join(downloads_folder, new_file_name)
        # Rename the file
        shutil.move(file_path, new_file_path)
        print(f"File renamed: {file_name} -> {new_file_name}")

        # Load the renamed CSV file into a DataFrame
        data_import = pd.read_csv(new_file_path)
        print("\nRaw data loaded from CSV:")
        print(tabulate(data_import.head(), headers='keys', tablefmt='psql'))
        break

if not file_found:
    print("No 'finviz' CSV files found in the Downloads folder.")
    exit()