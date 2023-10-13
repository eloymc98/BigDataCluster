FROM hdfs-base
ENV HADOOP_CONF_DIR=/etc/hadoop
COPY run.sh /run.sh
RUN chmod a+x run.sh
CMD ["/bin/bash", "/run.sh"]
ENTRYPOINT ["sh", "-c", "service ssh restart; /hadoop/sbin/start-dfs.sh; sleep infinity"]
