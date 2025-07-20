import nltk
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class PredictionService:
    def __init__(self):
        nltk.download('stopwords')
        nltk.download('punkt') 

    def _prepared_text(self, text: str) -> str:
        text = text.lower().translate(str.maketrans('', '', punctuation)) 
        tokens = [word for word in word_tokenize(text) if word not in set(stopwords.words('english'))]
        return ' '.join(tokens)

    def predict(self, model: MultinomialNB, vectorizer: CountVectorizer, text: str) -> tuple:
        status, message = False, None 

        try:
            X = vectorizer.transform([self._prepared_text(text)])
            message, *_ = model.predict(X)
            status = not status

        except (Exception, ) as e:
            message = str(e)

        finally:
            return status, message