import azure.functions as func
import logging
import json
from azure.data.tables import TableServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

#Get Movies
@app.route(route="GetMovies")
@app.table_input(arg_name="movies", table_name="Movies", connection="AzureWebJobsStorage")
def GetMovies(req: func.HttpRequest, movies) -> func.HttpResponse:
    logging.info('Python GetMovies trigger function processed a request.')

    movies_json = json.dumps(movies)
    return func.HttpResponse(
        movies_json 
        
    )
#Sets up TableServiceClient
connection_string = "UseDevelopmentStorage=true"
connection = TableServiceClient.from_connection_string(conn_str=connection_string)
#Get Movies by Year
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
        filter_string = f"ReleaseYear eq '{year}'"
        table_client=connection.get_table_client("Movies")
        results=table_client.query_entities(query_filter=filter_string)
        results_list = [dict(result) for result in results]
        results_json = json.dumps(results_list)
        return func.HttpResponse(
            results_json
        )
    
    #Get Movies by Genre
@app.route(route="GetMoviesByGenre")
@app.table_input(arg_name="genre", table_name="Movies", connection="AzureWebJobsStorage")
def GetMoviesByGenre(req: func.HttpRequest, genre) -> func.HttpResponse:
    logging.info('Running GetMoviesbyGenre')
    genre = req.params.get('genre')
    #Checks if genre parameter exists, if not, returns a status code 400
    if not genre:
        return func.HttpResponse("Please enter a genre", status_code=400)
    else:
        genre_filter_string = f"Genre eq '{genre}'"
        table_client=connection.get_table_client("Movies")
        results=table_client.query_entities(query_filter=genre_filter_string)
        """for result in results:
            logging.info(f"Query results: {result}")"""
        results_list= [dict(result) for result in results]
        results_json = json.dumps(results_list)
        return func.HttpResponse(results_json)
   