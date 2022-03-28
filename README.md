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
- Finally, `./manage.py runserver`to start the server.

### Optional Commands

- `./manage.py create_users` to create a superuser with username=superuser and password=password and a simple user with username=user and password=password.
- `./manage.py populate_movies` to add 20 movies to the list. `./manage.py depopulate_movies` can be used to remove every movie from the list.


## How to Use

Running this curl command `curl -X GET http://127.0.0.1:8000/api/v1/movies` will return a list of all the movies, containing their title, 
category, rating and the url to get their details.

<img width="455" alt="Screenshot 2022-03-28 at 14 20 33" src="https://user-images.githubusercontent.com/15820388/160387502-a8002dd2-a402-4d02-a4e8-8c59067c8dc6.png">

`curl -X GET http://127.0.0.1:8000/<details_url>` will then return information about the specific movie.

<img width="980" alt="Screenshot 2022-03-28 at 14 23 27" src="https://user-images.githubusercontent.com/15820388/160388080-86c85c0f-0217-45f5-903b-d607cd6b1b90.png">

The GET request can take arguments that filter the list of movies returned. The movies can be filtered based on their category and their ranking.
Both arguments can be set on the same request.
For example: `curl -X GET http://127.0.0.1:8000/api/v1/movies?category=Fantasy&rating=9`



- `./manage.py crf_create_token <username>` to create authentication tokens for each user.  

## Testing

Run `./manage.py test --shuffle` to test the project. `--shuffle` ensures a random test execution order.
