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


#
