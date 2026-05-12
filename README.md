# Steam-Data-Analytics-Project
This is a project taking data from Kaggle and trying to find out what makes a good steam review.



# How to load a csv file 
1. grab one of the 11 csv files from the list. (this files can be found on the original Kaggle file)
2. Paste the your chosen csv file in to the "file_path" variable.(This was done because if we did all the file at once that would take up a lot of memory)


# load_data function
- This function was the one that gave me the most troubles. I kept getting a buffer overflow error when I was trying to run any of the csv files. I learned that the when the encoder was set to latin-1 that is was able to parse the data. The function also takes in a parameter called "nrows". The reason for that parameter is because I only want to access a certian amount of rows from the chosen csv file. The requirments for this project was to access anywhere between 10,000 to 50,000 rows. This function also uses kagglehub which allows me to access Kaggle resources, which in this case would be the "forgemaster/steam-reviews-dataset". 

# clean_data function 
- In this function we clean any data the would be considered messy. This function takes in a DataFrame as a parameter, one of the first things we do is create a copy of the the DataFrame (I was learning that we so that way we do not affect the original dataset in order to compare different DataFrame). We also drop any duplicates that are any rows from within the dataset. We also remove any missing values from the review column. I also made all the words in the reviews lower case so it make easier to parse the data. I also converted "voted_up" column from a Boolean type into an int type so I can use it later in the feature_engineering() function. This would make the positive reviews set to 1 and negative reviews set to 0. We also fill any missing values in the "votes_up", "votes_funny", and "weighted_vote_score" columns. 


# feature_engineering function
- In this function we add some new columns. The first ones being the review_length_chars and review_length_words. This were created so I can see how long reivews are and it also makes it eaiser to make some comparson that will be explored later in the project. We also created a "playtime_hours" which was done my taking playtime_forever and dividing it by 60 so we can have a better understanding on how long a user has actually played for. We also created a "total_votes" by adding both "voted_up" and "votes_up". We also did a helpfulness_ratio by dividing "voted_up" from "total_votes", this column is set to a 0 to 1 ratio. The final three columnes that where created have to do with time. Those columns being "review_date", "review_year", "review_month". The original "unix_timestamp_created" column was formated in a odd way, so these columns make it easir to see when a review was created.(I was trying to formate the review_date differently, however, I learned that we need unit set to "s", because the way in which the "unix_timestamp_created" column is formated. When I tried to do other dateing formats along with the to_datetime() function I got a lot of different errors.)


# updated feature_engineering function 
- I was looking at some of the other columns and say that there is a column named "playtime_at_review" which tracks how many hours was played when the review was made. So I created a new column called "playtime_at_review_hours" which converts the time into hours so it is easier to read. 


## Question: Does playing more hours make a review longer?
# Tools and Code:
- columns that were used:
    - 'review_length_words' (how long a review is via a word count)
    - 'playtime_at_review_hours' (how many hours the user had playing on the game before review)

- Type of graph and step for code:
    - scatter polt 
    - median lines (two median lines were used for 'review_length_words' and  'playtime_at_review_hours') 
    - nrows was set to 50,000
    - filtered 'playtime_at_review_hours' to hours less than 200 hours

- Code for the graph
    ```python
    raw_df = load_data(nrows=50000)
    clean_df = clean_data(raw_df)
    final_df = feature_engineering(clean_df)

    filtered_df = final_df[
    final_df['playtime_at_review_hours'] < 200
    ]

    plt.figure(figsize=(12,7))
    plt.scatter(filtered_df['review_length_words'], filtered_df['playtime_at_review_hours'], alpha=0.15, s=10)
    plt.axhline(
        y=filtered_df['playtime_at_review_hours'].median(), 
        color='red', 
        linestyle='--', 
        label=f'Median Playtime at Review: {filtered_df["playtime_at_review_hours"].median():.2f} hours'
    )
    plt.axhline(
        y=filtered_df['review_length_words'].median(), 
        color='orange', 
        linestyle='--', 
        label=f'Median Review Length: {filtered_df["review_length_words"].median():.2f} words'
    )
    plt.title('Playtime Hours at Review vs Review Length (Words)')
    plt.xlabel('Review Length (Words)')
    plt.ylabel('Playtime Hours at Review')
    plt.legend()
    plt.show()

    ```
# Results/Insight:
- When first looking at the graph, we can see that the data is heavily skewed to the left.

- The graph also shows that there is a dense concentration of points near the lower left. This cluster can be seen with players that write about 20 words and have a playtime of about 10 hours.

- We also see that most players leave short reviews. The median review length was 14 words. This means that players will not normally leave a very detailed review.

- We also see that most players do not play the game for very long before they create the review. The median hours was about 10 hours. This could be caused by factors such as the type of game or how interesting and engaging the game was within the first ten hours.

- There were some extreme outliers, such as some people playing the game for 500+ hours and only writing a review that was 10–14 words long, while other people played for only 1–2 hours and wrote reviews that were 1,000+ words long. That is why the playtime hours were filtered to 200 hours or less.

- Through this graph, we can see that there is a very weak relationship between playtime and review length. This means that increased playtime does not necessarily result in a longer review. 

## Question: Does the length of a review make it a helpful review?
# Tools and Code
- columns that were used:
    - 'review_length_words' (how long a review is via a word count)
    - 'votes_up' (how many people found the vote helpful)

- Type of graph and step for code:
    - scatter polt 
    - nrows was set to 50,000
    - filtered 'review_length_words' was set to 500 or less. (this was because most review past this lenght begin to spread out farther.)
    - filtered 'votes_up' to was set to 100 or less. (most reviews for not get pass 100 up votes)
    - filtered 'votes_up' to drop any reviews that had 0 up votes. (the 0s was removed from the graph because it would make it harder to see a pattern.)

- Code for graph
    ```python
    raw_df = load_data(nrows=50000)
    clean_df = clean_data(raw_df)
    final_df = feature_engineering(clean_df)

    filtered_df = final_df[(final_df['votes_up'] < 100) & (final_df['review_length_words'] < 500) & (final_df['votes_up'] != 0)]


    plt.figure(figsize=(12,7))
    plt.scatter(filtered_df['votes_up'], filtered_df['review_length_words'], alpha=0.15, s=10)
    plt.title('Votes Up vs Review Length (Words)')
    plt.xlabel('Votes Up')
    plt.ylabel('Review Length (Words)')
    plt.show()
    ```
# Results/Insight:
- We can see in this graph that the data is heavily left skewed.

- The graph shows that there is a heavy concentration in the lower-left section of the graph. This cluster stays anywhere between 1–5 votes. After the graph passes 10 votes, the data becomes more inconsistent and spread out.

- Most reviews get 1–5 votes regardless of how long or detailed the review is. This means that most reviews receive very little engagement regardless of review size.

- I did notice that when the number of votes increases, more medium-to-long reviews become more apparent. This is because the graph becomes easier to read as the data becomes less concentrated compared to the lower vote ranges.

- I also noticed that review length is not the only factor that makes a review useful. We can see this with some of the outliers, one of those being a review that is only 14 words long but received 59 up votes.

- Upon further investigation of the review, I noticed that it was full of profanity and mocked the company Rockstar, which is a gaming company that created games such as GTA 5 and Red Dead Redemption.
This means that other factors such as timing, game popularity, humor, and emotional response likely influence what is considered to be a helpful review.

- Through this graph, we can see that there is not a very strong relationship between the length of a review and how many up votes that review received. However, there does appear to be a stronger relationship between these two factors compared to the previous graph involving playtime and review length.

