import azure.functions as func
import logging
import json
import os
from azure.data.tables import TableServiceClient
from azure.core.credentials import AzureNamedKeyCredential
from azure.data.tables import TableClient

account_name = os.getenv("AccountName")
account_key =  os.getenv("AccountKey")
azurewebjobs = os.getenv("AzureWebJobsStorage")
connection_string = os.getenv("WEBSITE_CONTENTAZUREFILECONNECTIONSTRING")

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

#Get Movies
@app.function_name(name="GetMovies")
@app.route(route="GetMovies")
@app.table_input(arg_name="movies", table_name="Movies", connection="AzureWebJobsStorage")
def GetMovies(req: func.HttpRequest, movies) -> func.HttpResponse:
    logging.info('GetMovies trigger function processed a request.')
    logging.info(f"Movies: {movies}")

    movies_json = json.dumps(movies)
    logging.info(f"Movies JSON: {movies_json}")
    return func.HttpResponse(
        movies_json 
        
    )
#Get Movies by Year
@app.function_name(name="GetMoviesByYear")
@app.route(route="GetMoviesByYear")
@app.table_input(arg_name="movies", table_name="Movies",connection="AzureWebJobsStorage")
def GetMoviesByYear(req: func.HttpRequest, movies) -> func.HttpResponse: 
    logging.info('Running GetMoviesByYear')
    logging.info(f"Movies Type: {type(movies)}")
    logging.info(f"Movies data: {movies}")

    #Converts movies data to python list using json.loads
    movies_to_list=json.loads(movies)
    logging.info(f"Movies Type After Conversion with JSON.loads: {type(movies_to_list)}")

    #Gets year parameter from URL
    year = req.params.get('year')
    logging.info(f"Year received: {year}")

    #Checks if year parameter exists, if not, returns a status code 400.
    if not year: 
        return func.HttpResponse(
            "Please enter a year", status_code=400
        )
    else:
        filtered_movies = []
        logging.info(f"Filtered Movies initialization: {filtered_movies}")

        #For every movie in our movies list, if a movies ReleaseYear is equal to the year that was given in the URL parameter, it will add that movie to the empty list: filtered_movies
        for movie in movies_to_list:
            if movie["ReleaseYear"] == year:
                filtered_movies.append(movie)
                logging.info(f"Filtered Movies: {filtered_movies}")

                #Converts filtered_movies list to json
                filtered_movies_json = json.dumps(filtered_movies)
                logging.info(f"Filtered Movies JSON: {filtered_movies_json}")

        return func.HttpResponse(
            #Returns json DATA
            filtered_movies_json
        )
#Get Movies By year with azure table client
@app.function_name(name="GetMoviesByYearWithTableClient")
@app.route(route="GetMoviesByYearWithTableClient")
@app.table_input(arg_name="movies", table_name="Movies",connection="AzureWebJobsStorage")
def GetMoviesByYearWithTableClient(req: func.HttpRequest, movies) -> func.HttpResponse:
    logging.info("running query with Table Client")
    logging.info(f"Movies Type: {type(movies)}")

    year = req.params.get('year')
    logging.info(f"Year received: {year}")
    logging.info(f"Year type: {type(year)}")

    #Checks if year parameter exists
    if not year:
        return func.HttpResponse("Please enter a year")
    
    #Checks if year parameter is digits
    if not year.isdigit():
        return func.HttpResponse("Please enter a valid year. It must be 4 digits. Example: 2008", status_code=400)
    
    #Checks if year parameter is 4 digits long
    if not len(year) == 4:
        return func.HttpResponse("Please enter a valid year. It must be 4 digits. Example: 2008", status_code=400)

    #Query
    movie_filter = f"ReleaseYear eq '{year}'"

    #Sets up table client
    table_client = TableClient.from_connection_string(conn_str=connection_string, table_name="Movies")
    logging.info(f"Table Client: {table_client}")
    logging.info(f"Table Client Type: {type(table_client)}")

    #Gets entities from table client that matches the query
    entities = table_client.query_entities(movie_filter)
    

    #initializing query result list
    query_result = []

    #adds entities from table client into query_result list
    for entity in entities:
        logging.info(f"Processing entity: {entity}")
        query_result.append(entity)

    logging.info(f"Query Result List: {query_result}")

    #Checks if query_results list is empty, this happens when the query does not return any results. AKA, the year that was requested does not exist in the table
    if not query_result:
        return func.HttpResponse(f"No movies with year {year} exist in this table.", status_code=404)

    #Converts result into JSON format
    query_result_json = json.dumps(query_result)
    logging.info(f"Query Result in JSON: {query_result_json}")
    logging.info(f"Query Result in JSON Type: {type(query_result_json)}")
    return func.HttpResponse(
        query_result_json
    )



#Get movies by genre with azure table client
@app.function_name(name="GetMoviesByGenreWithAzureTableClient")
@app.route(route="GetMoviesByGenreWithAzureTableClient")
@app.table_input(arg_name="movies", table_name="Movies", connection="AzureWebJobsStorage")
def GetMoviesByGenreWithAzureTableClient(req: func.HttpRequest, movies) -> func.HttpResponse:
    logging.info("Running GetMoviesByGenreWithAzureTableClient")

    genre = req.params.get('genre')

    #Checks if genre parameter exists
    if not genre:
        return func.HttpResponse("Please enter a genre")
    
    #Checks if genre parameter is digits
    if genre.isdigit():
        return func.HttpResponse("Please enter a valid genre.", status_code=400)
    

    movie_filter = f"Genre eq '{genre}'"
    #sets up table client
    table_client = TableClient.from_connection_string(conn_str=connection_string, table_name="Movies")
    entities = table_client.query_entities(movie_filter)

    query_result = []

    for entity in entities:
        query_result.append(entity)

    if not query_result: 
        return func.HttpResponse(f"The genre {genre} does not exist in this table.")

    query_result_json = json.dumps(query_result)

    return func.HttpResponse(query_result_json)
    



    #Get Movies by Genre
@app.function_name(name="GetMoviesByGenre")
@app.route(route="GetMoviesByGenre")
@app.table_input(arg_name="movies", table_name="Movies", connection="AzureWebJobsStorage")
def GetMoviesByGenre(req: func.HttpRequest, movies) -> func.HttpResponse:
    logging.info('Running GetMoviesbyGenre')
    logging.info(movies)

    movies_to_list=json.loads(movies)
    genre = req.params.get('genre')
    #Checks if genre parameter exists, if not, returns a status code 400
    if not genre:
        return func.HttpResponse("Please enter a genre", status_code=400)
    else:

        filtered_movies = []
        #For every movie in movies list, if the movie Genre is equal to the genre parameter from the URL, add it to the empty filtered_movies list.
        for movie in movies_to_list:
            if movie["Genre"] == genre:
                filtered_movies.append(movie)
        
        filtered_movies_json = json.dumps(filtered_movies)
        return func.HttpResponse(filtered_movies_json)

#Create Movie
@app.function_name(name="CreateMovie")
@app.route(route="CreateMovie")
@app.table_output(arg_name="movie", table_name="Movies", connection="AzureWebJobsStorage")
def CreateMovie(req: func.HttpRequest, movie) -> func.HttpResponse:
    logging.info('running func CreateMovie')
    logging.info(f"Movie Data Type: {type(movie)}")

    movie = req.get_json()
    if not movie:
        return func.HttpResponse("Please enter a movie", status_code=400)
    
    if not (movie["ReleaseYear"].isdigit() and len(movie["ReleaseYear"]) == 4):
        return func.HttpResponse("Invalid ReleaseYear. It must be a 4-digit year. Example: 2020", status_code=400)

    
    required_keys = ["ReleaseYear", "Genre", "Title", "posterURL"]
    if not all (key in movie for key in required_keys):
        return func.HttpResponse("Missing movie data", status_code=400)
        

    
    endpoint = f"https://{account_name}.table.core.windows.net/Movies"
    credential = AzureNamedKeyCredential(name=account_name, key=account_key)
    service = TableServiceClient(endpoint=endpoint,credential=credential)
    moviestable = service.get_table_client("Movies")
    movie_data = {
        "PartitionKey": movie["ReleaseYear"],
        "RowKey": movie["Title"],
        "Title": movie["Title"],
        "Genre": movie["Genre"],
        "posterURL": movie["posterURL"],
        "ReleaseYear": movie["ReleaseYear"]
        }
    
    moviestable.create_entity(movie_data)
    

    return func.HttpResponse("Movie added successfully!", status_code=201)


        
