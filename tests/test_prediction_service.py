from unittest import TestCase
from unittest.mock import patch
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from services import PredictionService
from faker import Faker 

class PredictionServiceTests(TestCase):
    def setUp(self):
        faker = Faker()
        self.model = MultinomialNB()
        self.vectorizer = CountVectorizer()
        self.text = faker.text()

    @patch.object(PredictionService, 'predict')
    def test_predict_method(self, mock):
        args = (self.model, self.vectorizer, self.text)
        mock.return_value = ()
        service = PredictionService()
        response = service.predict(*args)
        mock.assert_called_once_with(*args)
        self.assertIsInstance(response, tuple)