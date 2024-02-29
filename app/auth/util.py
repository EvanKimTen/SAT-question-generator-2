import datetime
import json
from typing import Any, Union

import jwt
from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30
ALGORITHM = "HS256"
JWT_SECRET_KEY = "a-square-lab-secret-key"
JWT_REFRESH_SECRET_KEY = "a-square-lab-refresh-secret-key"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {"exp": expires_delta, "sub": str(subject), "user_id": subject}
    encoded_jwt = jwt.encode(
        payload, JWT_SECRET_KEY, ALGORITHM, json_encoder=DateTimeEncoder
    )
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    payload = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(payload, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET_KEY, [ALGORITHM])
