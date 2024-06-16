import json
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Allow CORS for frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="webapp/static"), name="static")
app.mount("/data", StaticFiles(directory="data"), name="data")
templates = Jinja2Templates(directory="webapp/templates")

@app.get("/", response_class=HTMLResponse)
async def get_movies(request: Request):
    movie_data = []
    data_path = os.path.join(os.path.dirname(__file__), '../data')
    
    with open(data_path+'/movies/movies.json', "r") as f:
        movies = json.load(f)
    
    for movie in movies:
        if movie['c_reviews'] == 0:
            continue

        try:
            with open(f"{data_path}/summarised_reviews/{movie['id']}.json", "r") as f:
                movie_review = json.load(f)
    
            movie_obj = movie
            movie_obj["review"] = movie_review
    
            movie_data.append(movie_obj)

        except Exception as e:
            print(e)
            continue

    return templates.TemplateResponse("index.html", {"request": request, "movies": movie_data})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
