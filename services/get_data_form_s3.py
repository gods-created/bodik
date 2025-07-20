from boto3 import resource
from botocore.exceptions import ClientError, ConnectionError, BotoCoreError, InvalidS3AddressingStyleError
from os.path import join, exists
from os import makedirs
from exceptions import ModelOrVectorizerDoesNotExist
from joblib import load
from shutil import rmtree

class GetDataFromS3Service:
    def __init__(self, aws_configs: dict, bucket_name: str):
        self.aws_configs = aws_configs
        self.bucket_name = bucket_name
        self.s3_resource = None

    def __enter__(self):
        self.s3_resource = resource('s3', **self.aws_configs) \
            .Bucket(self.bucket_name)
        return self
    
    def get(self, dir: str, model_filename: str, vectorizer_filename: str) -> tuple:
        status, message, data = False, None, None 

        try:
            if not exists(dir):
                makedirs(dir)

            fullpathes = []
            for index, filename in enumerate([model_filename, vectorizer_filename], 1):
                key = f'models/{filename}' if index == 1 else f'vectorizers/{filename}'
                fullpath = join(dir, filename)

                self.s3_resource \
                    .download_file(
                        key,
                        fullpath
                    )
                
                fullpathes.append(fullpath)
            
            checking = (exists(path) for path in fullpathes)
            if not all(checking):
                raise ModelOrVectorizerDoesNotExist('Model or vectorizer doesn\'t find. Next executing is impossible.')

            data = (load(fullpathes[0]), load(fullpathes[1]), )
            status = not status, rmtree(dir)

        except (
            Exception,
            ClientError, 
            ConnectionError, 
            BotoCoreError,
            InvalidS3AddressingStyleError,
            ModelOrVectorizerDoesNotExist
        ) as e:
            message = str(e)

        finally:
            return status, message, data
        
    def __exit__(self, *args, **kwargs):
        pass