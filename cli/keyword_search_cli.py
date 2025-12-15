import argparse
import math
from re import sub
from keyword_search import search_comand
from inverted_index import InvertedIndex

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build the inverted index")

    tf_parser = subparsers.add_parser('tf', help="Get the token frequency")
    tf_parser.add_argument("doc_id", type=int, help="The ID of the documetn we need to search on")
    tf_parser.add_argument("term", type=str, help="The token we need to get the frequency")

    idf_parser = subparsers.add_parser("idf", help="Get the inverted document frequency")
    idf_parser.add_argument("term", type=str, help="The token we need to get idf")

    tfidf_parser = subparsers.add_parser("tfidf", help="Term Frequency-Inverse Document Frequency")
    tfidf_parser.add_argument("doc_id", type=int, help="The ID of the documetn we need to search on")
    tfidf_parser.add_argument("term", type=str, help="The token we need to get the frequency")

    args = parser.parse_args()

    idx = InvertedIndex()

    match args.command:
        case "search":
            search_query = args.query
            searched_movies = search_comand(search_query)
            print(f'Searching for: {search_query}')
            for index, movie in enumerate(searched_movies):
                print(f'{index + 1}. {movie['id']} {movie['title']}')
            
        case "build":
            idx.build()
            idx.save()
        
        case "tf":
            idx.load()
            tf_value = idx.get_tf(args.doc_id, args.term)
            print(f"Term {args.term} is found {tf_value} times in document {args.doc_id}")
            
        case "idf":
            idx.load()
            total_doc_count = len(idx.docmap)
            term_match_doc_count = len(idx.get_documents(args.term))
            idf_value = math.log((total_doc_count + 1) / (term_match_doc_count + 1))
            print(f"Inverse document frequency of '{args.term}': {idf_value:.2f}")

        case "tfidf":
            idx.load()
            tf_value = idx.get_tf(args.doc_id, args.term)
            total_doc_count = len(idx.docmap)
            term_match_doc_count = len(idx.get_documents(args.term))
            idf_value = math.log((total_doc_count + 1) / (term_match_doc_count + 1))
            tfidf_value = tf_value * idf_value
            print(f"TF-IDF score of '{args.term}' in document '{args.doc_id}': {tfidf_value:.2f}")

        case _:
            parser.print_help()

if __name__ == "__main__":
    main()  