#!/bin/bash

# Start the Airflow container
docker run -d -p 8090:8080 --name airflow -e LOAD_EX=y -v $(pwd)/dags:/opt/airflow/dags -v $(pwd)/infra/hdfs:/opt/airflow/hdfs -v $(pwd)/infra/spark:/opt/airflow/spark -v $(pwd)/infra/kafka:/opt/airflow/kafka -v $(pwd)/infra/utils:/opt/airflow/utils apache/airflow bash -c "airflow db init && airflow webserver"
docker exec airflow chmod +x /opt/airflow/utils/execute-ssh-cmd.sh

# Wait for Airflow to start
sleep 5

# Install expect
docker exec -u root airflow sudo apt-get update -y
docker exec -u root airflow sudo apt-get install -y expect

# Create an admin user
docker exec airflow airflow users create --username admin --password admin --firstname FIRST_NAME --lastname LAST_NAME --role Admin --email admin@example.org

# Start the Airflow scheduler
docker exec -d airflow airflow scheduler
