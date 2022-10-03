from msilib.schema import Directory
import sqlite3
import pandas as pd
import os

def convertToBinaryData(filename):
      
    # Convert binary format to images 
    # or files data
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def insertBLOB(name, photo):
    try:
          
        # Using connect method for establishing
        # a connection
        sqliteConnection = sqlite3.connect('Capstone_Project')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
          
        # insert query
        sqlite_insert_blob_query = """ INSERT INTO Traductor
                                  (Palabra, Imagen) VALUES (?, ?)"""
          
        # Converting human readable file into 
        # binary data
        empPhoto = convertToBinaryData(photo)
          
        # Convert data into tuple format
        data_tuple = (name, empPhoto)
          
        # using cursor object executing our query
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()
  
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


conn = sqlite3.connect('Capstone_Project') 
c = conn.cursor()


c.execute('''
           CREATE TABLE IF NOT EXISTS Traductor
           ([ID] INTEGER PRIMARY KEY AUTOINCREMENT, [Palabra] TEXT, [Imagen] BLOB)
           ''')

directory = "Pictures"

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        insertBLOB(filename.split(".")[0], f)

c.execute('''
        SELECT *
        FROM Traductor
        ''')


df = pd.DataFrame(c.fetchall(), columns=['ID','Palabra','Imagen'])
print(df)
#print(df[df.Palabra.str.contains("yo")].Imagen[0])


