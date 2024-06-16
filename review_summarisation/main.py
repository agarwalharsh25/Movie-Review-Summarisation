import json
import os
import re
from datetime import datetime

from llm import llm
from review_summarisation import prompt
from utilities.preprocessing import get_preprocess_text

COHERE_API_KEY = os.environ['COHERE_API_KEY']


class ReviewSummariser:

    def __init__(self, movie_metadata, movie_reviews):
        self.movie_metadata = movie_metadata
        self.movie_reviews = movie_reviews

    def preproceess_text(self):
        # preprocess movie metadata
        movie_metadata_preprocessed = self.movie_metadata
        movie_metadata_preprocessed['overview'] = get_preprocess_text(self.movie_metadata['overview'])

        # preprocess movie reviews
        movie_reviews_preprocessed = []
        for review in self.movie_reviews:
            review_preprocessed = get_preprocess_text(review)
            movie_reviews_preprocessed.append(review_preprocessed)

        return movie_metadata_preprocessed, movie_reviews_preprocessed

    def build_review_summarisation_prompt(self, movie_metadata_preprocessed,
                                          movie_reviews_preprocessed):
        # build prompt input object

        movie_obj = {
            "movie_metadata": {
                "title":
                movie_metadata_preprocessed['title'],
                "genre":
                ", ".join(movie_metadata_preprocessed['genres']),
                "language":
                movie_metadata_preprocessed['language'],
                "release_year":
                (datetime.strptime(movie_metadata_preprocessed['release_date'],
                                   "%Y-%m-%d")).year,
                "plot_synopsis":
                movie_metadata_preprocessed['overview']
            },
            "movie_reviews": movie_reviews_preprocessed
        }

        movie_obj_str = json.dumps(movie_obj)

        return movie_obj_str

    def summarise_reviews(self):
        # preprocess text
        movie_metadata_preprocessed, movie_reviews_preprocessed = self.preproceess_text()

        # prompt to summarise movie reviews
        llm_review_summarisation_prompt = self.build_review_summarisation_prompt(
            movie_metadata_preprocessed, movie_reviews_preprocessed)

        # call llm to get movie summarised review
        llm_cohere = llm.LLM(COHERE_API_KEY, 'cohere')
        movie_summarised_review = llm_cohere.chat(
            llm_review_summarisation_prompt,
            prompt.MOVIE_REVIEWS_SUMMARY_PREAMBLE)

        movie_review_summary = {}
        # extract review json from llm response
        try:
            if movie_summarised_review:
                json_block_match = re.search(r'review\s*=\s*({.*})', movie_summarised_review, re.DOTALL)
                if json_block_match:
                    json_block = json_block_match.group(1)
                    
                    # clean json block
                    json_block = json_block.replace('\n', '').replace('\r', '').replace('\t', '')
                    json_block = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_block)
                    
                    movie_review_summary = json.loads(json_block)
        except Exception as e:
            print(e)
            print(movie_summarised_review)

        return movie_review_summary
