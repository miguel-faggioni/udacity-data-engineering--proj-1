import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):
    """
    - Reads the file received in the parameters
    - Extracts the wanted fields from the json
    - Inserts both song and artist data into the database using SQL query defined in sql_queries.py
    """
    # open song file
    df = pd.read_json(filepath, typ='series')

    # insert song record
    song_data = list(df[['song_id','title','artist_id','year','duration']].values)
    try:
        cur.execute(song_table_insert, song_data)
    except psycopg2.Error as e:
        print("Error inserting into songs table")
        print(e)
    
    # insert artist record
    artist_data = list(df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values)
    try:
        cur.execute(artist_table_insert, artist_data)
    except psycopg2.Error as e:
        print("Error inserting into artists table")
        print(e)


def process_log_file(cur, filepath):
    """
    - Reads the file received in the parameters
    - Filters the data to account only for NextSong page hits
    - Converts the timestamp into datetime format and extracts the wanted pieces from it
    - Inserts the data into the timestamps and user tables
    - Searches the song table to get the correct song and artist id
    - Inserts the data into the songplays table
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action (page)
    df = df[ df.page == 'NextSong' ]

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'],unit='ms')
    t = df.ts
    
    # insert time data records
    time_data = [
        t,
        pd.Series(t.dt.hour,name='hour'),
        pd.Series(t.dt.day,name='day'),
        pd.Series(t.dt.isocalendar().week,name='week'),
        pd.Series(t.dt.month,name='month'),
        pd.Series(t.dt.year,name='year'),
        pd.Series(t.dt.dayofweek,name='weekday')
    ]
    time_df = pd.concat(time_data, axis=1)

    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except psycopg2.Error as e:
            print("Error inserting into timestamps table")
            print(e)

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        try:
            cur.execute(user_table_insert, row)
        except psycopg2.Error as e:
            print("Error inserting into users table")
            print(e)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        try:
            cur.execute(song_select, (row.song, row.artist, row.length))
        except psycopg2.Error as e:
            print("Error selecting from songs table")
            print(e)
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [
            row.ts,
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent
        ]
        try:
            cur.execute(songplay_table_insert, songplay_data)
        except psycopg2.Error as e:
            print("Error inserting into songplays table")
            print(e)


def process_data(cur, conn, filepath, func):
    """
    - Gets all the json files insite the filepath received in the parameters
    - Calls the function received in the parameters passing each json file found
    - Prints the process to the console
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Connects to the Postgres instance running on localhost 
    - Accesses the sparkifydb database
    - Processes the song and log data json files for database insertion
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
