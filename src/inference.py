import os
import sys
import json
import shutil
import logging
from dotenv import load_dotenv
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StandardScaler
from pyspark.ml.classification import RandomForestClassificationModel

from constants import BUCKET_NAME, TEMP_MODEL_PATH, PREDICTION_TABLE
from utils import get_file_from_S3, get_spark, download, store_prediction

load_dotenv()

hdfs_file_path = os.environ['HDFS_FILE_PATH']


def preprocess(object_key):
    logging.info("Started running pipeline for data pre-processing.")

    # Read file from S3 foe new batch prediction
    df = get_file_from_S3(BUCKET_NAME, object_key)
    
    spark = get_spark()

    spark_df = spark.createDataFrame(df)

    # Remove duplicates
    spark_df = spark_df.distinct()

    # Create feature column
    numericCols = ['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
       'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20',
       'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount']
    assembler = VectorAssembler(inputCols=numericCols, outputCol="features")
    spark_df = assembler.transform(spark_df).select('features', 'Class', 'Amount') 

    # Standardize input feature vector
    scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures",
                        withStd=True, withMean=False)

    # Compute summary statistics by fitting the StandardScaler
    scalerModel = scaler.fit(spark_df)

    # Normalize each feature to have unit standard deviation.
    spark_df = scalerModel.transform(spark_df)

    logging.info("Completed running pipeline for data pre-processing.")

    return spark_df
   
if __name__ == "__main__":
    s3_model_path = sys.argv[2]
    test_file_path = sys.argv[1]

    df = preprocess(test_file_path)

    download(BUCKET_NAME, s3_model_path, TEMP_MODEL_PATH)
    model = RandomForestClassificationModel.load(TEMP_MODEL_PATH)

    predictions = model.transform(df)

    shutil.rmtree(TEMP_MODEL_PATH)

    logging.info("Completed batch prediction for file {0}".format(test_file_path))
