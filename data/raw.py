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

# Feature engineering

def feature_engineering(df):
    df = df.copy()

    #df["review_length_chars"] = df["review"].astype(str).str.len()
    #df["review_length_words"] = df["review"].astype(str).str.split().str.len()
    
    if "playtime_forever" in df.columns:
        df["playtime_hours"] = (df["playtime_forever"] / 60).round(2)
        
    if "voted_up" in df.columns and "voted_down" in df.columns:
        df["total_votes"] = df["voted_up"] + df["voted_down"]
        df["helpfulness_ratio"] = df["voted_up"] / df["voted_down"].replace(0, 1)
    
    if "unix_timestamp_created" in df.columns:
        df["review_date"] = pd.to_datetime(df["unix_timestamp_created"], unit="s")
        df["review_year"] = df["review_date"].dt.year
        df["review_month"] = df["review_date"].dt.month
    
    return df





raw_data = load_data(50000)

clean_df = clean_data(raw_data)

final_df = feature_engineering(clean_df)


print("Raw Data:")
print(raw_data.head())

print("Final Data:")
print(final_df.head())




