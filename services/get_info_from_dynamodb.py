from boto3 import resource
from botocore.exceptions import ClientError, ConnectionError, BotoCoreError
from exceptions import NoUserException

class GetInfoFromDynamoDBService:
    def __init__(self, aws_configs: dict, table_name: str):
        self.aws_configs = aws_configs
        self.table_name = table_name
        self.dynamodb_resource = None

    def __enter__(self):
        self.dynamodb_resource = resource('dynamodb', **self.aws_configs) \
            .Table(self.table_name)
        return self
    
    def get(self, user_id: str) -> tuple:
        status, message, data = False, None, None 

        try:
            response = self.dynamodb_resource.get_item(Key={'user_id': user_id})
            item = response.get('Item', {})
            if not item:
                raise NoUserException('The data with so ID doesn\'t exist.')
            
            data = (item.get('model'), item.get('vectorizer'))
            status = not status

        except (
            Exception,
            ClientError, 
            ConnectionError, 
            BotoCoreError,
            NoUserException
        ) as e:
            message = str(e)

        finally:
            return status, message, data
        
    def __exit__(self, *args, **kwargs):
        pass