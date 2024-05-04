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
        pass
        
    def summarise_reviews(self):
        # preprocess text
        movie_metadata_preprocessed, movie_reviews_preprocessed = self.preproceess_text()

        # summarise movie reviews
        llm_review_summarisation_prompt = self.build_review_summarisation_prompt(movie_metadata_preprocessed, movie_reviews_preprocessed)
        
        movie_review_summary = ""
        # TODO: implement summarisation logic

        return movie_review_summary
        