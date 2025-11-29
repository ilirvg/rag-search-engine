import json
from pathlib import Path

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
