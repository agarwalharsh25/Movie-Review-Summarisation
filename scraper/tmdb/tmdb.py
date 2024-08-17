from datetime import datetime, timedelta

import requests


class TMDb:

  def __init__(self, api_key):
    self.api_key = api_key
    self.base_url = "https://api.themoviedb.org/3/"

  def fetch_data(self, url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
      return response.json()
    else:
      print(f"Error: {response.json()} \n Request: {(url, params)}")
      return None

  def fetch_movies(self, language, min_vote_count, days, max_pages=None):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    url = f"{self.base_url}discover/movie"

    data = []

    page_number = 1
    while True:
      params = {
          "api_key": self.api_key,
          "languange": "en-US",
          "primary_release_date.gte": start_date.strftime("%Y-%m-%d"),
          "primary_release_date.lte": end_date.strftime("%Y-%m-%d"),
          "with_original_language": language,
          "vote_count.gte": min_vote_count,
          "page": page_number
      }
      movies_data = self.fetch_data(url, params)
      if movies_data is not None:
        data.extend(movies_data["results"])

      if movies_data is None or page_number >= movies_data["total_pages"]:
        break

      if max_pages is not None and page_number >= max_pages:
        break

      page_number += 1

    return data

  def fetch_reviews(self, movie_id, max_pages=None):
    url = f"{self.base_url}movie/{movie_id}/reviews"

    data = []

    page_number = 1
    while True:
      params = {"api_key": self.api_key, "page": page_number}
      reviews_data = self.fetch_data(url, params)
      if reviews_data is not None:
        data.extend(reviews_data["results"])

      if reviews_data is None or page_number >= reviews_data["total_pages"]:
        break

      if max_pages is not None and page_number >= max_pages:
        break

      page_number += 1

    return data

  def fetch_genres(self):
    url = f"{self.base_url}genre/movie/list"

    params = {"api_key": self.api_key, "languange": "en-US"}

    data = self.fetch_data(url, params)

    if data is not None:
      genre_dict = {}
      for genre in data["genres"]:
        genre_dict[genre["id"]] = genre["name"]
      return genre_dict

    return {}
