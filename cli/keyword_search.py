from fetch_data import get_movies_list

def search_comand(query:str) -> list[dict]:
    movies = []
    for movie in get_movies_list():
        if query.lower() in movie['title'].lower():
            movies.append(movie)

    movies.sort(key=lambda item: item['id'])
    return movies