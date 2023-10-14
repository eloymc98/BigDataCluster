# All
start-all: start-airflow start-hdfs start-spark start-kafka

stop-all: stop-airflow stop-hdfs stop-spark stop-kafka

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

# Kafka
start-kafka:
	docker-compose -f ./infra/kafka/kafka-compose.yml up -d
stop-kafka:
	docker-compose -f ./infra/kafka/kafka-compose.yml down

# Pipe
start-pipe:
	./infra/pipe/start-pipe.sh
stop-pipe:
	./infra/pipe/stop-pipe.sh