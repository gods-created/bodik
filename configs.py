from os import getenv
from dotenv import load_dotenv

load_dotenv()

AWS_CONFIGS = {
    'aws_access_key_id': getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': getenv('AWS_SECRET_ACCESS_KEY'),
    'region_name': getenv('AWS_REGION_NAME')
}

S3_BUCKET_NAME = getenv('S3_BUCKET_NAME')
DYNAMODB_TABLE_NAME = getenv('DYNAMODB_TABLE_NAME')
TMP_PATH = getenv('TMP_PATH')