from fetch_data import get_movies_list
from text_processing import tokenize_and_process, tokenize_simple, stop_words
from inverted_index import InvertedIndex

def search_comand(query: str) -> list[dict]:
    movies = []
    query_tokens = tokenize_simple(query)

    if not query_tokens:
        return movies

    idx = InvertedIndex()

    try:
        idx.load()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return []

    seen_doc_ids = set()

    for token in query_tokens:
        if len(movies) >= 5:
            break
        for doc_id in idx.get_documents(token):
            if doc_id not in seen_doc_ids:
                seen_doc_ids.add(doc_id)
                movie = idx.docmap[doc_id]
                movies.append(movie)
                if len(movies) >= 5:
                    break

    movies.sort(key=lambda item: item['id'])
    return movies