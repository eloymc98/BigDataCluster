#!/bin/bash

# Start the Airflow container
docker run -d -p 8090:8080 --name airflow -e LOAD_EX=y -v $(pwd)/dags:/opt/airflow/dags -v ~/var/run/docker.sock:/var/run/docker.sock -v $(pwd)/infra/hdfs:/opt/hdfs -v $(pwd)/infra/spark:/opt/spark apache/airflow bash -c "airflow db init && airflow webserver"

# Wait for Airflow to start
sleep 5

# Create an admin user
docker exec airflow airflow users create --username admin --password admin --firstname FIRST_NAME --lastname LAST_NAME --role Admin --email admin@example.org

# Start the Airflow scheduler
docker exec -d airflow airflow scheduler