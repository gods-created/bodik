from unittest import TestCase
from unittest.mock import MagicMock
from services import SaveToS3Service
from uuid import uuid4
from configs import AWS_CONFIGS, S3_BUCKET_NAME

class SaveToS3ServiceTests(TestCase):
    def setUp(self):
        user_id = str(uuid4())
        self.data = (
            f'{user_id}_training_set.csv',
            f'{user_id}_vectorizer.pkl',
            f'{user_id}_model.pkl',
            f'Test USER ID is {user_id}.',
            f'/tmp/{user_id}_vectorizer.csv',
            f'/tmp/{user_id}_model.csv',
        )

    def test_save_method(self):
        with SaveToS3Service(AWS_CONFIGS, S3_BUCKET_NAME) as service:
            service.save = MagicMock(return_value=())
            response = service.save(*self.data)
            service.save.assert_called_once_with(*self.data)
        
        self.assertIsInstance(response, tuple)