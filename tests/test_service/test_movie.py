# Тесты для сервиса фильмы
from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from service.movie import MovieService


@pytest.fixture
def test_movies():
    test_movie1 = Movie(id=1, title='Чернуха', description='История Малевича', trailer='No', year=2020, rating=0,
                        genre_id=4, director_id=2)
    test_movie2 = Movie(id=2, title='Оптимистическая трагедия', description='История Малевича2', trailer='No',
                        year=2022, rating=0, genre_id=4, director_id=2)
    return {1: test_movie1, 2: test_movie2}


@pytest.fixture
def movie(test_movies):
    movie = Movie
    movie.delete = MagicMock()
    movie.update = MagicMock()
    movie.partially_update = MagicMock()
    movie.get_all = MagicMock(return_value=test_movies.values())
    movie.get_one = MagicMock(side_effect=test_movies.get)
    movie.create = MagicMock(return_value=Movie(id=3))
    return movie


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie):
        self.movie_service = MovieService(dao=movie)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id == 1
        assert movie.title == 'Чернуха'

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_d = {
            "title": "Безвкусица",
        }
        movie = self.movie_service.create(movie_d)
        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_d = {"id": 2, "title": "Оптимистическая", "description": "История Малевича3", "trailer": "No",
                   "year": 2000, "rating": 10, "genre_id": 4, "director_id": 2, }
        self.movie_service.update(movie_d)

    def test_partially_update(self):
        movie_d = {
            "id": 2,
            "year": 1984,
            }
        movie = self.movie_service.partially_update(movie_d)
        assert movie.year == movie_d.get('year')
