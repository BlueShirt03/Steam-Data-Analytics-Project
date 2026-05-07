# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import os

import kagglehub
from kagglehub import KaggleDatasetAdapter
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

# Set the path to the file you'd like to load
path = kagglehub.dataset_download("forgemaster/steam-reviews-dataset")

file_path = os.path.join(path, "reviews-11265-13495.csv")


df = pd.read_csv(file_path, encoding="latin-1", engine="python", on_bad_lines="skip", nrows=10000)


df = df.drop_duplicates()


df.columns = df.columns.str.strip()


df = df.fillna("Unknown")

print(df.info())




