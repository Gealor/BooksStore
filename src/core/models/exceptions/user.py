class BaseUserException(Exception):
    pass


class UserNotFoundException(BaseUserException):
    pass


class SelfDeleteException(BaseUserException):
    pass


class ListUsersNotFoundException(BaseUserException):
    pass
