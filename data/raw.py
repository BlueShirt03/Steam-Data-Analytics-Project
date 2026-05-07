# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import os
import kagglehub
import pandas as pd

# List all files in the dataset
""" ['reviews-1-115.csv', 
      'reviews-11265-13495.csv', 
      'reviews-115-1230.csv', 
      'reviews-1230-2345.csv', 
      'reviews-13495-13500.csv', 
      'reviews-13500-13537.csv', 
      'reviews-13537-27075.csv', 
      'reviews-2345-4575.csv', 
      'reviews-4575-6805.csv', 
      'reviews-6805-9035.csv', 
      'reviews-9035-11265.csv']"""

# Load the dataset (adjust the file name as needed)

def load_data(nrows):
    path = kagglehub.dataset_download("forgemaster/steam-reviews-dataset")
    file_path = os.path.join(path, "reviews-11265-13495.csv")
    df = pd.read_csv(file_path, encoding="latin-1", engine="python", on_bad_lines="skip", nrows=nrows)
    return df


raw_data = load_data(50000)

print(raw_data.head())




