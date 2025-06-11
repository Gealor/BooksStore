from fastapi.testclient import TestClient
from sqlalchemy import text

from core.models import db_helper, db_helper_mock
from core.schemas.users import UserCreate
from crud import users as users_crud
from main import main_app

# заменяю зависимость от основной базы данных на mock базу данных
main_app.dependency_overrides[db_helper.session_getter] = db_helper_mock.session_getter
client = TestClient(main_app)

def test_get_all_users():
    
    response = client.get('/api/users/find-users')

    print(response.json())
    assert response.status_code == 200

def test_unauthorized_lending_book():
    # with pytest.raises(HTTPException):
    params = {
        "book_id" : 4,
    }
    response = client.post("/api/business/lending-book", params=params)
    
    assert response.status_code == 401 # Unauthorized
    assert response.json()["detail"] == "Not authenticated" 

def test_authorized_and_me():
    form_data = {
        "username" : "ivan.petrov@example.com",
        "password" : "Petrov2025!"
    }
    # т.к. в /api/auth/login параметры являются Form, то они ожидают не json, а application/x-www-form-urlencoded, значит передаем data, а не json
    response_1 = client.post('/api/auth/login', data = form_data)

    assert response_1.status_code == 200

    body = response_1.json()

    headers = {
        "Authorization" : f"Bearer {body['access_token']}"
    }

    response_2 = client.get('/api/users/me', headers=headers)
    assert response_2.status_code == 200

def test_authorized_and_lending_book():
    form_data = {
        "username" : "maria.smirnova@example.org",
        "password" : "Sm1rnova#88"
    }
    # т.к. в /api/auth/login параметры являются Form, то они ожидают не json, а application/x-www-form-urlencoded, значит передаю data, а не json
    response_1 = client.post('/api/auth/login', data = form_data)

    assert response_1.status_code == 200

    body = response_1.json()

    headers = {
        "Authorization" : f"Bearer {body['access_token']}"
    }

    params = {
        "book_id" : 5,
    }

    response_2 = client.post("/api/business/lending-book", params = params, headers=headers)
    assert response_2.status_code == 200


def test_authorized_and_return_book():
    form_data = {
        "username" : "maria.smirnova@example.org",
        "password" : "Sm1rnova#88"
    }

    response_1 = client.post('/api/auth/login', data = form_data)

    assert response_1.status_code == 200

    body = response_1.json()

    headers = {
        "Authorization" : f"Bearer {body['access_token']}"
    }

    params = {
        "borrowed_id" : 1,
    }

    response_2 = client.patch("/api/business/return-book", params = params, headers=headers)
    assert response_2.status_code == 200