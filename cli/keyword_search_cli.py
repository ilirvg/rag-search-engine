import argparse
from re import sub
from keyword_search import search_comand
from inverted_index import InvertedIndex

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build the inverted index")

    args = parser.parse_args()

    match args.command:
        case "search":
            search_query = args.query
            searched_movies = search_comand(search_query)
            print(f'Searching for: {search_query}')
            for index, movie in enumerate(searched_movies[:5]):
                print(f'{index + 1}. {movie['title']}')
            
        case "build":
            idx = InvertedIndex()
            idx.build()
            idx.save()
            
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()  