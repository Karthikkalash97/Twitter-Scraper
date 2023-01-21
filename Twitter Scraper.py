#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Importing Required Modules
import snscrape.modules.twitter as sntwitter
import pandas as pd
from pymongo import MongoClient
import datetime
import streamlit as st
import base64
import openpyxl

# Function to search and scrape tweets using Username
def id_search(user,tweet_count): 
    id = f'from:{user}' 
    #Creating list to append tweet data to
    tweets_list1 = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(id).get_items()): #Using TwitterSearchScraper to scrape data and append tweets to list
        if i > tweet_count:
            break
        tweets_list1.append(
            [tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount,
             tweet.lang, tweet.source, tweet.likeCount])
        
        #Creating a dataframe from tweets list above
        tweets_df1 = pd.DataFrame(tweets_list1,
                                  columns=['Datetime', 'Tweet Id', 'URL', 'Text', 'Username', 'Reply Count',
                                           'Retweet Count', 'Language', 'Source', 'Likes'])

    if tweets_list1 == []:
        return "Sorry"
    else:
        return tweets_df1

# Function to search and scrape tweets using Keyword Or Phrase
def keyword_search(user,tweet_count):
    # Creating list to append tweet data to
    tweets_list2 = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(user).get_items()):
        if i > tweet_count:
            break
        tweets_list2.append(
            [tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount,
             tweet.lang, tweet.source, tweet.likeCount])

    # Creating a dataframe from the tweets list above
    tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'URL', 'Text', 'Username', 'Reply Count',
                                                     'Retweet Count', 'Language', 'Source', 'Likes'])
    if tweets_list2 == []:
        return "Sorry"
    else:
        return tweets_df2

#Function to store dataframe as MongoDb collection when searching with Username
def MongoDb_Store_username(col_name, user,tweet_count):
   
    df1 = id_search(user,tweet_count)
    client = MongoClient('mongodb://localhost:27017/')

    db = client['Twitter_Username_Webscraping']
    collection = db[f'{col_name}']

    collection.insert_many(df1.to_dict(orient='records'))


#Function to store dataframe as MongoDb collection when searching with Keyword or Phrase
def MongoDb_Store_Keyword(col_name, user,tweet_count):
    df1 = keyword_search(user,tweet_count)
    client = MongoClient('mongodb://localhost:27017/')

    db = client['Twitter_Keyword_Webscraping']
    collection = db[f'{col_name}']

    collection.insert_many(df1.to_dict(orient='records'))

#Function to return MongoDb collection name(within the naming convention) using username/keyword , start date and end date
def collection_name(name, s_date, e_date):
    if "@" in name:
        name = name.replace('@', "")
        user = name.replace(' ', '')
    else:
        user = name.replace(' ', '')

    s, e = '', ''
    for i in s_date:
        if i.isdigit():
            s = s + str(i)

    for j in e_date:
        if j.isdigit():
            e = e + str(j)
    query = str(f'{user} since:{s_date} until:{e_date}')
    col_name = str(f'{user}_between_{s}__{e}')
    var = [col_name, query]
    return var

#Function to run GUI using Streamlit
def streamlit():
    st.set_page_config(page_title="Twitter Scraper", page_icon=":guardsman:", layout="wide")
    st.title("Twitter Scraper")
    #Recieve User Input
    name = st.text_input("Enter Username Or Keyword:") #Username / Keyword Input
    s_date = st.date_input("Enter start date (YYYY-MM-DD):") #Input start date to search tweets from
    e_date = st.date_input("Enter end date (YYYY-MM-DD):") #Input end date to search for tweets
    tweet_count = st.slider("Select number of tweets to scrape:", min_value=1, max_value=100, value=20) #Innput number of tweets to be retrieved
    
    file_name = str(f'{name}_From:{s_date}_Till:{e_date}')
    
    #Selecting if the user wants to search using username / keyword

    search_type = st.radio("Search by:", ("Username", "Keyword"))
    if search_type == "Username":
        user = collection_name(name, str(s_date), str(e_date))[1]
        tweets_df = id_search(user,tweet_count)
        if st.button("Scrape"):
            if type(tweets_df) == str:
                st.error("Please check the username again")
            else:
                st.dataframe(tweets_df)

    if search_type == "Keyword":
        user = collection_name(name, str(s_date), str(e_date))[1]
        tweets_df = keyword_search(user,tweet_count)
        if st.button("Scrape"):
            if type(tweets_df) == str:
                st.error("Please check the Keyword again")
            else:
                st.dataframe(tweets_df)
                
    #Storing Datadrame In MongoDb

    if st.button("Store data in MongoDB"):
        col_name = collection_name(name, str(s_date), str(e_date))[0]
        if search_type == 'Username':
            MongoDb_Store_username(col_name, user,tweet_count)
            st.success("Data stored in MongoDB!")
            
        if search_type == 'Keyword':
            MongoDb_Store_Keyword(col_name, user,tweet_count)
            st.success("Data stored in MongoDB!")
    
    #Downloading DataFrame as CSV
    if st.button("Download data as CSV"):
        csv = tweets_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download={file_name}.csv>Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("Data Exported to CSV!")

    #Downloading DataFrame as Excel File
    if st.button("Download data as Excel"):
        tweets_df = tweets_df.astype(str)
        excel = tweets_df.to_excel(f'{file_name.replace(":","_").replace("@","_")}.xlsx', index=False)
        st.success("Data exported to Excel!")


streamlit()



