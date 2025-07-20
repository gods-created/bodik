import nltk, pandas
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from exceptions import InvalidUploadedFile
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from uuid import uuid4
from joblib import dump
from io import StringIO
from os.path import join

class TrainService:
    def __init__(self, tmp_path: str = './assets'):
        self.tmp_path = tmp_path

        nltk.download('stopwords')
        nltk.download('punkt')

    def _prepared_text(self, text: str) -> str:
        text = text.lower().translate(str.maketrans('', '', punctuation))
        tokens = [word for word in word_tokenize(text) if word not in set(stopwords.words('english'))]
        return ' '.join(tokens)

    def train(self, file_object: object, file_name: str) -> tuple:
        message, data = None, None 

        try:
            if not file_name.endswith('.csv'):
                raise InvalidUploadedFile('Invalid uploaded file extension.')

            content = file_object.read().decode('utf-8')
            raw_strings = StringIO()
            raw_strings.write(content)
            raw_strings.seek(0)

            df = pandas.read_csv(filepath_or_buffer=raw_strings)
            X = df.iloc[:, :-1].values
            Y = df.iloc[:, -1].values

            vectorizer = CountVectorizer()
            model = MultinomialNB()

            texts = [self._prepared_text(item[0]) for item in X]
            X_train, _, y_train, _ = train_test_split(
                vectorizer.fit_transform(texts),
                Y,
                test_size=.2,
                random_state=42
            )

            model.fit(X_train, y_train)

            user_id = str(uuid4())
            tmp_path, training_set_file_name, vectorizer_file_name, model_file_name = (
                self.tmp_path,
                f'{user_id}_training_set.csv',
                f'{user_id}_vectorizer.pkl',
                f'{user_id}_model.pkl',
            )

            full_path_to_vectorizer, full_path_to_model = (
                join(tmp_path, vectorizer_file_name),
                join(tmp_path, model_file_name),
            )

            dump(vectorizer, full_path_to_vectorizer)
            dump(model, full_path_to_model)

            message = 'Model and vectorizer trained success.'

            data = (
                user_id,
                training_set_file_name,
                vectorizer_file_name,
                model_file_name,
                content,
                full_path_to_vectorizer,
                full_path_to_model,
            )

        except (Exception, InvalidUploadedFile, ) as e:
            message = str(e)

        finally:
            return message, data
