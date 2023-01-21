# Twitter Scraper
## Overview

This project is a Twitter scraping tool that allows users to scrape tweets for a specific username or keyword, store the tweets in a MongoDB collection, and export the tweets as a CSV or Excel file. The script uses the snscrape, pandas, and pymongo libraries to scrape the tweets and interact with MongoDB, and the streamlit library to create a graphical user interface (GUI)

## Requirements
1. Python 3.x

2. snscrape

3. pandas

4. pymongo

5. streamlit

6. openpyxl

## Libraries Used
1. snscrape: A Python library for scraping various websites, including Twitter.

2. pandas: A library for data manipulation and analysis. It is used to create the Dataframe of tweets.

3. pymongo: A library for working with MongoDB databases in Python. It is used to store the scraped tweets in a MongoDB collection.

4. datetime: A built-in Python library for working with dates and times.

5. streamlit: A library for creating interactive web apps in Python.

6. base64: A built-in Python library for encoding and decoding binary data in base64 format.

7. openpyxl: A library for working with Excel files in Python.

## Functionalities

1. id_search(user, tweet_count): Search and scrape tweets using a Twitter username. It takes two arguments, user and tweet_count, and returns a Dataframe of tweets.

2. keyword_search(user, tweet_count): Search and scrape tweets using a keyword or phrase. It takes two arguments, user and tweet_count, and returns a Dataframe of tweets.

3. MongoDb_Store_username(col_name, user, tweet_count): Store the Dataframe returned by id_search function as a MongoDB collection with the given collection name. It takes three arguments, col_name, user, and tweet_count.

4. MongoDb_Store_Keyword(col_name, user, tweet_count): Store the Dataframe returned by keyword_search function as a MongoDB collection with the given collection name. It takes three arguments, col_name, user, and tweet_count.

5. collection_name(name, s_date, e_date): Return MongoDb collection name(within the naming convention) using username/keyword, start date and end date.

6. streamlit():The streamlit() function is a function that uses the streamlit library to create an interactive web app for scraping tweets from Twitter. It allows the user to input a Twitter username or keyword to search for tweets, a start and end date to search for tweets within a specific date range, and the number of tweets to scrape. It also gives the user the option to search for tweets by username or keyword.



## Workflow

1.The user enters a username or keyword to search for in the text input field.

2.The user enters a start and end date for the tweets they want to retrieve.

3.The user clicks the "Scrape Tweets" button to start scraping the tweets.

4.The scraped tweets are displayed in a table.

5.The user can choose to export the tweets as a CSV or Excel file by clicking the corresponding button.

6.The tweets are also stored in a MongoDB collection, with the collection name based on the username or keyword and the start and end date.


## Execution
1. Clone or download the repository

2. Install the required libraries by running the following code in command terminal:  pip install -r requirements.txt.

3. Run the script using command terminal and enter: streamlit run twitter_scraper.py.

4. Follow the steps outlined in the "Workflow" section to scrape tweets, export to CSV/Excel and store in MongoDB


## Note
1. Make sure MongoDB is running on your machine and the correct connection string is used in the script.

2. You can also change the number of tweets to be scraped by changing the tweet_count variable

3. You can change the MongoDB host and port by changing the MongoClient('mongodb://localhost:27017/')

4. Please make sure that you comply with Twitter's terms of service when using this script. This includes not using the script to scrape tweets for commercial use or for spamming or harassing users. It's your responsibility to ensure that you comply with Twitter's terms of service when using this script.

## Limitations
1. The script is limited to the number of tweets that can be retrieved using the Twitter API.

2. The script is also limited by the rate limits of the Twitter API.

3. If you have a large amount of tweets to scrape, it is recommended to use the tweet_count parameter to scrape tweets in smaller chunks to avoid hitting the rate limit
