from fetch_data import get_movies_list
from text_processing import tokenize_and_process

from pathlib import Path
import pickle

class InvertedIndex():
    index = {} # a dictionary mapping tokens (strings) to sets of document IDs (integers).
    docmap = {} # a dictionary mapping document IDs to their full document objects.

    def __add_document(self, doc_id, text):
        tokenized_text = tokenize_and_process(text)
        for token in tokenized_text:
            if token in InvertedIndex.index:
                InvertedIndex.index[token].add(doc_id)
            else:
                InvertedIndex.index[token] = {doc_id}

    def get_documents(self, term):
        term_ids = []
        if term.lower() in InvertedIndex.index:
            term_ids = list(InvertedIndex.index[term.lower()])
        return sorted(term_ids)

    def build(self):
        for movie in get_movies_list():
            text = movie['title'] + " " + movie['description']
            self.__add_document(movie['id'], text)
            InvertedIndex.docmap[movie['id']] = movie

    def pickle_object(self, path, obj) -> None:
        try:
            with open(path, 'wb') as file:
                pickle.dump(obj, file)
        except IOError as e:
            print(f"Error creating/writing to file {path}: {e}")
        except pickle.PickleError as e:
            print(f"Error while tyring to pickele {e}")


    def save(self):
        cache_path = Path("cache")
        cache_path.mkdir(parents=True, exist_ok=True)
        index_path = cache_path / 'index.pkl'
        docmap_path = cache_path / 'docmap.pkl'
        
        self.pickle_object(index_path, InvertedIndex.index)
        self.pickle_object(docmap_path, InvertedIndex.docmap)


if __name__ == "__main__":
    idx = InvertedIndex()
    idx._InvertedIndex__add_document(1, "test 123")