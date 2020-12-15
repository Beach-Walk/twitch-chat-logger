import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def create_channel_table(channelString, query):

    create_channel_table = """
        CREATE TABLE IF NOT EXISTS channel (
          id TEXT PRIMARY KEY,  
          comments TEXT NOT NULL,  
        );
        """
    return create_channel_table

def create_username_insert_string(messageClasses):
    insert_user_name_string = """
        INSERT INTO
        users (user_id)
        VALUES
        
        """
    arrayLen = len(messageClasses)
    x = 0
    for messages in messageClasses:

        if ((x + 1) == arrayLen):  # for last username add ; instead of , for the right synthax
            insert_user_name_string = insert_user_name_string + "('" + str(messages.name) + "');"
            x = x + 1
        elif(x<arrayLen):
            insert_user_name_string = insert_user_name_string + "('"+str(messages.name)+"'),"
            x = x + 1
        #print(str(x) +", " +str(arrayLen))
    #print(insert_user_name_string)


    return insert_user_name_string

def create_comments_insert_string(messageClasses, channelName):
    insert_comments_string = """
        INSERT INTO
        comments (comment,channel_id,user_id,comment_date)
        VALUES
                            
        """

    for messages in messageClasses: #FILTER ESCAPE CHARS

        if "'" in messages.message:
            messages.message=messages.message.replace("'"," %APOS ")
		
        if "," in messages.message:
            messages.message=messages.message.replace(","," %COMM ")

    arrayLen = len(messageClasses)
    x = 0
    for messages in messageClasses:

        if ((x + 1) == arrayLen):  # for last username add ; instead of , for the right synthax
            insert_comments_string = insert_comments_string + "('"+str(messages.message)+"','"+str(channelName)+"','"+str(messages.name)+"','"+str(messages.date)+"');"
            x = x + 1
        elif (x < arrayLen):
            insert_comments_string = insert_comments_string + "('"+str(messages.message)+"','"+str(channelName)+"','"+str(messages.name)+"','"+str(messages.date)+"'),"
            x = x + 1
        #print(str(x) + ", " + str(arrayLen))
    #print(insert_comments_string)

    return insert_comments_string
