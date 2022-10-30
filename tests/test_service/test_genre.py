# Тесты для сервиса жанры
from unittest.mock import MagicMock

import pytest

from dao.model.genre import Genre
from service.genre import GenreService


@pytest.fixture
def test_genres():
    test_genre1 = Genre(id=1, name='Чернуха')
    test_genre2 = Genre(id=2, name='Оптимистическая трагедия')
    return {1: test_genre1, 2: test_genre2}


@pytest.fixture
def genre(test_genres):
    genre = Genre
    genre.delete = MagicMock()
    genre.update = MagicMock()
    genre.get_all = MagicMock(return_value=test_genres.values())
    genre.get_one = MagicMock(side_effect=test_genres.get)
    genre.create = MagicMock(return_value=Genre(id=3))
    return genre


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre):
        self.genre_service = GenreService(dao=genre)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre is not None
        assert genre.id == 1
        assert genre.name == 'Чернуха'

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) > 0

    def test_create(self):
        genre_d = {
            "name": "Безвкусица",
        }
        genre = self.genre_service.create(genre_d)
        assert genre.id is not None

    def test_delete(self):
        self.genre_service.delete(1)

    def test_update(self):
        director_d = {
            "id": 3,
            "name": "Вкусовщина",
            }
        self.genre_service.update(director_d)
