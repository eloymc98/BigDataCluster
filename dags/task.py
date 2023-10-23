import json
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from hdfs import InsecureClient

with DAG(
        'etl_task',
        description='DAG that executes the ETL pipeline',
        schedule_interval=None,
        start_date=datetime(2023, 10, 12),
        catchup=False,
) as dag:
    metadata_filepath = "/opt/airflow/data/metadata.json"
    with open(metadata_filepath, "r") as json_file:
        metadata = json.load(json_file)

    def hdfs_upload():
        client = InsecureClient('http://namenode:9870')
        client.upload('/data/input/events/person', '/opt/airflow/data/input/events/person/input-data.json',
                      overwrite=True)
        client.upload('/data', '/opt/airflow/data/metadata.json',
                      overwrite=True)


    create_spark_cluster = EmptyOperator(
        task_id='create_spark_cluster',
    )

    create_hdfs_cluster = EmptyOperator(
        task_id='create_hdfs_cluster',
    )

    create_kafka_cluster = EmptyOperator(
        task_id='create_kafka_cluster',
    )

    upload_to_hdfs = PythonOperator(
        task_id='upload_to_hdfs',
        python_callable=hdfs_upload
    )

    spark_job = SparkSubmitOperator(
        task_id='run_etl',
        conn_id='spark_default',
        application="/opt/airflow/dags/pipelines/etl.py",
        application_args=["--metadata", json.dumps(metadata)],
    )

    # Set the task dependencies
    [create_hdfs_cluster, create_spark_cluster, create_kafka_cluster] >> upload_to_hdfs >> spark_job
