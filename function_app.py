import azure.functions as func
import logging
import json
import os
from azure.data.tables import TableServiceClient
from azure.core.credentials import AzureNamedKeyCredential
account_name = os.getenv("AccountName")
account_key =  os.getenv("AccountKey")
azurewebjobs = os.getenv("AzureWebJobsStorage")

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

#Get Movies
@app.function_name(name="GetMovies")
@app.route(route="GetMovies")
@app.table_input(arg_name="movies", table_name="Movies", connection="AzureWebJobsStorage")
def GetMovies(req: func.HttpRequest, movies) -> func.HttpResponse:
    logging.info('Python GetMovies trigger function processed a request.')
    movies_json = json.dumps(movies)
    return func.HttpResponse(
        movies_json 
        
    )
#Get Movies by Year
@app.function_name(name="GetMoviesByYear")
@app.route(route="GetMoviesByYear")
@app.table_input(arg_name="movies", table_name="Movies",connection="AzureWebJobsStorage")
def GetMoviesByYear(req: func.HttpRequest, movies) -> func.HttpResponse: 
    logging.info('Running GetMoviesByYear')
    year = req.params.get('year')

    #Checks if year parameter exists, if not, returns a status code 400.
    if not year: 
        return func.HttpResponse(
            "Please enter a year", status_code=400
        )
    else:
        filtered_movies = [movie for movie in movies ['ReleaseYear'] == year]
        filtered_movies_json = json.dumps(filtered_movies)
        return func.HttpResponse(
            filtered_movies_json
        )
    
    #Get Movies by Genre
@app.function_name(name="GetMoviesByGenre")
@app.route(route="GetMoviesByGenre")
@app.table_input(arg_name="movies", table_name="Movies", connection="AzureWebJobsStorage")
def GetMoviesByGenre(req: func.HttpRequest, movies) -> func.HttpResponse:
    logging.info('Running GetMoviesbyGenre')
    genre = req.params.get('genre')
    #Checks if genre parameter exists, if not, returns a status code 400
    if not genre:
        return func.HttpResponse("Please enter a genre", status_code=400)
    else:
        filtered_movies = [movie for movie in movies if movie['Genre'] == genre]
        filtered_movies_json = json.dumps(filtered_movies)
        return func.HttpResponse(filtered_movies_json)

connection_string="AzureWebJobsStorage"
#Create Movie
@app.function_name(name="CreateMovie")
@app.route(route="CreateMovie")
@app.table_output(arg_name="movie", table_name="Movies", connection="AzureWebJobsStorage")
def CreateMovie(req: func.HttpRequest, movie) -> func.HttpResponse:
    logging.info('running func CreateMovie')
    movie = req.get_json()
    if not movie:
        return func.HttpResponse("Please enter a movie", status_code=400)
    else:
        endpoint = f"https://{account_name}.table.core.windows.net/Movies"
        credential = AzureNamedKeyCredential(name=account_name, key=account_key)
        service = TableServiceClient(endpoint=endpoint,credential=credential)
        moviestable = service.get_table_client("Movies")
        movie_data = {
            "PartitionKey": movie["ReleaseYear"],
            "RowKey": movie["Genre"],
            "Title": movie["Title"],
            "Genre": movie["Genre"],
            "coverURL": movie["coverURL"],
            "ReleaseYear": movie["ReleaseYear"]
        }
        moviestable.create_entity(movie_data)

        return func.HttpResponse("Movie added successfully!", status_code=201)
