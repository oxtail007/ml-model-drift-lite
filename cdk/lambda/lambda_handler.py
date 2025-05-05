import os
import boto3
import pandas as pd
from mldrift.drift import compute_psi

def handler(event, context):
    s3 = boto3.client('s3')
    bucket = os.environ['BUCKET_NAME']

    train_key = 'train.csv'
    test_key = 'test.csv'

    def read_csv(key):
        obj = s3.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(obj['Body'])

    train = read_csv(train_key)
    test = read_csv(test_key)

    psi_scores = {}
    for col in train.columns:
        if col in test.columns:
            psi_scores[col] = compute_psi(train[col], test[col])

    print("PSI Scores:", psi_scores)
