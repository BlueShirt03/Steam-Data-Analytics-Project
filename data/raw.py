# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import os
import kagglehub
import pandas as pd
import matplotlib.pyplot as plt

# Dataset File Reference
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
    file_path = os.path.join(path, "reviews-1230-2345.csv")
    df = pd.read_csv(file_path, encoding="latin-1", engine="python", on_bad_lines="skip", nrows=nrows)
    return df

# Cleans that data by removing any rows with missing values and duplicates, and also converts the 'review' column to lowercase for consistency.
def clean_data(df):
    df = df.copy()
    df = df.drop_duplicates()
    df = df.dropna(subset=["review"])
    df["review"] = df["review"].str.lower()


    # Convert voted_up from True/False into 1/0 for analysis.
    if "voted_up" in df.columns:
        df["voted_up"] = df["voted_up"].astype(int)
    
    
    # Fill missing vote-related columns with 0 and round values
    vote_cols = ["votes_up", "votes_funny", "weighted_vote_score"]
    for col in vote_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0).round(2)
    
    return df

# Feature engineering
def feature_engineering(df):
    df = df.copy()

    # creates new features based on the length of the review text
    df["review_length_chars"] = df["review"].astype(str).str.len()
    df["review_length_words"] = df["review"].astype(str).str.split().str.len()
    
    #converts playtime from minutes to hours
    if "playtime_forever" in df.columns and "playtime_at_review" in df.columns:
        df["playtime_hours"] = (df["playtime_forever"] / 60).round(2)
        df["playtime_at_review_hours"] = (df["playtime_at_review"] / 60).round(2)
    
    
    # Create vote-related metrics.  
    if "voted_up" in df.columns and "votes_up" in df.columns:
        df["total_votes"] = df["voted_up"] + df["votes_up"]
        df["helpfulness_ratio"] = df["voted_up"] / df["total_votes"].replace(0, 1)
    

    # Convert UNIX timestamp into readable date features.
    if "unix_timestamp_created" in df.columns:
        df["review_date"] =pd.to_datetime(df["unix_timestamp_created"],unit="s")
        df["review_year"] = df["review_date"].dt.year
        df["review_month"] = df["review_date"].dt.month
    
    return df




# Pipeline Execution
raw_df = load_data(nrows=50000)
clean_df = clean_data(raw_df)
final_df = feature_engineering(clean_df)


# Output Preview
print("Raw DataFrame:")
print(raw_df.head())

print("\nCleaned DataFrame:")
print(clean_df.head())

print("\nFinal DataFrame with Engineered Features:")
print(final_df.head())  



