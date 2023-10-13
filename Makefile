# All
start-all:
	start-hdfs
	start-spark
stop-all:
	stop-hdfs
	stop-spark

# Airflow
start-airflow:
	./infra/airflow/start-airflow.sh
stop-airflow:
	./infra/airflow/stop-airflow.sh

# HDFS
start-hdfs:
	docker-compose -f ./infra/hdfs/hdfs-compose.yml up -d
stop-hdfs:
	docker-compose -f ./infra/hdfs/hdfs-compose.yml down

# Spark
start-spark:
	docker-compose -f ./infra/spark/spark-compose.yml up -d
stop-spark:
	docker-compose -f ./infra/spark/spark-compose.yml down