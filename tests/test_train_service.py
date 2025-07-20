from services import TrainService
from unittest import TestCase
from unittest.mock import patch
from faker import Faker

class TrainServiceTests(TestCase):
    def setUp(self):
        faker = Faker()
        self.file_obj, self.file_name = object(), ''.join(faker.random_letters()) + '.csv'
        
    @patch.object(TrainService, 'train')
    def test_train_method(self, mock):
        mock.return_value = ()
        service = TrainService()
        response = service.train(self.file_obj, self.file_name)
        mock.assert_called_once_with(self.file_obj, self.file_name)
        self.assertIsInstance(response, tuple)