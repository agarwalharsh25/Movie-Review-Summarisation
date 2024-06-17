function formatDate(inputDate) {
    const dateObj = new Date(inputDate);

    const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];

    const formattedDate = `${monthNames[dateObj.getMonth()]} ${dateObj.getFullYear()}`;

    return formattedDate;
}

document.addEventListener("DOMContentLoaded", () => {
    const posters = document.querySelectorAll(".movie-poster");
    const detailsContent = document.getElementById("details-content");
    const placeholder = document.getElementById("placeholder");
    const coverImage = document.getElementById("movie-cover-image");
    const posterImage = document.getElementById("movie-poster-image");
    const movieTitle = document.getElementById("movie-title");
    const genre = document.getElementById("movie-genres");
    const plotSynopsis = document.getElementById("movie-plot-synopsis");
    const releaseDate = document.getElementById("movie-release-date");
    const reviewSummary = document.getElementById("movie-review-summary");

    posters.forEach(poster => {
        poster.addEventListener("click", () => {
            const movie = JSON.parse(poster.dataset.movie);
            coverImage.src = `https://image.tmdb.org/t/p/original${movie.details.backdrop_path}`;
            posterImage.src = `https://image.tmdb.org/t/p/original${movie.details.poster_path}`;
            movieTitle.textContent = movie.details.title;
            genre.textContent = movie.details.genres.join(', ')
            plotSynopsis.textContent = movie.details.overview;
            releaseDate.textContent = formatDate(movie.details.release_date);
            
            reviewSummary.innerHTML = movie.review.movie_review;

            updateReviewEvaluation(movie.review.movie_evaluations, "storyline");
            updateReviewEvaluation(movie.review.movie_evaluations, "cinematography");
            updateReviewEvaluation(movie.review.movie_evaluations, "direction");
            updateReviewEvaluation(movie.review.movie_evaluations, "performances");
            updateReviewEvaluation(movie.review.movie_evaluations, "dialogues");
            updateReviewEvaluation(movie.review.movie_evaluations, "soundtrack");

            function updateReviewEvaluation(evaluationObj, evaluationMetric) {
                const evaluationMetricDiv = document.getElementById(evaluationMetric);
                if (evaluationObj.hasOwnProperty(evaluationMetric) && evaluationObj[evaluationMetric]["evaluation"].trim() !== '' && evaluationObj[evaluationMetric]["rating"] !== 0) {
                    const rating = evaluationMetricDiv.querySelector('#review-evaluation-rating');
                    const content = evaluationMetricDiv.querySelector('#review-evaluation-content');

                    rating.textContent = evaluationObj[evaluationMetric]["rating"];
                    content.innerHTML = evaluationObj[evaluationMetric]["evaluation"];

                    if (evaluationMetricDiv.classList.contains("d-none")) {
                        evaluationMetricDiv.classList.remove("d-none");
                    }
                } else {
                    if (!evaluationMetricDiv.classList.contains("d-none")) {
                        evaluationMetricDiv.classList.add("d-none");
                    }
                }
            }
            

            // reviewSummary.innerHTML = '';
            // for (const [aspect, summary] of Object.entries(movie.review_summary)) {
            //     const li = document.createElement("li");
            //     li.textContent = `${aspect.charAt(0).toUpperCase() + aspect.slice(1)}: ${summary}`;
            //     reviewSummary.appendChild(li);
            // }

            if (!placeholder.classList.contains("d-none")) {
                placeholder.classList.add("d-none");
            }
            if (detailsContent.classList.contains("d-none")) {
                detailsContent.classList.remove("d-none");
            }

            // Smooth scroll to the top of the page
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    });
});
