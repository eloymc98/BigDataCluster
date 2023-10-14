from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
        'etl_task',
        description='DAG that executes the ETL pipeline',
        schedule_interval=None,
        start_date=datetime(2023, 10, 12),
        catchup=False,
) as dag:
    create_spark_cluster = BashOperator(
        task_id='create_spark_cluster',
        bash_command='/opt/airflow/utils/execute-ssh-cmd.sh "{{ var.value.host }}" "{{ var.value.password }}" "{{ var.value.project_dir }}" start-spark',
        dag=dag,
    )

    create_hdfs_cluster = BashOperator(
        task_id='create_hdfs_cluster',
        bash_command='/opt/airflow/utils/execute-ssh-cmd.sh "{{ var.value.host }}" "{{ var.value.password }}" "{{ var.value.project_dir }}" start-hdfs',
        dag=dag,
    )

    create_kafka_cluster = BashOperator(
        task_id='create_kafka_cluster',
        bash_command='/opt/airflow/utils/execute-ssh-cmd.sh "{{ var.value.host }}" "{{ var.value.password }}" "{{ var.value.project_dir }}" start-kafka',
        dag=dag,
    )

    # Set the task dependencies
    create_spark_cluster >> create_hdfs_cluster >> create_kafka_cluster
