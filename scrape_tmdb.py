import json
import os

from scraper import tmdb

TMDB_API_KEY = os.environ['TMDB_API_KEY']

movies = []

tmdb_obj = tmdb.TMDb(TMDB_API_KEY)

# fetch movie genres
genres = tmdb_obj.fetch_genres()

# fetch movies released in the last 90 days
movies_en = tmdb_obj.fetch_movies(language='en', min_vote_count=1, days=90)
movies_hi = tmdb_obj.fetch_movies(language='hi', min_vote_count=1, days=90)
movies = []
movies.extend(movies_en)
movies.extend(movies_hi)

print(f"{len(movies)} movies scraped.")

movie_details = []

# fetch reviews for each movie
for movie in movies:
    reviews = tmdb_obj.fetch_reviews(movie['id'])

    review_details = []
    for review in reviews:
        review_obj = {
            "id": review["id"],
            "author": review["author"],
            "content": review["content"],
            "created_at": review["created_at"],
            "updated_at": review["updated_at"]
        }
        review_details.append(review_obj)
    with open('data/movies/movies.json', 'w') as file:
        json.dump(review_details, file)

    movie_obj = {
        "id": movie["id"],
        "title": movie["title"],
        "language": movie["original_language"],
        "overview": movie["overview"],
        "release_date": movie["release_date"],
        "vote_count": movie["vote_count"],
        "vote_average": movie["vote_average"],
        "popularity": movie["popularity"],
        "poster_path": movie["poster_path"],
        "backdrop_path": movie["backdrop_path"],
        "genres": [genres[genre_id] for genre_id in movie['genre_ids']],
        "c_reviews": len(review_details)
    }
    movie_details.append(movie_obj)

with open('data/movies/movies.json', 'w') as file:
    json.dump(movie_details, file)
