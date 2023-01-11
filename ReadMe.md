# Data Pipelines with Apache Airflow Project

## Description

Sparkify, A music streaming company, decided to use Apache Airflow to automate and monitor their ETL pipelines. Airflow enriches their ETL given it enables:
* Historical back-filling of data
* Reusable code to replicate, tweak, and apply to similar tasks eliminating verbosity  
* Orchestration monitoring to easily diagnose and debug failed steps of the automated orchestration

Source datasets are available as JSON logs in S3 and this Airflow-enabled ETL loads & processes this data in AWS Redshift.

## Data

### Song Dataset

Here's an example of what a song JSON contains:

```json
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null,
"artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud",
"song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration":
152.92036, "year": 0}
```

### Log Dataset

Here's an example of what a log JSON contains:
![JSON!](./img/log-data.png "JSON-log")

## Project Files

    .
    │    
    ├── dags                            
    │   └── sparkify_dag.py             # Main DAG file with all imports, tasks, operators, and dependencies
    │
    │── plugins                         
    │   └── helpers                     
    │   │   └── sql_queries.py          # SQL syntax for inserting data into created tables
    │   └── operators                   
    │       ├── data_quality.py         # Class object that runs data quality checks 
    │       ├── load_dimension.py       # DAG Operator that loads data into dimension tables
    │       ├── load_fact.py            # DAG Operator that loads data into fact table
    │       └── stage_redshift.py       # Copies data from S3 to Redshift
    │    
    │── create_tables.py                # SQL syntax to create desired tables in Redshift
    │    
    ├── img                             # Images used in this ReadMe.md file
    │   └── ...                         # ...
    │    
    └── ReadMe.md                       # This ReadMe.md file

## DAG Configuration

**Configuration of task dependencies in `sparkify_dag.py`:**
```
start_operator  >> [stage_events_to_redshift, 
                    stage_songs_to_redshift] >> \
load_songplays_table >> [load_user_dimension_table, 
                         load_song_dimension_table, 
                         load_artist_dimension_table, 
                         load_time_dimension_table] >> \
run_data_quality_checks >> end_operator
```

**Graph view of task dependencies**:
![DAG!](./img/sparkify-dag.png "sparkify-dag")

## Airflow Connections

You'll need to add your AWS IAM credentials and Redshift config following these steps in the Airflow UI:

1. Admin tab -> Connections
![admin connections!](./img/airflow-connections.png "admin connections")

2. Connections -> Create -> Insert AWS IAM Credentials
![admin connections!](./img/airflow-connections-IAM.png "admin connections IAM")

3. Connections -> Create -> Insert AWS Redshift Credentials
![admin connections!](./img/airflow-connections-Redshift.png "admin connections Redshift")