import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import array_contains


def random_text_classifier(input_loc, output_loc):
    """
    This is a dummy function to show how to use spark, It is supposed to mock
    the following steps
        1. clean input data
        2. use a pre-trained model to make prediction
        3. write predictions to a HDFS output

    Since this is meant as an example, we are going to skip building a model,
    instead we are naively going to mark reviews having the text "good" as positive and
    the rest as negative
    """

    # read input
    df_raw = spark.read.option("header", True).csv(input_loc)

    # parquet is a popular column storage format, we use it here
    df_out.write.mode("overwrite").parquet(output_loc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="HDFS input")
    parser.add_argument("--output", type=str, help="HDFS output")
    args = parser.parse_args()
    spark = SparkSession.builder.appName("ETL Task").getOrCreate()
    random_text_classifier(input_loc=args.input, output_loc=args.output)
