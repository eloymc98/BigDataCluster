build-images:
	docker build -t hdfs-base:latest ./infra/hdfs/base
	docker build -t hdfs-namenode:latest ./infra/hdfs/namenode
start:
	docker-compose up
stop:
	docker-compose down
