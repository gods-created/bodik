from boto3 import resource
from botocore.exceptions import (
    ClientError, 
    ConnectionError, 
    HTTPClientError, 
    BotoCoreError
)

class SaveToDynamoDBService:
    def __init__(self, aws_configs: dict, table_name: str):
        self.aws_configs = aws_configs
        self.table_name = table_name
        self.dynamodb_resource = None 

    def __enter__(self):
        self.dynamodb_resource = resource('dynamodb', **self.aws_configs).Table(self.table_name)
        return self
    
    def save(
        self, 
        user_id: str,
        training_set_file_name: str,
        vectorizer_file_name: str,
        model_file_name: str,
    ) -> tuple:
        status, message = False, None 

        try:
            self.dynamodb_resource.put_item(
                Item={
                    'user_id': user_id,
                    'model': model_file_name,
                    'vectorizer': vectorizer_file_name,
                    'training_set': training_set_file_name
                }
            )
            
            status = not status
            message = 'Row with USER_ID and other data have been saved success to DynamoDB table.'

        except (
            Exception,
            ClientError, 
            ConnectionError, 
            HTTPClientError, 
            BotoCoreError
        ) as e:
            message = str(e)
        
        finally:
            return status, message
    
    def __exit__(self, *agrs, **kwargs):
        pass