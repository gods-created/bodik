from unittest import TestCase
from unittest.mock import MagicMock
from services import GetDataFromS3Service
from configs import AWS_CONFIGS, S3_BUCKET_NAME
from uuid import uuid4 

class GetDataFromS3ServiceTests(TestCase):
    def setUp(self):
        self.user_id = str(uuid4())

    def test_get_method(self):
        with GetDataFromS3Service(AWS_CONFIGS, S3_BUCKET_NAME) as service:
            service.get = MagicMock(return_value=())
            response = service.get(self.user_id)
            service.get.assert_called_once_with(self.user_id)
            
        self.assertIsInstance(response, tuple)