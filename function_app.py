import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

movies = []
movie1 = {"Title":"The Dark Knight", "Release Year":"2008", "Genre": "Action","coverURL":"https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg"}
movie2 = {"Title":"Bogus Name", "Release Year": "2012", "Genre":"Retard", "coverURL":"https://example.org"}
movies.append(movie1)
movies.append(movie2)

@app.route(route="GetMovies")
def GetMovies(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python GetMovies trigger function processed a request.')

    movies_json = json.dumps(movies)
    return func.HttpResponse(
        movies_json 
        
    )

@app.route(route="GetMoviesByYear")
def GetMoviesByYear(req: func.HttpRequest) -> func.HttpResponse: 
    logging.info('Running GetMoviesByYear')

    year = req.params.get('year')
    filtered_movies = [ release_year for release_year in movies if release_year["Release Year"] == year]
    filtered_movies_json = json.dumps(filtered_movies)
    if year: 
        return func.HttpResponse(
            filtered_movies_json
        )
    else:
        return func.HttpResponse(
            "Please enter a year"
        )
    





    

'''def GetMovies(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )'''