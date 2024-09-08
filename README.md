# Azure-Functions-Movies-API

Description:
MovieAPI is a Python-based API built using Azure Functions and Azure Table Storage. This API allows you to store and retrieve information about movies, including querying by release year or genre, and adding new movies. The API uses Azure's serverless architecture for easy scalability and cost efficiency.

Features: 
- Retrieve all movies stored in an Azure Table.
- Query movies by their release year or genre.
- Add new movies to the Azure Table.
- JSON response for easy integration with other systems.

# 1. GetMovies
- Description: Retrieves all movies stored in the Azure Table
- Method: GET
- URL: https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMovies

Example: 
```
curl https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMovies
```
# 2. GetMoviesByYear
- Description: Retrieves movies released in a specific year
- Method: GET
- URL https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMoviesByYear?year={year}

Example:
```
curl https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMoviesByYear?year=2008
```
# 3. GetMoviesByGenre
- Description: Retrives movies of a specific genre
- Method: GET
- URL: https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMoviesByGenre?genre={genre}

Example:
```
curl https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMoviesByGenre?genre=Action
```
# 4. GetMoviesByYearWithTableClient
- Description: Retrives movies of a specific year using the Azure Table Client
- Method: GET
- URL https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMoviesByYearWithTableClient?year={year}

Example:
```
curl https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMoviesByYearWithTableClient?year=2008
```
# 5. GetMoviesByGenreWithAzureTableClient
- Description: Retrieves movies of a specified genre using the Azure Table Client
- Method: GET
- URL https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMoviesByGenreWithAzureTableClient{genre}
Example:
```
curl https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMoviesByGenreWithAzureTableClient?genre=Action
```
# 5. CreateMovie
- Description: Adds a movie to the Azure Table
- Method: POST
- URL https://dlvmoviesfunctionapi.azurewebsites.net/api/CreateMovie
Example:
```
curl --location 'https://dlvmoviesfunctionapi.azurewebsites.net/api/CreateMovie' \
--header 'Content-Type: application/json' \
--data '{
  "Title": "The LEGO Batman Movie",
  "Genre": "Comedy",
  "ReleaseYear": "2017",
  "posterURL":"https://www.imdb.com/title/tt4116284/mediaviewer/rm2772370432/?ref_=tt_ov_i"
}
'
```
