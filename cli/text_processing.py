import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from utils import ensure_nltk_data

ensure_nltk_data('tokenizers/punkt_tab')  # Newer NLTK versions use punkt_tab
ensure_nltk_data('corpus/stopwords')

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

translator = str.maketrans("", "", string.punctuation)

def stem_tokens(tokenized_words:list[str]) -> list[str]:
    return [stemmer.stem(word) for word in tokenized_words]

# def tokenize_and_process(text: str) -> list[str]:
#     processed_text: list[str] = word_tokenize(text.lower().translate(translator))
#     return stem_tokens(processed_text)

def tokenize_and_process(text: str) ->str:
    return text.lower().translate(translator)

def tokenize_simple(text: str) -> list[str]:
    processed_text: list[str] = word_tokenize(text.lower())
    return stem_tokens(processed_text)
