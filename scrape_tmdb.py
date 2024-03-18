import os
from scraper import tmdb
# import google_drive_manager

TMDB_API_KEY = os.environ['TMDB_API_KEY']

movies = []

tmdb_obj = tmdb.TMDb(TMDB_API_KEY)

# fetch movies released in the last 90 days
movies = tmdb_obj.fetch_movies(days=90, max_pages=2)
print(movies)

# fetch reviews for each movie
for movie in movies:
  reviews = tmdb_obj.fetch_reviews(movie['id'], max_pages=2)
  print(reviews)
  break
