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

# Load the dataset and is able to input the number of rows you want.
def load_data(nrows):
    path = kagglehub.dataset_download("forgemaster/steam-reviews-dataset")
    file_path = os.path.join(path, "reviews-11265-13495.csv")
    df = pd.read_csv(file_path, encoding="latin-1", engine="python", on_bad_lines="skip", nrows=nrows)
    return df

# Cleans that data by removing any rows with missing values and duplicates, and also converts the 'review' column to lowercase for consistency.

def clean_data(df):
    df = df.copy()
    df = df.drop_duplicates()
    df = df.dropna(subset=["review"])
    df["review"] = df["review"].str.lower()

    
    return df

      




raw_data = load_data(50000)

clean_df = clean_data(raw_data)


print(raw_data.shape)

print(clean_df.shape)





