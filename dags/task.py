from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
        'etl_task',
        description='DAG that executes the ETL pipeline',
        schedule_interval=None,
        start_date=datetime(2023, 10, 12),  # Adjust the start date
        catchup=False,
) as dag:
    # Define the path to your Docker Compose file
    spark_compose_file = '/spark/spark-compose.yml'
    hdfs_compose_file = '/hdfs/hdfs-compose.yml'

    create_spark_cluster = BashOperator(
        task_id='start_spark_cluster',
        bash_command=f'docker-compose -f {spark_compose_file} up -d',
        dag=dag,
    )

    create_hdfs_cluster = BashOperator(
        task_id='start_hdfs_cluster',
        bash_command=f'docker-compose -f {hdfs_compose_file} up -d',
        dag=dag,
    )

    # Set the task dependencies
    create_spark_cluster >> create_hdfs_cluster
