# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import os
import kagglehub
import pandas as pd
import matplotlib.pyplot as plt

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
    file_path = os.path.join(path, "reviews-1230-2345.csv")
    df = pd.read_csv(file_path, encoding="latin-1", engine="python", on_bad_lines="skip", nrows=nrows)
    return df

# Cleans that data by removing any rows with missing values and duplicates, and also converts the 'review' column to lowercase for consistency.
def clean_data(df):
    df = df.copy()
    df = df.drop_duplicates()
    df = df.dropna(subset=["review"])
    df["review"] = df["review"].str.lower()

    if "voted_up" in df.columns:
        df["voted_up"] = df["voted_up"].astype(int)
    
    
    vote_cols = ["votes_up", "votes_funny", "weighted_vote_score"]
    for col in vote_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0).round(2)
    
    return df

# Feature engineering

def feature_engineering(df):
    df = df.copy()

    df["review_length_chars"] = df["review"].astype(str).str.len()
    df["review_length_words"] = df["review"].astype(str).str.split().str.len()
    
    if "playtime_forever" in df.columns and "playtime_at_review" in df.columns:
        df["playtime_hours"] = (df["playtime_forever"] / 60).round(2)
        df["playtime_at_review_hours"] = (df["playtime_at_review"] / 60).round(2)
    
    
        
    if "voted_up" in df.columns and "votes_up" in df.columns:
        df["total_votes"] = df["voted_up"] + df["votes_up"]
        df["helpfulness_ratio"] = df["voted_up"] / df["total_votes"].replace(0, 1)
    
    if "unix_timestamp_created" in df.columns:
        df["review_date"] =pd.to_datetime(df["unix_timestamp_created"],unit="s")
        df["review_year"] = df["review_date"].dt.year
        df["review_month"] = df["review_date"].dt.month
    
    return df





raw_df = load_data(nrows=50000)

clean_df = clean_data(raw_df)

final_df = feature_engineering(clean_df)

#print("Raw DataFrame: for playtime_at_review")
#print(raw_df.head()['playtime_at_review'])

#print("\nFinal DataFrame: for playtime_at_review_hours")
#print(final_df.head()['playtime_at_review_hours'])



#print("Raw DataFrame:")
#print(raw_df.info())


#print("Final DataFrame:")
#print(final_df.info())





print("\nSummary Statistics for votes_up:")
print(final_df[['votes_up', 'review_length_words']].corr())





filtered_df = final_df[(final_df['votes_up'] < 100) & (final_df['review_length_words'] < 500) & (final_df['votes_up'] != 0)]
plt.figure(figsize=(12,7))
plt.scatter(filtered_df['votes_up'], filtered_df['review_length_words'], alpha=0.15, s=10)

plt.title('Votes Up vs Review Length (Words)')
plt.xlabel('Votes Up')
plt.ylabel('Review Length (Words)')
plt.show()



