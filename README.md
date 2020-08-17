- [](#org7f81a80)
- [Data Modeling with Postgres - Udacity](#orga9c68e9)
  - [Introduction](#org0857e64)
  - [Project Description](#org28448c7)
- [Folder structure](#org20c1817)
- [Usage](#orgacbd7ef)
  - [Creating the tables](#org507dd46)
  - [Running the pipeline](#org0e88a76)


<a id="org7f81a80"></a>

# TODO 

1.  The README file includes a summary of the project, how to run the Python scripts, and an explanation of the files in the repository. Comments are used effectively and each function has a docstring.
2.  Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.
3.  State and justify your database schema design and ETL pipeline.
4.  [Optional] Provide example queries and results for song play analysis.
5.  Scripts have an intuitive, easy-to-follow structure with code separated into logical functions. Naming for variables and functions follows the PEP8 style guidelines.
6.  Insert data using the COPY command to bulk insert log files instead of using INSERT on one row at a time
7.  Add data quality checks
8.  Create a dashboard for analytic queries on your new database (how?)


<a id="orga9c68e9"></a>

# Data Modeling with Postgres - Udacity

This repository is intended for the first project of the Udacity Data Engineering Nanodegree Program: Data Modeling with Postgres.

The introduction and project description were taken from the Udacity curriculum, since they summarize the activity better than I could heh.


<a id="org0857e64"></a>

## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.


<a id="org28448c7"></a>

## Project Description

In this project, you'll apply what you've learned on data modeling with Postgres and build an ETL pipeline using Python. To complete the project, you will need to define fact and dimension tables for a star schema for a particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL.


<a id="org20c1817"></a>

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


<a id="orgacbd7ef"></a>

# Usage


<a id="org507dd46"></a>

## Creating the tables

To remove and recreate the tables necessary, run the following command in the terminal at the root of the project.

```bash
python create_tables.py
```

It connects to a Postgre database running on localhost and drops then creates a database named `sparkifydb`; then it executes the queries for dropping and creating the necessary tables for the ETL pipeline.

The core functionality of the file was provided by Udacity, and only the SQL queries needed to drop and create the tables was filled in on the `sql_queries.py` file.


<a id="org0e88a76"></a>

## Running the pipeline

After the tables are created and the log and song files are on the data folder, run the following command in the terminal at the root of the project to parse the files and insert the data in the database

```bash
python etl.py
```