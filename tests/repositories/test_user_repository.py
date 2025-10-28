import pytest
from core.models.users import User
from sqlalchemy.orm import Session

from core.schemas.users import UserCreate
from repositories.user_repository import UserRepository

# то что указывается в качестве параметров тестов и фикстур, может быть другими фикстурами
# (чтобы передать фикстуру надо просто передать в качестве параметра ее имя, с которой она была определена)
@pytest.fixture
def user_repo(session: Session):
    return UserRepository(session=session)

@pytest.fixture
def create_user():
    return UserCreate(name="Egor", email="test1@gmail.com", password="test1")

@pytest.fixture
def update_user():
    return {
        "name": "test4",
        "email": "test4@gmail.com"
    }

def test_get_all_users(user_repo, mock_users):
    result = user_repo.get_all_users()
    assert len(result) == len(mock_users)

def test_get_user_by_id_successful(user_repo, mock_users):
    result = user_repo.get_user_by_id(user_id=mock_users[0].id)

    assert result is not None
    assert result.id == mock_users[0].id
    assert result.name == mock_users[0].name
    assert result.email == mock_users[0].email

def test_get_user_by_id_not_found(user_repo, mock_users):
    result = user_repo.get_user_by_id(user_id=102)

    assert result is None

def test_create_user(user_repo, create_user):
    result = user_repo.create_user(create_user)

    assert result.name == create_user.name
    assert result.email == create_user.email
    
    find_user = user_repo.get_user_by_id(user_id=result.id)

    assert find_user is not None
    assert find_user.id == result.id

def test_delete_user(user_repo, create_user):
    result = user_repo.create_user(create_user)

    find_user = user_repo.get_user_by_id(user_id=result.id)

    assert find_user is not None
    assert find_user.id == result.id

    user_repo.delete_user_by_id(user_id=find_user.id)

    find_user = user_repo.get_user_by_id(user_id=result.id)

    assert find_user is None

def test_update_user(user_repo, mock_users, update_user):
    result = user_repo.get_user_by_id(user_id=mock_users[0].id)

    assert result is not None
    assert result.id == mock_users[0].id

    user_repo.update_user_data(user=result, new_data=update_user)
    updated_result = user_repo.get_user_by_id(user_id=mock_users[0].id)

    assert updated_result is not None
    assert updated_result.id == mock_users[0].id
    assert updated_result.name == update_user["name"]
    assert updated_result.email == update_user["email"]
    




