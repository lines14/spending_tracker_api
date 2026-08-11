import json
from datetime import UTC, datetime, timedelta
from os import getenv

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.types import PublicKeyTypes

from dto.jwt_dto import JWTDTO
from utils.data_utils import DataUtils
from utils.storage_utils import StorageUtils


class JWTUtils:
    @staticmethod
    def generate_token(id: str) -> str:
        payload = JWTDTO(id=id, exp=datetime.now(UTC) + timedelta(seconds=int(getenv("TOKEN_TTL"))))

        return jwt.encode(payload.model_dump(), StorageUtils.private_key, algorithm=getenv("ENCODE_ALGORITHM"))

    @classmethod
    def verify_token(cls, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                cls.__parse_public_key(StorageUtils.public_key),
                algorithms=[getenv("ENCODE_ALGORITHM")],
                options={"verify_exp": False},
            )
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError(json.dumps(DataUtils.responses.token_expired_error)) from None
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError(json.dumps(DataUtils.responses.invalid_token_error)) from None

    @staticmethod
    def __parse_public_key(key_pem: str) -> PublicKeyTypes:
        key_bytes = key_pem.encode()
        return serialization.load_pem_public_key(key_bytes, backend=default_backend())
