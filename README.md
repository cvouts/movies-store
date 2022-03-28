# Online Movies Rent Store

An online store where users can rent movies. 

Created in Django.

## Project Details

This is a proof of concept project, that serves the following API responses:
- Anyone can
  - get a list of all movies
  - filter the list based on movie categories or ranking
  - get the details for a movie.   
- Logged-in regular users can also
  - rent a movie
  - return a movie and get the charge based on the days they had it
  - get a list of rentals they have from the store
  - filter the list based on movie title, category, ranking, or rental status.
- Finally, superusers can
  - add a movie to the list
  - edit a movie listing
  - delete a movie from the list.

## Installation

Run the following commands in the `movies-store/movies_store/` directory:
- `python3 -m venv venv; source venv/bin/activate` to create and use a python virtual environment.
- `pip install -r requirments.txt` to install the project's dependencies.
- `./manage.py migrate` to create the project tables in the database.
- Finally, `./manage.py runserver` to start the server.

### Optional

- Run `./manage.py create_users` to create a superuser with username=superuser and password=password and a simple user with username=user and password=password.
- Run `./manage.py populate_movies` to add 20 movies to the list. `./manage.py depopulate_movies` can be used to remove every movie from the list.
- Install [direnv](https://direnv.net/) so that you can automatically configure your environment when you cd into this project's directory

## User Authentication

In order for a user's requests to have proper authentication, an authorization token must be included in their request. 
Run `./manage.py drf_create_token <username>` to create a token for a user, and include it by adding 
`-H "Authorization: Token <token_string>"` to the curl commands that require authentication.

## How to Use

The project has the following URLs:
1. /movies
2. /rent
3. /return
4. /profile

### /movies

#### GET Request
Running this curl command ```curl -X GET "http://127.0.0.1:8000/api/v1/movies"``` will return a list of all the movies, containing their title, 
category, rating and the url to get their details.

```
{
    "title": "The Shawshank Redemption",
    "category": "Drama",
    "rating": 9.3,
    "details_url": "/api/v1/movies/12"
},
{
    "title": "The Lord of the Rings: The Return of the King",
    "category": "Fantasy",
    "rating": 9.0,
    "details_url": "/api/v1/movies/13"
},
{
    "title": "The Godfather",
    "category": "Crime",
    "rating": 9.2,
    "details_url": "/api/v1/movies/14"
},
```
`curl -X GET "http://127.0.0.1:8000/<details_url>"` will then return information about the specific movie.
```
{
    "id": 12,
    "title": "The Shawshank Redemption",
    "category": "Drama",
    "rating": 9.3,
    "details": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
}
```

The GET request can take arguments that filter the list of movies returned. The movies can be filtered based on their **category** and their **ranking**.
Both arguments can be set in the same request.
For example: ```curl -X GET "http://127.0.0.1:8000/api/v1/movies?category=Fantasy&rating=9"```

#### POST / PATCH / DELETE Request

A logged in superuser can make requests to /movies with additional methods.

- POST: the following will add the movie to the list.
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token <token_string>" http://127.0.0.1:8000/api/v1/movies -d "{\"title\":\"Superman\", \"category\": \"Superhero\", \"rating\":7.5}"
``` 

- PATCH: the following will update the entry. 
```
curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Token <token_string>" http://127.0.0.1:8000/api/v1/movies -d "{\"details\":\"An alien orphan is sent from his dying planet to Earth, where he grows up to become his adoptive home's first and greatest superhero.\"}"
``` 

The previous POST and PATCH examples are given to demonstrate in a simple but not-so-pretty-looking way, how to pass data arguments. Another way would be with a json file, so instead of `-d "{\"title\":\"Superman\", \"category\": \"Superhero\", \"rating\":7.5}"` we would include
`--data-binary @path/to/movie.json` to the curl command, where the movie.json file would be:
```
{
  "title": "Superman",
  "category": "Superhero",
  "rating": 7.4
}
```

- DELETE: the following will delete the movie with the given id.
```
curl -X DELETE -H "Authorization: Token <token_string>" http://127.0.0.1:8000/api/v1/movies/<movie_id>
``` 
 
### /rent and /return

A logged in user can rent a movie by sending a POST request to /rent and providing the movie's id. For example, by sending the following request, the user requests to rent the movie with id=12.
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token <token_string>" http://127.0.0.1:8000/api/v1/rent -d "{\"movie\":\"12\"}"
```

They can similarly return a rented movie. This next command will complete the return and notify the user about the charge.
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token <token_string>" http://127.0.0.1:8000/api/v1/return -d "{\"movie\":\"12\"}"
```

### /profile

A GET request to /profile, by a logged in user, will return a list of information about every occasion they have rented any movie in the store.
```
curl -X GET -H "Authorization: Token <token_string>" http://127.0.0.1:8000/api/v1/profile
```

Additional GET parameters can be included to filter the list, based on the movie's **title** (to get information about every time they have rented a specific movie), the movie's **category**, and the **status** of the renting (if the movie is currently being rented or was in the past).
A couple examples:
```
curl -X GET -H "Authorization: Token <token_string>" "http://127.0.0.1:8000/api/v1/profile?category=Fantasy"
```
```
curl -X GET -H "Authorization: Token <token_string>" "http://127.0.0.1:8000/api/v1/profile?status=rented_currently"
```

These parameters can also be combined.

The list includes the renting's cost of the renting's charge. If the movie is currently on rent, the cost returned is the cost accrued up to the current day.

## Testing

Run `./manage.py test --shuffle` to test the project. `--shuffle` ensures a random test execution order.

## Considerations
- Authentication: the scope of this project does not include real world authentication considerations like:
  - the danger of sending the token through http instead of https, therefore sending it through the internet in plain text.
  - the need for the user to be able to revoke their token or know when it was last used.
  - the danger of keeping all the tokens in plain text in the database.
  - not keeping the same tokens indefinitely.

- Pagination: If there were hundreds of thousands of movies in the database, requests to /movies from multiple users would slow down our service considerably. Pagination would allow us to serve only a small number of movies at a time.  

- POSTing the same movie multiple times: Since additional information about movies like "release year" are not included, it is currently possible for a superuser to successfully add the exact same movie to the database multiple times. 
