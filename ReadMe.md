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

<p align="left">
  <img src="./img/log-data.png" alt="Statoscope example" width="650">
</p>

## Project Files

This project workspace includes 2 folders: dags, plugins as shown in the following figure:
![Project Explore!](./image/project-explore.PNG "sparkify")

>- The **spakify_dag.py** includes all the imports, tasks and task dependencies <br>
>- The **operators** folder includes 4 user defined operators  that will stage the data, transform the data, fill the data warehouse, and run checks on data quality. <br>
>- A **helper** class for the SQL transformations

## DAG Configuration

**Graph view of task dependencies**:
![DAG!](./image/sparkify-dag.PNG "sparkify-dag")

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

## Building the operators

### Stage Operator
<p>The stage operator is expected to be able to load any JSON formatted files from S3 to Amazon Redshift. The operator creates and runs a SQL COPY statement based on the parameters provided. The operator's parameters should specify where in S3 the file is loaded and what is the target table.</p>

<p>The parameters should be used to distinguish between JSON file. Another important requirement of the stage operator is containing a templated field that allows it to load timestamped files from S3 based on the execution time and run backfills.</p>

### Fact and Dimension Operators
<p>With dimension and fact operators, you can utilize the provided SQL helper class to run data transformations. Most of the logic is within the SQL transformations and the operator is expected to take as input a SQL statement and target database on which to run the query against. You can also define a target table that will contain the results of the transformation.</p>

<p>Dimension loads are often done with the truncate-insert pattern where the target table is emptied before the load. Thus, you could also have a parameter that allows switching between insert modes when loading dimensions. Fact tables are usually so massive that they should only allow append type functionality.</p>

### Data Quality Operator
<p>The final operator to create is the data quality operator, which is used to run checks on the data itself. The operator's main functionality is to receive one or more SQL based test cases along with the expected results and execute the tests. For each the test, the test result and expected result needs to be checked and if there is no match, the operator should raise an exception and the task should retry and fail eventually.</p>

## Airflow Connections

Use Airflow's UI to configure your AWS credentials and connection to Redshift.

1. Click on the Admin tab and select Connections.
![admin connections!](./image/admin-connections.png "admin connections")

2. Under Connections, select Create. <br>
![create connections!](./image/create-connection.png "create connections")

3. On the create connection page, enter the following values:

>- **Conn Id**: Enter aws_credentials.
>- **Conn Type**: Enter Amazon Web Services.
>- **Login**: Enter your Access key ID from the IAM User credentials you downloaded earlier.
>- **Password**: Enter your Secret access key from the IAM User credentials you downloaded earlier.
Once you've entered these values, select Save and Add Another.
![connection-aws-credentials!](./image/connection-aws-credentials.png "connection-aws-credentials")

4. On the next create connection page, enter the following values:

>- **Conn Id**: Enter redshift.
>- **Conn Type**: Enter Postgres.
>- **Host**: Enter the endpoint of your Redshift cluster, excluding the port at the end. You can find this by selecting your cluster in the Clusters page of the Amazon Redshift console. See where this is located in the screenshot below. IMPORTANT: Make sure to NOT include the port at the end of the Redshift endpoint string.
>- **Schema**: Enter dev. This is the Redshift database you want to connect to.
>- **Login**: Enter awsuser.
>- **Password**: Enter the password you created when launching your Redshift cluster.
>- **Port**: Enter **5439**. <br>

![cluster-details!](./image/cluster-details.png "cluster-details")

![connection-redshift!](./image/connection-redshift.png "connection-redshift")