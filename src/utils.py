import os
import boto3
import pandas as pd
from dotenv import load_dotenv
from pyspark.sql import SparkSession

load_dotenv()

aws_key = os.environ['AWS_ACCESS_KEY']
aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']
aws_token = os.environ['AWS_SESSION_TOKEN']

def get_file_from_S3(bucket_name, object_key):
    session = boto3.Session(
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        aws_session_token=aws_token
        )
    s3 = session.client('s3')

    s3_object = s3.get_object(Bucket=bucket_name, Key=object_key)
    body = s3_object['Body']
    df = pd.read_csv(body)

    return df


def get_spark():
    spark = SparkSession.builder.master("local[1]").appName("fraud_detection.com").getOrCreate()
    return spark
