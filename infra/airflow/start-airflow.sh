#!/bin/bash

# Start the Airflow container
docker run -d -p 8090:8080 --name airflow -e LOAD_EX=y -v $(pwd)/dags:/usr/local/airflow/dags apache/airflow bash -c "airflow db init && airflow webserver"

# Wait for Airflow to start (adjust the sleep time as needed)
sleep 10

# Create an admin user
docker exec airflow airflow users create --username admin --password admin --firstname FIRST_NAME --lastname LAST_NAME --role Admin --email admin@example.org

# Start the Airflow scheduler
docker exec -d airflow airflow scheduler