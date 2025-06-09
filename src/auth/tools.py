import copy
import datetime
from typing import Any
import jwt
import bcrypt

from core.config import settings

def encode_jwt(
    payload : dict,
    private_key : str = settings.jwt.private_key_path.read_text(), # получаю содержимое файла с помощью read_text библиотеки pathlib
    algorithm : str = settings.jwt.algorithm, 
    expire_minutes : int = settings.jwt.access_token_expire_minutes       
):
    copy_payload = copy.copy(payload)
    # exp - время жизни токена, т.е. указыватся дата, после которой токен сгорает
    copy_payload.update(
        # время для iat и exp надо указывать время по utc, т.е. всемирное координированное время, универсальный мировой стандарт времени.
        # короче без учета часовых поясов
        exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expire_minutes),
        iat = datetime.datetime.now(datetime.timezone.utc),
    )
    encoded = jwt.encode(
        copy_payload,
        private_key,
        algorithm = algorithm
    )
    return encoded

def decode_jwt(
        jwt_token : str | bytes,
        public_key : str = settings.jwt.public_key_path.read_text(),
        algorithm : str = settings.jwt.algorithm,
):
    decoded = jwt.decode(
        jwt_token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded

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
