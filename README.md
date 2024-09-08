# Azure-Functions-Movies-API

Description:
MovieAPI is a Python-based API built using Azure Functions and Azure Table Storage. This API allows you to store and retrieve information about movies, including querying by release year or genre, and adding new movies. The API uses Azure's serverless architecture for easy scalability and cost efficiency.

Features: 
- Retrieve all movies stored in an Azure Table.
- Query movies by their release year or genre.
- Add new movies to the Azure Table.
- JSON response for easy integration with other systems.

# 1. GetMovies
- URL: https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMovies

Example: 
```
curl https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMovies
```
# 2. GetMoviesByYear
- URL https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMoviesByYear?year=<year>

Example:
```
curl https://dlvmoviesfunctionapi.azurewebsites.net/api/GetMoviesByYear?year=2008
```

Example Response:
```
[{"PartitionKey": "2008", "RowKey": "Inception", "Title": "Inception", "Genre": "Thriller", "posterURL": "inception.com/image.jpg", "ReleaseYear": "2008"}, {"PartitionKey": "2008", "RowKey": "The Dark Knight", "ReleaseYear": "2008", "Title": "The Dark Knight", "Genre": "Action", "posterURL": "https://example.org/example.jpeg"}]
```
