import boto3
from moto import mock_s3
from . import sys_details


@mock_s3

def test_my_model_save():
    conn = boto3.resource('s3', region_name='us-east-1')
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    conn.create_bucket(Bucket='mybucket-1')
    model_instance = sys_details('steve', 'is awesome')
    model_instance.save()
    body = conn.Object('mybucket', 'steve').get()['Body'].read().decode("utf-8")
    assert body == 'is awesome'