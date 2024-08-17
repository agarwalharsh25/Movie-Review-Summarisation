import json

from review_summarisation import main as movie_reviewer


def main():
    # loop through movies and their reviews
    with open('data/movies/movies.json', 'r') as file:
        movies = json.load(file)

    for movie in movies:
        if movie['c_reviews'] == 0:
            continue
        
        movie_id = movie['id']

        with open(f'data/reviews/{movie_id}.json', 'r') as file:
            movie_reviews = json.load(file)

        movie_metadata = {
            'title': movie['title'],
            'genres': movie['genres'],
            'language': movie['language'],
            'release_date': movie['release_date'],
            'overview': movie['overview']
        }

        movie_reviews = [review['content'] for review in movie_reviews]
        
        # summarise TMDb reviews
        summariser = movie_reviewer.ReviewSummariser(movie_metadata, movie_reviews)
        movie_summary = summariser.summarise_reviews()

        with open(f'data/summarised_reviews/{movie_id}.json', 'w') as file:
            json.dump(movie_summary, file)


if __name__=="__main__":
    main()
