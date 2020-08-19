- [Data Modeling with Postgres - Udacity](#orgef10cbf)
  - [Introduction](#org0461a83)
  - [Project Description](#orga82479d)
- [Folder structure](#orga1f09a9)
- [Usage](#orgde76376)
  - [Creating the tables](#orgb21f108)
  - [Running the pipeline](#org1415ac6)
- [Motivation](#orgb05d89d)
- [Example queries for analysis](#org08d8dc3)
  - [Average session length](#orge0467aa)
  - [Hour of the day with highest number of songplays](#orge29bb42)


<a id="orgef10cbf"></a>

# Data Modeling with Postgres - Udacity

This repository is intended for the first project of the Udacity Data Engineering Nanodegree Program: Data Modeling with Postgres.

The introduction and project description were taken from the Udacity curriculum, since they summarize the activity better than I could heh.


<a id="org0461a83"></a>

## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.


<a id="orga82479d"></a>

## Project Description

In this project, you'll apply what you've learned on data modeling with Postgres and build an ETL pipeline using Python. To complete the project, you will need to define fact and dimension tables for a star schema for a particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL.


<a id="orga1f09a9"></a>

# Folder structure

```
/
├── create_tables.py - contains code that drops and recreates the database and tables
├── data
│   ├── log_data - contains all the log files pertaining simulated activity from the mock music streaming app
│   │   └── <year>
│   │       └── <month>
│   │           ├── (...)
│   │           └── <year>-<month>-<day>-events.json
│   └── song_data - contains a subset of the Million Song Dataaset
│       └── <first letter of song track ID>
│           └── <second letter of song track ID>
│               └── <third letter of song track ID>
│                   ├── (...)
│                   └── TR<track ID>.json
├── etl.ipynb - jupyter notebook to walk through the necessary steps to fill the missing parts of etl.py
├── etl.py - code to parse the files in data/ and insert them into the database
├── README.md - this file in markdown
├── README.org - this file in orgmode
├── sql_queries.py - file containing the SQL queries to select from, create, and drop the tables needed
└── test.ipynb - jupyter notebook to test the ETL pipeline by selecting the first rows of each table
```


<a id="orgde76376"></a>

# Usage


<a id="orgb21f108"></a>

## Creating the tables

To remove and recreate the tables necessary, run the following command in the terminal at the root of the project.

```bash
python create_tables.py
```

It connects to a Postgre database running on localhost and drops then creates a database named `sparkifydb`; then it executes the queries for dropping and creating the necessary tables for the ETL pipeline.

The core functionality of the file was provided by Udacity, and only the SQL queries needed to drop and create the tables was filled in on the `sql_queries.py` file.


<a id="org1415ac6"></a>

## Running the pipeline

After the tables are created and the log and song files are on the data folder, run the following command in the terminal at the root of the project to parse the files and insert the data in the database

```bash
python etl.py
```


<a id="orgb05d89d"></a>

# Motivation

In order to be able to analyze the songplays of Sparkify as well as user profiles, this project allows for insertion of the log files collected into a Postgres database. This allows better and quicker parsing of the information with SQL queries.

The database is designed using the star schema, with the `users`, `songs`, `artists` tables containing the information of their namesake entities; the `timestamps` table containing the timestamp of the songplays divided into hour, day, week, month, year and weekday (for more granularity during the analysis); and the `songplays` table being the fact table of the start schema, containing foreign keys to the previously described dimension tables, along with the user account type (free or paid), location, and User Agent used for the access.

With this information it is now possible to create queries to better analyze Sparkify's users' usage patterns.


<a id="org08d8dc3"></a>

# Example queries for analysis


<a id="orge0467aa"></a>

## Average session length

Selecting first the first and last start time of each songplay session we can calculate the time difference to get an estimate of each session length. It is only an estimate since we don't have the end time of the session, so this will be a lower bound on each session length.

Then we can select the average of the previous query to get the average session length, in seconds.

```sql
 WITH sessions AS (
     SELECT sp.session_id, 
            min(sp.start_time)::timestamp as min,
            max(sp.start_time)::timestamp as max
     FROM songplays sp
     GROUP BY 1
),
session_length AS (
     SELECT sessions.session_id,
            ((DATE_PART('day', max - min) * 24 +
              DATE_PART('hour', max - min)) * 60 +
              DATE_PART('minute', max - min)) * 60 +
              DATE_PART('second', max - min) as length_in_seconds
     FROM sessions
)
SELECT AVG(length_in_seconds) 
FROM session_length
```


<a id="orge29bb42"></a>

## Hour of the day with highest number of songplays

Joining the timestamps table with with songplays we can get the hour of the day when each songplay recorded occurred; then grouping by the selected column and counting we can know how many songplays occurred on each hour of the day.

By changing the column selected from the timestamps table we can change what information we extract.

```sql
SELECT ts.weekday, COUNT(*)
FROM timestamps ts
JOIN songplays sp
ON ts.start_time = sp.start_time
GROUP BY 1
ORDER BY 2 DESC
```

We can also add a statement to consider only the free users, and get the most effective hours to play adds to try and convert them into paid users, for example.

```sql
SELECT ts.weekday, COUNT(*)
FROM timestamps ts
JOIN songplays sp 
ON ts.start_time = sp.start_time AND
   sp.level = 'free'
GROUP BY 1
ORDER BY 2 DESC   
```