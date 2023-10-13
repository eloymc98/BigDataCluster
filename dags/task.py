from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
        'start_spark_cluster',
        description='Start Spark Cluster using Docker Compose',
        schedule_interval=None,  # You can set the schedule as needed
        start_date=datetime(2023, 10, 12),  # Adjust the start date
        catchup=False,
) as dag:
    # Define the path to your Docker Compose file
    spark_compose_file = '../infra/spark/spark-compose.yml'
    hdfs_compose_file = '../infra/spark/spark-compose.yml'


    # Define the DockerOperator task
    start_spark_cluster = DockerOperator(
        task_id='start_spark_cluster',
        image='docker',
        api_version='auto',
        auto_remove='success',  # Remove the container when it finishes
        command=f'compose -f {spark_compose_file} up -d',
        network_mode='bridge',  # You can specify the network mode as needed
        dag=dag,
    )

    # Define the DockerOperator task
    start_hdfs_cluster = DockerOperator(
        task_id='start_hdfs_cluster',
        image='docker',
        api_version='auto',
        auto_remove='success',  # Remove the container when it finishes
        command=f'compose -f {docker_compose_file} up -d',
        network_mode='bridge',  # You can specify the network mode as needed
        dag=dag,
    )
    # Set the task dependencies
    start_spark_cluster
