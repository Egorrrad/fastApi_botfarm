from httpx import AsyncClient

from tests.conftest import client


async def test_get_users_none(ac: AsyncClient):
    """
    Получение всех созданных пользователей, в базе еще нет пользователей
    """
    response = await ac.get("/users")

    assert response.status_code == 200
    assert response.json() == []

def test_create_user_valid(ac: AsyncClient):
    """
    Добавление пользователя при правильном запросе
    """
    request_data = {
        "login": "vader@deathstar.com",
        "password": "rainbow",
        "project_id": 1,
        "env": "prod",
        "domain": "www.ru"
    }

    response = client.post("/user", json=request_data)

    assert response.status_code == 201


def test_create_user_dublicate(ac: AsyncClient):
    """
    Добавление дубликата пользователя при правильном запросе с существующим логином
    """
    request_data = {
        "login": "vader@deathstar.com",
        "password": "rainbow",
        "project_id": 1,
        "env": "prod",
        "domain": "www.ru"
    }

    response = client.post("/user", json=request_data)

    assert response.status_code == 409


def test_create_user_invalid(ac: AsyncClient):
    """
    Добавление пользователя при неправильно написанном email (поле логин)
    """
    request_data = {
        "login": "vader123deathstar.com",
        "password": "rainbow",
        "project_id": 1,
        "env": "prod",
        "domain": "www.ru"
    }

    response = client.post("/user", json=request_data)

    assert response.status_code == 422


async def test_get_users(ac: AsyncClient):
    """
    Получение всех созданных пользователей
    """
    response = await ac.get("/users")

    assert response.status_code == 200
    assert response.json()[0]["login"] == "vader@deathstar.com"
    assert response.json()[0]["project_id"] == 1
    assert response.json()[0]["env"] == "prod"
    assert response.json()[0]["domain"] == "www.ru"


async def test_lock_user(ac: AsyncClient):
    """
    Блокировка пользователя, который не был заблокирован до этого
    """
    request_data = {
        "id": 1
    }

    response = await ac.put("/user/lock", json=request_data)

    assert response.status_code == 201
    assert response.json()["locked_yet"] == False

    locktime = response.json()["locktime"]

    assert locktime is not None


async def test_lock_user_dublicate(ac: AsyncClient):
    """
    Блокировка пользователя, который был заблокирован до этого
    """
    request_data = {
        "id": 1
    }

    response = await ac.put("/user/lock", json=request_data)

    assert response.status_code == 409


async def test_lock_uncreated_user(ac: AsyncClient):
    """
    Блокировка несуществующего пользователя
    """
    request_data = {
        "id": 10
    }

    response = await ac.put("/user/lock", json=request_data)

    assert response.status_code == 404


async def test_unlock_uncreated_user(ac: AsyncClient):
    """
    Разлокировка несуществующего пользователя
    """
    request_data = {
        "id": 10
    }

    response = await ac.put("/user/lock", json=request_data)

    assert response.status_code == 404


async def test_unlock_user(ac: AsyncClient):
    """
    Разблокировка пользователя, который был заблокирован до этого
    """
    request_data = {
        "id": 1
    }

    response = await ac.put("/user/unlock", json=request_data)

    assert response.status_code == 201
    assert response.json()["locked_yet"] == False

    locktime = response.json()["locktime"]

    assert locktime is None


async def test_unlock_user_dublicate(ac: AsyncClient):
    """
    Разблокировка пользователя, который был разблокирован до этого
    """
    request_data = {
        "id": 1
    }

    response = await ac.put("/user/unlock", json=request_data)

    assert response.status_code == 409
