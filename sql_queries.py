# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS timestamps;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    id            int                       PRIMARY KEY,
    start_time    timestamp                 NOT NULL,
    user_id       int                       ,
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
    id            int                       PRIMARY KEY,
    first_name    text                      NOT NULL,
    last_name     text                      NOT NULL,
    gender        text                      NOT NULL,
    level         text                      NOT NULL
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    id            text                      PRIMARY KEY,
    title         text                      NOT NULL,
    artist_id     text                      NOT NULL,
    year          int                       NOT NULL,
    length        decimal                   NOT NULL
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    id            text                      PRIMARY KEY,
    name          text                      NOT NULL,
    location      text                      NOT NULL,
    latitude      decimal                   ,
    longitude     decimal                   
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS timestamps (
    start_time    timestamp                 PRIMARY KEY,
    hour          int                       NOT NULL,
    day           int                       NOT NULL,
    week          int                       NOT NULL,
    month         int                       NOT NULL,
    year          int                       NOT NULL,
    weekday       int                       NOT NULL
);
""")

foreign_key_constraints = ("""
ALTER TABLE songplays ADD CONSTRAINT FK_USERS FOREIGN KEY(user_id) REFERENCES users(id);
ALTER TABLE songplays ADD CONSTRAINT FK_SONGS FOREIGN KEY(song_id) REFERENCES songs(id);
ALTER TABLE songplays ADD CONSTRAINT FK_ARTISTS FOREIGN KEY(artist_id) REFERENCES artists(id);
ALTER TABLE songplays ADD CONSTRAINT FK_TIMESTAMPS FOREIGN KEY(start_time) REFERENCES timestamps(start_time);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (id,start_time,user_id,level,song_id,artist_id,session_id,location,user_agent) 
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (id)
DO NOTHING;
""")

user_table_insert = ("""
INSERT INTO users (id,first_name,last_name,gender,level)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (id)
DO NOTHING;
""")

song_table_insert = ("""
INSERT INTO songs (id,title,artist_id,year,length)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (id)
DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists (id,name,location,latitude,longitude)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (id)
DO NOTHING;
""")

time_table_insert = ("""
INSERT INTO timestamps (start_time,hour,day,week,month,year,weekday)
VALUES (%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (start_time)
DO NOTHING;
""")

# FIND SONGS

song_select = ("""
SELECT s.id, a.id FROM songs s
JOIN artists a on s.artist_id = a.id
WHERE 
    s.title = %s AND
    a.name = %s AND
    s.length = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, foreign_key_constraints]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
