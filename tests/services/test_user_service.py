from repositories.user_repository import UserRepository
from services.user_service import UserService


def test_get_users_without_id(user_service: UserService, mocker, mock_users_list):
    # Создаю mock объект для репозитория
    mock_repo = mocker.MagicMock()
    mocker.patch("services.user_service.UserRepository", return_value=mock_repo)
    mock_repo.get_all_users.return_value = mock_users_list

    result = user_service.get_users()
    assert len(result) == len(mock_users_list)
    mock_repo.get_all_users.assert_called_once()
