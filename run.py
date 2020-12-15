from selenium import webdriver;
from selenium.webdriver.chrome.options import Options
import time;
import re;
import datetime;
import random;
import urllib;
import os;
import urllib.request
import sys;
from bs4 import BeautifulSoup;
import sqlite3
from sqlite3 import Error
import sql;

class messageClass():
    def __init__(self,uName,message,inDate,inPrinted):
        self.name=uName
        self.message=message
        self.printed=inPrinted
        self.date=inDate

menu=True
try:

    while menu is True:
        chrome_path =r"drivers\chrome\chromedriver.exe" #driver needs to be the same version as your chrome version
        options = Options()
        options.headless=True
        driver = webdriver.Chrome(chrome_path,chrome_options=options)
        chatLink = input("Enter a Twitch Popout url...\n")
        #chatLink = r"https://www.twitch.tv/popout/xqcow/chat?popout="#input("Enter a Twitch Chat url...\n")
        driver.get(chatLink)
        print("Opening: ",chatLink," ...")

        chatSearch = True
        messageClasses = []
        matchedClasses = [] #

        sqlPath= "database.sqlite"





        channelName=input("enter a channel name \n")

        sqlConnection = sql.create_connection(sqlPath) # create/ connect to database file, assign file to a var

        create_channels_table = """
             CREATE TABLE IF NOT EXISTS channels (
               id TEXT PRIMARY KEY
             );
             """

        create_users_table = """
             CREATE TABLE IF NOT EXISTS users (
               user_id TEXT PRIMARY KEY  
             );
             """

        create_comments_table = """
             CREATE TABLE IF NOT EXISTS comments (
               comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
               comment TEXT NOT NULL,
               channel_id TEXT,
               user_id TEXT,
               FOREIGN KEY (user_id) REFERENCES users (user_id)
               FOREIGN KEY (channel_id) REFERENCES channels (id)
               comment_date timestamp
             );
             """

        sql.execute_query(sqlConnection, create_comments_table)
        sql.execute_query(sqlConnection, create_channels_table)
        sql.execute_query(sqlConnection, create_users_table)

        insert_channel_name = """
            INSERT INTO
                channels (id)
                VALUES
                ('"""+str(channelName)+"""')
                """

        sql.execute_query(sqlConnection, insert_channel_name)

        print("Searching chat, press CTRL+C ONCE at any time to exit...")

        while chatSearch is True:
            time.sleep(1)
            if(len(messageClasses)>=700):

                insert_user_name = sql.create_username_insert_string(messageClasses)#create insert string for usernames

                sql.execute_query(sqlConnection, insert_user_name)

                insert_comments = sql.create_comments_insert_string(messageClasses,channelName)#create insert string for comments

                sql.execute_query(sqlConnection, insert_comments)


                print("******FLUSH******"+str(len(messageClasses)))
                messageClasses.clear()
                print("******FLUSH******"+str(len(messageClasses)))

            htmlSource = driver.page_source  # get html code from selenium loaded site

            soup = BeautifulSoup(htmlSource, "html.parser")  # input html code from selenium to beautiful soup

            parsedMessages = soup.find_all("div", class_="chat-line__message")

            parsedUsernames = soup.find_all("div", class_="chat-line__message")

            for messages in parsedMessages:

                if  messages.find("span", class_="chat-author__display-name") is not None:
                    username = messages.find("span", class_="chat-author__display-name").text
                    if messages.find("span", class_="text-fragment") is not None:
                        message = messages.find("span", class_="text-fragment").text
                        m = messageClass(username,message,datetime.datetime.now(),False)#the parsed out message. put it into a class
                        skip=False
                        for dupCheck in messageClasses:#check for duplicates in current array
                            if(dupCheck.name==m.name and dupCheck.message==m.message):
                                skip=True
                        if skip==False:#if there are no duplicates of this message, add it to the array
                            messageClasses.append(m)


except KeyboardInterrupt:
    print("Cleaning up, please wait...")
    driver.quit()
    sys.exit()
