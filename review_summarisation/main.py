import ast
import json
from datetime import datetime

from utilities.preprocessing import get_preprocess_text


class ReviewSummariser:

    def __init__(self, movie_metadata, movie_reviews):
        self.movie_metadata = movie_metadata
        self.movie_reviews = movie_reviews

    def preproceess_text(self):
        # preprocess movie metadata
        movie_metadata_preprocessed = get_preprocess_text(self.movie_metadata)

        # preprocess movie reviews
        movie_reviews_preprocessed = []
        for review in self.movie_reviews:
            review_preprocessed = get_preprocess_text(review)
            movie_reviews_preprocessed.append(review_preprocessed)

        return movie_metadata_preprocessed, movie_reviews_preprocessed

    def build_review_summarisation_prompt(self, movie_metadata_preprocessed, movie_reviews_preprocessed):
        # build prompt input object

        movie_obj = {
            "movie_metadata": {
                "title": movie_metadata_preprocessed['title'],
                "genre": ", ".join(ast.literal_eval(movie_metadata_preprocessed['genres'])),
                "language": movie_metadata_preprocessed['original_language'],
                "release_year": (datetime.strptime(movie_metadata_preprocessed['release_date'], "%Y-%m-%d")).year,
                "plot_synopsis": movie_metadata_preprocessed['overview']
            },
            "movie_reviews": movie_reviews_preprocessed
        }
        
        movie_obj_str = json.dumps(movie_obj)

        return movie_obj_str
        
    def summarise_reviews(self):
        # preprocess text
        movie_metadata_preprocessed, movie_reviews_preprocessed = self.preproceess_text()

        # summarise movie reviews
        llm_review_summarisation_prompt = self.build_review_summarisation_prompt(movie_metadata_preprocessed, movie_reviews_preprocessed)
        
        movie_review_summary = {}
        # TODO: implement summarisation logic

        return movie_review_summary
        