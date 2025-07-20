from boto3 import resource
from botocore.exceptions import (
    ClientError, 
    ConnectionError, 
    HTTPClientError, 
    InvalidS3AddressingStyleError, 
    BotoCoreError
)
from io import BytesIO

class SaveToS3Service:
    def __init__(self, aws_configs: dict, bucket_name: str):
        self.aws_configs = aws_configs
        self.bucket_name = bucket_name
        self.s3_resource = None 

    def __enter__(self):
        self.s3_resource = resource('s3', **self.aws_configs).Bucket(self.bucket_name)
        return self
    
    def save(
        self,
        training_set_file_name: str,
        vectorizer_file_name: str,
        model_file_name: str, 
        content: str,
        full_path_to_vectorizer: str,
        full_path_to_model: str,
    ) -> tuple:
        status, message = False, None 

        try:
            raw_bytes = BytesIO()
            raw_bytes.write(content.encode('utf-8'))
            raw_bytes.seek(0)

            self.s3_resource.upload_fileobj(raw_bytes, f'training_sets/{training_set_file_name}')
            self.s3_resource.upload_file(full_path_to_vectorizer, f'vectorizers/{vectorizer_file_name}')
            self.s3_resource.upload_file(full_path_to_model, f'models/{model_file_name}')

            status = not status
            message = 'Training set, vectorizer, model have been saved success to S3 bucket.'

        except (
            Exception,
            ClientError, 
            ConnectionError, 
            HTTPClientError, 
            InvalidS3AddressingStyleError, 
            BotoCoreError
        ) as e:
            message = str(e)

        finally:
            return status, message
    
    def __exit__(self, *agrs, **kwargs):
        pass