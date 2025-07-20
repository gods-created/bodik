from unittest import TestCase
from unittest.mock import MagicMock
from services import GetInfoFromDynamoDBService
from configs import AWS_CONFIGS, DYNAMODB_TABLE_NAME
from uuid import uuid4 

class GetInfoFromDynamoDBServiceTests(TestCase):
    def setUp(self):
        self.user_id = str(uuid4())

    def test_get_method(self):
        with GetInfoFromDynamoDBService(AWS_CONFIGS, DYNAMODB_TABLE_NAME) as service:
            service.get = MagicMock(return_value=())
            response = service.get(self.user_id)
            service.get.assert_called_once_with(self.user_id)
            
        self.assertIsInstance(response, tuple)