import nltk

def ensure_nltk_data(resource: str) -> None:
    try:
        nltk.data.find(resource)
    except LookupError:
        # Extract resource name from path for download
        # 'tokenizers/punkt' -> 'punkt'
        # 'corpus/stopwords' -> 'stopwords'
        resource_name = resource.split('/')[-1]
        nltk.download(resource_name, quiet=True)