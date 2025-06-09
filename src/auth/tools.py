import copy
import datetime
from typing import Any
import jwt
import bcrypt

from core.config import settings

def hash_password(
    password : str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes : bytes = password.encode('utf-8')
    return bcrypt.hashpw(pwd_bytes, salt)


def compare_hashed_passwords(
        entered_password : bytes,
        hashed_password : bytes,
) -> bool:
    return bcrypt.checkpw(
        entered_password,
        hashed_password
    )
