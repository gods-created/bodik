from services import SaveToDynamoDBService
from unittest import TestCase
from unittest.mock import MagicMock
from uuid import uuid4
from configs import AWS_CONFIGS, DYNAMODB_TABLE_NAME

class SaveToDynamoDBServiceTests(TestCase):
    def setUp(self):
        user_id = str(uuid4())
        self.data = (
            user_id,
            f'{user_id}_model.pkl',
            f'{user_id}_vectorizer.pkl'
            f'{user_id}_training_set.csv'
        )

    def test_save_method(self):
        with SaveToDynamoDBService(AWS_CONFIGS, DYNAMODB_TABLE_NAME) as service:
            service.save = MagicMock(return_value=())
            response = service.save(*self.data)
            service.save.assert_called_once_with(*self.data)
        
        self.assertIsInstance(response, tuple)