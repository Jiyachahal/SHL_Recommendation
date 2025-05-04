import re
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# Ensure stopwords are downloaded once
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess_text(text):
    # Remove special characters and lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
    # Tokenize, remove stopwords, and stem
    tokens = [stemmer.stem(word) for word in text.split() if word not in stop_words]
    return ' '.join(tokens)
