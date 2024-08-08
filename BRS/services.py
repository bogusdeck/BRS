import requests

GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'

def fetch_books(query, api_key, res):
    params = {
        'q': query,
        'key': api_key,
        'maxResults': res
    }
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def fetch_book_for_preference(preference, api_key):
    query = '+'.join(preference)
    response = fetch_books(query, api_key, 10)
    return response.get('items',[])
