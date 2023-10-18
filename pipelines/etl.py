from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, when, concat_ws, lit
import json


class ETL:
    def __init__(self, spark, metadata):
        self.spark = spark
        self.metadata = metadata

    def validate_fields(self, df, validations):
        # By default all rows are valid
        df = df.withColumn("failed_validations", lit(""))

        for validation in validations:
            field = validation["field"]
            field_validations = validation["validations"]
            if "notEmpty" in field_validations:
                df = df.withColumn(
                    "failed_validations",
                    when((col(field) != "") & col(field).isNotNull(), col("failed_validations")).otherwise(
                        concat_ws(",", col("failed_validations"), lit(f"notEmpty validation failed for {field}"))
                    )
                )

            if "notNull" in field_validations:
                df = df.withColumn(
                    "failed_validations",
                    when(col(field).isNotNull(), col("failed_validations")).otherwise(
                        concat_ws(",", col("failed_validations"), lit(f"notNull validation failed for {field}"))
                    )
                )

        df.cache()
        valid_df = df.filter(col("failed_validations") == "").drop("failed_validations")
        invalid_df = df.filter(col("failed_validations") != "")
        return {'ok': valid_df, 'ko': invalid_df}

    def add_fields(self, df, fields):
        for field in fields:
            field_name = field["name"]
            field_function = field["function"]

            if field_function == "current_timestamp":
                df = df.withColumn(field_name, current_timestamp())

        return df

    def run(self):
        # Iterate over dataflows
        for dataflow in self.metadata["dataflows"]:

            # Read sources
            sources = dataflow["sources"]
            inputs = dict()
            for source in sources:
                source_name = source["name"]
                path = source["path"]
                format_type = source["format"]
                df = self.spark.read.format(format_type).load(path)
                inputs[source_name] = df

            # Apply transformations
            transformations = dataflow["transformations"]
            for transformation in transformations:
                transformation_type = transformation["type"]
                transformation_name = transformation["name"]
                params = transformation["params"]
                input = params["input"]

                if transformation_type == "validate_fields":
                    validations = params["validations"]
                    validation_result_dfs = self.validate_fields(inputs[input], validations)
                    inputs[f"{transformation_name}_ok"] = validation_result_dfs["ok"]
                    inputs[f"{transformation_name}_ko"] = validation_result_dfs["ko"]

                elif transformation_type == "add_fields":
                    fields = params["addFields"]
                    df = self.add_fields(inputs[input], fields)
                    inputs[transformation_name] = df

            # Write data to sinks
            sinks = dataflow["sinks"]
            for sink in sinks:
                input = sink["input"]
                sink_name = sink["name"]
                format_type = sink["format"]
                df = inputs[input]

                if format_type == "KAFKA":
                    # # Write to Kafka topic
                    # topic = sink["topics"][0]
                    # input_df.write.format("kafka").option("kafka.bootstrap.servers", "kafka_broker").option("topic",
                    #                                                                                         topic).save()
                    pass
                elif format_type == "JSON":
                    save_mode = sink["saveMode"]
                    paths = sink["paths"]
                    for path in paths:
                        df.write.format("json").mode(save_mode).save(path)


if __name__ == "__main__":
    metadata_filepath = "/Users/eloymc/Documents/BigDataEngProject/data/metadata.json"
    with open(metadata_filepath, "r") as json_file:
        metadata = json.load(json_file)

    spark = SparkSession.builder.appName("SparkPipeline").getOrCreate()
    ETL(
        spark=spark,
        metadata=metadata
    ).run()
    spark.stop()
