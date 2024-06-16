document.addEventListener("DOMContentLoaded", () => {
    const posters = document.querySelectorAll(".movie-poster");
    const detailsContent = document.getElementById("details-content");
    const placeholder = document.getElementById("placeholder");
    const coverImage = document.getElementById("cover-image");
    const movieTitle = document.getElementById("movie-title");
    const genre = document.getElementById("genre");
    const plotSynopsis = document.getElementById("plot-synopsis");
    const releaseDate = document.getElementById("release-date");
    const reviewSummary = document.getElementById("review-summary");

    posters.forEach(poster => {
        poster.addEventListener("click", () => {
            const movie = JSON.parse(poster.dataset.movie);
            coverImage.src = movie.cover_image;
            movieTitle.textContent = movie.title;
            genre.textContent = `Genre: ${movie.genre}`;
            plotSynopsis.textContent = `Plot: ${movie.plot_synopsis}`;
            releaseDate.textContent = `Release Date: ${movie.release_date}`;

            reviewSummary.innerHTML = '';
            for (const [aspect, summary] of Object.entries(movie.review_summary)) {
                const li = document.createElement("li");
                li.textContent = `${aspect.charAt(0).toUpperCase() + aspect.slice(1)}: ${summary}`;
                reviewSummary.appendChild(li);
            }

            placeholder.classList.add("d-none");
            detailsContent.classList.remove("d-none");
        });
    });
});
