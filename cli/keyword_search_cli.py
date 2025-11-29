import argparse
import json
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            search_query = args.query
            searched_movies = search_comand(search_query)

            print(f'Searching for: {search_query}')
            for index, movie in enumerate(searched_movies[:5]):
                print(f'{index + 1}. {movie['title']}')

            pass
        case _:
            parser.print_help()



def get_movies_list() -> list[dict]:
    # Get the directory where this script is located and go up one level from cli/ to repo root
    script_dir = Path(__file__).parent.parent
    data_path = script_dir / 'data' / 'movies.json'

    try:
        with open(data_path, 'r') as data_file:
            data = json.load(data_file)
            return data['movies']
    except Exception as e:
        print(f'Failed to read the movies data: {e}')
        return

def search_comand(query:str) -> list[dict]:
    movies = []
    for movie in get_movies_list():
        if query.lower() in movie['title'].lower():
            movies.append(movie)

    movies.sort(key=lambda item: item['id'])
    return movies

if __name__ == "__main__":
    main()  