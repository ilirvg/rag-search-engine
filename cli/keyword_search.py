from fetch_data import get_movies_list
from text_processing import tokenize_and_process, tokenize_simple, stop_words


def search_comand(query: str) -> list[dict]:
    movies = []
    query_tokens = tokenize_and_process(query)

    if not query_tokens:
        return movies

    for movie in get_movies_list():
        title_tokens = tokenize_and_process(movie['title'])
        title_tokens = [token for token in title_tokens if token and token not in stop_words]
        if any(word in title_tokens for word in query_tokens):
            movies.append(movie)

    movies.sort(key=lambda item: item['id'])
    return movies