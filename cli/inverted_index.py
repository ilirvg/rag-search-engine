from fetch_data import get_movies_list
from text_processing import tokenize_and_process

from collections import Counter
from pathlib import Path
import pickle

class InvertedIndex():
    index = {} # a dictionary mapping tokens (strings) to sets of document IDs (integers).
    docmap = {} # a dictionary mapping document IDs to their full document objects.
    term_frequencies = {} # a nested dictionary mapping document IDs (integers) to Counter objects, where each Counter maps tokens (strings) to their frequency counts (integers) within that document.

    def __add_document(self, doc_id, text):
        tokenized_text = tokenize_and_process(text)

        for token in tokenized_text:
            if token in InvertedIndex.index:
                InvertedIndex.index[token].add(doc_id)
            else:
                InvertedIndex.index[token] = {doc_id}

            if doc_id not in InvertedIndex.term_frequencies:
                InvertedIndex.term_frequencies[doc_id] = Counter()
            InvertedIndex.term_frequencies[doc_id][token] += 1

    def get_documents(self, term):
        term_ids = []
        tokenized_term_list = tokenize_and_process(term)
        if len(tokenized_term_list) == 0:
            return []
        tokenized_term = tokenized_term_list[0]
        if tokenized_term in InvertedIndex.index:
            term_ids = list(InvertedIndex.index[tokenized_term])
        return sorted(term_ids)

    def build(self):
        for movie in get_movies_list():
            text = movie['title'] + " " + movie['description']
            self.__add_document(movie['id'], text)
            InvertedIndex.docmap[movie['id']] = movie

    def pickle_dump(self, path, obj) -> None:
        try:
            with open(path, 'wb') as file:
                pickle.dump(obj, file)
        except IOError as e:
            print(f"Error creating/writing to file {path}: {e}")
        except pickle.PickleError as e:
            print(f"Error while tyring to dump pickele {e}")

    def save(self):
        cache_path = Path("cache")
        cache_path.mkdir(parents=True, exist_ok=True)
        index_path = cache_path / 'index.pkl'
        docmap_path = cache_path / 'docmap.pkl'
        term_frequencies_path = cache_path / "term_frequencies.pkl"

        self.pickle_dump(index_path, InvertedIndex.index)
        self.pickle_dump(docmap_path, InvertedIndex.docmap)
        self.pickle_dump(term_frequencies_path, InvertedIndex.term_frequencies)

    def pickle_load(self, path) -> object:
        try:
            with open(path, 'rb') as file:
                loaded_object = pickle.load(file)
                return loaded_object
        except IOError as e:
            print(f"Error opening the file {path}: {e}")
        except pickle.PickleError as e:
            print(f"Error while tyring to load pickele {e}")

    def load(self):
        try:
            cache_path = Path("cache")
            index_path = cache_path / 'index.pkl'
            docmap_path = cache_path / 'docmap.pkl'
            term_frequencies_path = cache_path / "term_frequencies.pkl"

            if not index_path.exists():
                raise FileNotFoundError(f"Index file not found: {index_path}")
            if not docmap_path.exists():
                raise FileNotFoundError(f"Docmap file not found: {docmap_path}")
            if not term_frequencies_path.exists():
                raise FileNotFoundError(f"Term frequency file not found: {term_frequencies_path}")

            InvertedIndex.index = self.pickle_load(index_path)
            InvertedIndex.docmap = self.pickle_load(docmap_path)
            InvertedIndex.term_frequencies = self.pickle_load(term_frequencies_path)

        except Exception as e:
            print(f"Error loading {e}")
            exit()

    def get_tf(self, doc_id, term):
        tokenized_term_list = tokenize_and_process(term)

        if len(tokenized_term_list) > 1:
            raise Exception(f"Ther term has {len(tokenized_term_list)} tokens but we need only 1")

        if len(tokenized_term_list) == 0:
            return 0

        tokenized_term = tokenized_term_list[0]

        if doc_id not in InvertedIndex.term_frequencies:
            return 0

        # Counter automatically returns 0 for missing keys
        return InvertedIndex.term_frequencies[doc_id][tokenized_term]

if __name__ == "__main__":
    idx = InvertedIndex()
    idx._InvertedIndex__add_document(1, "test 123")