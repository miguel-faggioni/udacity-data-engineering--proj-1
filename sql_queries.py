# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE ENUM TYPES

user_gender_enum_create = ("""
CREATE TYPE user_gender AS ENUM (
    'M',
    'F',
    'Other'
);
""")

user_level_enum_create = ("""
CREATE TYPE user_level AS ENUM (
    'free',
    'paid'
);
""")

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id   SERIAL                    PRIMARY KEY,
    start_time    timestamp                 NOT NULL,
    user_id       int                       NOT NULL,
    level         text                      NOT NULL,
    song_id       text                      ,
    artist_id     text                      ,
    session_id    int                       NOT NULL,
    location      text                      ,
    user_agent    text                      
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id       int                       PRIMARY KEY,
    first_name    text                      ,
    last_name     text                      ,
    gender        user_gender               ,
    level         text                      
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id       text                      PRIMARY KEY,
    title         text                      ,
    artist_id     text                      NOT NULL,
    year          int                       ,
    duration      decimal                   
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id     text                      PRIMARY KEY,
    name          text                      NOT NULL,
    location      text                      ,
    latitude      numeric(9,6)              ,
    longitude     numeric(9,6)              
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time    timestamp                 PRIMARY KEY,
    hour          int                       NOT NULL,
    day           int                       NOT NULL,
    week          int                       NOT NULL,
    month         int                       NOT NULL,
    year          int                       NOT NULL,
    weekday       int                       NOT NULL
);
""")

# CREATE FOREIGN KEY CONTRAINTS

foreign_key_constraints_create = ("""
ALTER TABLE songplays ADD CONSTRAINT FK_USERS FOREIGN KEY(user_id) REFERENCES users(user_id);
ALTER TABLE songplays ADD CONSTRAINT FK_SONGS FOREIGN KEY(song_id) REFERENCES songs(song_id);
ALTER TABLE songplays ADD CONSTRAINT FK_ARTISTS FOREIGN KEY(artist_id) REFERENCES artists(artist_id);
ALTER TABLE songplays ADD CONSTRAINT FK_TIMESTAMPS FOREIGN KEY(start_time) REFERENCES time(start_time);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (start_time,user_id,level,song_id,artist_id,session_id,location,user_agent) 
VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
""")

user_table_insert = ("""
INSERT INTO users (user_id,first_name,last_name,gender,level)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (id)
DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs (song_id,title,artist_id,year,duration)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT(song_id)
DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id,name,location,latitude,longitude)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT(artist_id)
DO NOTHING;
""")

time_table_insert = ("""
INSERT INTO time (start_time,hour,day,week,month,year,weekday)
VALUES (%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT(start_time)
DO NOTHING;
""")

# FIND SONGS

song_select = ("""
SELECT s.song_id, a.artist_id FROM songs s
JOIN artists a on s.artist_id = a.artist_id
WHERE 
    s.title = %s AND
    a.name = %s AND
    s.duration = %s
""")

# QUERY LISTS

create_table_queries = [
    user_gender_enum_create,
    user_level_enum_create,
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
    foreign_key_constraints_create
]
drop_table_queries = [
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop
]
