from pathlib import Path

import nltk
from nltk.stem.wordnet import WordNetLemmatizer

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline


class TweetsClassificationPipeline:
    def __init__(self, pipeline=None, app=None):

        self.app = app
        self.tokenizer = nltk.tokenize.TweetTokenizer(strip_handles=True, reduce_len=True)
        self.lemmatizer = WordNetLemmatizer()
        if pipeline is None:
            self.pipeline = Pipeline([
                                    ("vectorizer", TfidfVectorizer(ngram_range=(1, 3), strip_accents='unicode', max_df=0.7, tokenizer=self.process_text)),
                                    ("model", SGDClassifier(loss="log", penalty="l2", alpha=0.0000005, verbose=4, tol=0.001, average=True))
                                    ])
        else:
            self.pipeline = pipeline

    def init_app(self, app):

        self.app = app
        nltk.download('wordnet')
        try:
            print('Loading ML model ... (this might take a while)')
            self.pipeline = joblib.load(Path().cwd() / "main" / "methods" / "ml_pipeline.sav")
        except Exception as e:
            print(f'\nWarning [!] : IS THE FlASK SERVER RESTARTING ?')
            print(f'** {e}\n')
            raise e

    def process_text(self, text):
        return [self.lemmatizer.lemmatize(token) for token in self.tokenizer.tokenize(text)]
