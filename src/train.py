
import os
import sys
import logging
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from dotenv import load_dotenv

from utils import get_spark

load_dotenv()

def train_model(df):
    train, test = df.randomSplit([0.7, 0.3], seed = 2018)

    rf_clf = RandomForestClassifier(featuresCol = 'scaledFeatures', labelCol = 'Class')
    rfModel = rf_clf.fit(train)

    predictions = rfModel.transform(test)

    evaluator = MulticlassClassificationEvaluator(labelCol="Class", predictionCol="prediction")

    accuracy = evaluator.evaluate(predictions)

    logging.info("Training of Model completed. Overal accuracy is {0}".format(accuracy))

    print(accuracy)

    rfModel.save("model")
    
    return accuracy

def main():
    spark = get_spark()

    preprocessed_df = spark.read.parquet(os.path.join(os.environ["HDFS_FILE_PATH"],sys.argv[1]))
    train_model(preprocessed_df)

main()
