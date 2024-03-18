import os
import requests
from datetime import datetime, timedelta

# API_KEY = os.environ['TMDB_API_KEY']


class TMDb:

  def __init__(self, api_key):
    self.api_key = api_key
    self.base_url = "https://api.themoviedb.org/3/"

  def fetch_data(self, url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
      return response.json()
    else:
      print(f"Error: {response.status_code}")
      return None

  def fetch_movies(self, days, max_pages=None):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    url = f"{self.base_url}discover/movie"

    data = []

    page_number = 1
    while True:
      params = {
          "api_key": self.api_key,
          "languange": "en-US",
          "release_date.gte": start_date.strftime("%Y-%m-%d"),
          "end_date.lte": end_date.strftime("%Y-%m-%d"),
          "page": page_number
      }
      movies_data = self.fetch_data(url, params)
      if movies_data is not None:
        data.extend(movies_data["results"])

      if movies_data is None or page_number == movies_data["total_pages"]:
        break

      if max_pages is not None and page_number >= max_pages:
        break

      page_number += 1

    return data

  def fetch_reviews(self, movie_id, max_pages=None):
    url = f"{self.base_url}/movie/{movie_id}/reviews"

    data = []

    page_number = 1
    while True:
      params = {"api_key": self.api_key, "page": page_number}
      reviews_data = self.fetch_data(url, params)
      if reviews_data is not None:
        data.extend(reviews_data["results"])

      if reviews_data is None or page_number == reviews_data["total_pages"]:
        break

      if max_pages is not None and page_number >= max_pages:
        break

      page_number += 1

    return data
