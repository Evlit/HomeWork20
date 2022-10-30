# Тесты для сервиса режиссеры
from unittest.mock import MagicMock

import pytest

from dao.model.director import Director
from service.director import DirectorService


@pytest.fixture
def test_directors():
    test_director1 = Director(id=1, name='Квентин Тарантино')
    test_director2 = Director(id=2, name='Сергей Бондарчук')
#    test_director3 = Director(id=3, name='Жора Крыжовников')
    return {1: test_director1, 2: test_director2}


@pytest.fixture
def director(test_directors):
    director = Director
    director.delete = MagicMock()
    director.update = MagicMock()
    director.get_all = MagicMock(return_value=test_directors.values())
    director.get_one = MagicMock(side_effect=test_directors.get)
    director.create = MagicMock(return_value=Director(id=3))
    return director


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director):
        self.director_service = DirectorService(dao=director)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id == 1
        assert director.name == 'Квентин Тарантино'

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        director_d = {
            "name": "Ivan",
        }
        director = self.director_service.create(director_d)
        assert director.id is not None

    def test_delete(self):
        self.director_service.delete(1)

    def test_update(self):
        director_d = {
            "id": 3,
            "name": "Ваня",
            }
        self.director_service.update(director_d)
